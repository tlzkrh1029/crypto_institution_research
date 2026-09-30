from datetime import datetime, timedelta, timezone

import pytest

from collector import fetch
from collector.fetch import FetchError
from collector.market.base import Candle, Ticker
from collector.market.jobs import (
    MarketConfig, VenueConfig, compute_reactions, ensure_candles, load_market_config,
    poll_tickers, price_at)
from collector.market.kraken import KrakenClient
from collector.market.runner import MarketRunner
from collector.market.upbit import UpbitClient
from collector.report import build_report, market_status

from .conftest import ROOT

T0 = datetime(2026, 9, 24, 14, 30, tzinfo=timezone.utc)


def venue(name="upbit", quote="KRW", symbols=("HBAR",)) -> VenueConfig:
    return VenueConfig(name=name, enabled=True, terms_checked="test", quote=quote,
                       reference="BTC", symbols=symbols, ticker_interval_sec=300)


def cfg(*venues: VenueConfig, **overrides) -> MarketConfig:
    base = dict(venues=venues or (venue(),), anomaly_window_min=60, anomaly_excess_pct=3.0,
                anomaly_cooldown_hours=6, reactions_interval_sec=1800,
                reactions_lookback_days=30)
    base.update(overrides)
    return MarketConfig(**base)


class FakeVenue:
    """Hourly candles from a price function; tickers from a dict."""

    def __init__(self, price_fn, name="upbit", pages_backward=True, listed=None,
                 history_hours=None):
        self.name = name
        self.pages_backward = pages_backward
        self.price_fn = price_fn
        self.listed_markets = listed or {"KRW-BTC", "KRW-HBAR"}
        self.history_hours = history_hours
        self.ticker_prices: dict[str, float] = {}
        self.candle_calls = 0
        self.now = T0

    def market_id(self, symbol, quote):
        return f"{quote}-{symbol}"

    def markets(self):
        return self.listed_markets

    def tickers(self, market_ids):
        return [Ticker(m, self.ticker_prices[m], None, T0) for m in market_ids]

    def hourly_candles(self, market_id, to):
        self.candle_calls += 1
        if not self.pages_backward:
            to = self.now          # like Kraken: always the most recent candles
        end = to.replace(minute=0, second=0, microsecond=0)
        if end == to:
            end -= timedelta(hours=1)
        count = self.history_hours or 200
        return [Candle(market_id, end - timedelta(hours=i),
                       *(self.price_fn(market_id, end - timedelta(hours=i - 1)),) * 4, 1.0)
                for i in range(count)]


def linear_prices(market, when):
    """BTC flat at 100; the asset is 10 before T0 and +1% per hour after it."""
    if market.endswith("BTC"):
        return 100.0
    hours = (when - T0).total_seconds() / 3600
    return 10.0 if hours <= 0 else 10.0 * (1 + 0.01 * hours)


def seed_event(conn, *symbols):
    conn.execute("INSERT INTO events (id, title, first_published_at, first_seen_at, "
                 "last_seen_at) VALUES (1, 't', ?, ?, ?)",
                 ("2026-09-24T14:30:00Z", "2026-09-24T14:35:00Z", "2026-09-24T14:35:00Z"))
    for symbol in symbols:
        conn.execute("INSERT INTO event_assets (event_id, symbol) VALUES (1, ?)", (symbol,))
    conn.commit()


def reactions(conn):
    return {(r["symbol"], r["window_name"]): r for r in conn.execute(
        "SELECT * FROM price_reactions")}


def test_config_file_loads_with_3pct_threshold_and_kraken_for_qnt():
    c = load_market_config(ROOT / "config" / "market.yaml")
    assert c.anomaly_excess_pct == 3.0
    assert c.venue_for("QNT").name == "kraken"
    assert c.venue_for("HBAR").name == "upbit"
    assert c.venue_for("DOGE") is None


def test_price_at_uses_last_completed_candle(harness):
    ctx, *_ = harness
    client = FakeVenue(linear_prices)
    now = T0 + timedelta(days=10)
    ensure_candles(ctx.conn, client, "KRW-HBAR", T0 - timedelta(hours=25),
                   T0 + timedelta(hours=7), now)
    # At 14:30 the last completed candle is 13:00-14:00, before the event.
    assert price_at(ctx.conn, "upbit", "KRW-HBAR", T0) == pytest.approx(10.0)
    assert price_at(ctx.conn, "upbit", "KRW-HBAR", T0 + timedelta(hours=6)) == pytest.approx(
        linear_prices("KRW-HBAR", datetime(2026, 9, 24, 20, 0, tzinfo=timezone.utc)))


def test_reactions_measured_pending_and_no_market(harness):
    ctx, *_ = harness
    seed_event(ctx.conn, "HBAR", "QNT")
    client = FakeVenue(linear_prices)
    now = T0 + timedelta(hours=30)
    compute_reactions(ctx.conn, {"upbit": client}, cfg(), {"upbit": client.markets()}, now)
    rows = reactions(ctx.conn)
    assert rows[("HBAR", "pre_24h")]["asset_return"] == pytest.approx(0.0)
    assert rows[("HBAR", "24h")]["status"] == "measured"
    assert rows[("HBAR", "24h")]["excess_return"] > 0.2
    assert rows[("HBAR", "3d")]["status"] == "pending"
    assert rows[("QNT", "1h")]["status"] == "no_market"   # no venue configured for QNT
    calls = client.candle_calls
    compute_reactions(ctx.conn, {"upbit": client}, cfg(), {"upbit": client.markets()},
                      T0 + timedelta(days=8))
    rows = reactions(ctx.conn)
    assert rows[("HBAR", "7d")]["status"] == "measured" and client.candle_calls > calls


def test_second_venue_prices_its_own_symbols(harness):
    ctx, *_ = harness
    seed_event(ctx.conn, "HBAR", "QNT")
    upbit = FakeVenue(linear_prices)
    kraken = FakeVenue(linear_prices, name="kraken", pages_backward=False,
                       listed={"USD-BTC", "USD-QNT"}, history_hours=720)
    kraken.now = T0 + timedelta(days=2)
    c = cfg(venue(), venue("kraken", "USD", ("QNT",)))
    compute_reactions(ctx.conn, {"upbit": upbit, "kraken": kraken}, c,
                      {"upbit": upbit.markets(), "kraken": kraken.markets()},
                      T0 + timedelta(days=2))
    rows = reactions(ctx.conn)
    assert rows[("QNT", "24h")]["status"] == "measured"
    assert rows[("QNT", "24h")]["venue"] == "kraken"
    assert rows[("HBAR", "24h")]["venue"] == "upbit"
    assert kraken.candle_calls == 2        # one fetch per market, no paging


def test_short_history_venue_reports_no_data(harness):
    ctx, *_ = harness
    seed_event(ctx.conn, "QNT")
    kraken = FakeVenue(linear_prices, name="kraken", pages_backward=False,
                       listed={"USD-BTC", "USD-QNT"}, history_hours=720)
    kraken.now = T0 + timedelta(days=40)   # the event is older than 720 hours
    c = cfg(venue("kraken", "USD", ("QNT",)), reactions_lookback_days=60)
    compute_reactions(ctx.conn, {"kraken": kraken}, c, {"kraken": kraken.markets()}, kraken.now)
    assert reactions(ctx.conn)[("QNT", "24h")]["status"] == "no_data"


def test_ticker_anomaly_alert_at_3pct_and_cooldown(harness):
    ctx, *_ = harness
    client = FakeVenue(linear_prices)
    listed = client.markets()
    v, c = venue(), cfg()
    client.ticker_prices = {"KRW-BTC": 100.0, "KRW-HBAR": 10.0}
    assert poll_tickers(ctx.conn, client, v, c, listed, T0) == []     # no history yet
    client.ticker_prices = {"KRW-BTC": 101.0, "KRW-HBAR": 10.25}      # excess +1.5%: quiet
    assert poll_tickers(ctx.conn, client, v, c, listed, T0 + timedelta(minutes=60)) == []
    client.ticker_prices = {"KRW-BTC": 101.0, "KRW-HBAR": 10.45}      # excess +3.5%: alert
    alerts = poll_tickers(ctx.conn, client, v, c, listed, T0 + timedelta(minutes=61))
    assert len(alerts) == 1 and alerts[0].message.startswith("HBAR +4.5% vs BTC +1.0%")
    ctx.conn.execute("INSERT INTO alerts (created_at, level, source_id, message) "
                     "VALUES (?, 'medium', 'market:upbit', ?)",
                     ("2026-09-24T15:30:00Z", alerts[0].message))
    client.ticker_prices = {"KRW-BTC": 101.0, "KRW-HBAR": 12.0}
    assert poll_tickers(ctx.conn, client, v, c, listed, T0 + timedelta(minutes=65)) == []


class FakeResponse:
    def __init__(self, data, status=200):
        self._data, self.status_code = data, status

    def json(self):
        return self._data


class FakeSession:
    def __init__(self, routes):
        self.routes = routes
        self.calls = []

    def get(self, url, params=None, timeout=None, headers=None):
        self.calls.append((url, params, headers))
        return FakeResponse(self.routes[url.rsplit("/", 1)[-1]])


def test_kraken_client_parses_pairs_ticker_and_ohlc():
    session = FakeSession({
        "AssetPairs": {"error": [], "result": {
            "QNTUSD": {"altname": "QNTUSD"}, "XXBTZUSD": {"altname": "XBTUSD"}}},
        "Ticker": {"error": [], "result": {
            "QNTUSD": {"c": ["295.26", "1"], "v": ["10", "100"]},
            "XXBTZUSD": {"c": ["82987.3", "1"], "v": ["1", "2"]}}},
        "OHLC": {"error": [], "result": {"QNTUSD": [
            [1790744400, "284.47", "296.41", "283.81", "295.26", "291.7", "2867.2", 1312]],
            "last": 1790744400}},
    })
    client = KrakenClient("ua", session, sleep=lambda s: None)
    assert client.market_id("BTC", "USD") == "XBTUSD"
    assert {"QNTUSD", "XBTUSD"} <= client.markets()
    prices = {t.market: t.price for t in client.tickers(["QNTUSD", "XBTUSD"])}
    assert prices == {"QNTUSD": 295.26, "XBTUSD": 82987.3}
    candle = client.hourly_candles("QNTUSD", T0)[0]
    assert candle.close == 295.26 and candle.start_at.tzinfo is not None
    assert all(h["User-Agent"] == "ua" for _, _, h in session.calls)


def test_upbit_client_parses_ticker_and_candles():
    session = FakeSession({
        "ticker": [{"market": "KRW-HBAR", "trade_price": 145.0,
                    "acc_trade_price_24h": 1.0e10, "timestamp": 1790740000000}],
        "60": [{"market": "KRW-HBAR", "candle_date_time_utc": "2026-09-30T05:00:00",
                "opening_price": 144.0, "high_price": 146.0, "low_price": 143.0,
                "trade_price": 145.0, "candle_acc_trade_volume": 1000.0}],
    })
    client = UpbitClient("ua", session, sleep=lambda s: None)
    assert client.tickers(["KRW-HBAR"])[0].price == 145.0
    candle = client.hourly_candles("KRW-HBAR", T0)[0]
    assert candle.start_at == datetime(2026, 9, 30, 5, tzinfo=timezone.utc)


class Clock:
    def __init__(self):
        self.t = 5000.0

    def __call__(self):
        return self.t

    def sleep(self, seconds):
        self.t += seconds


class ClosingFakeSession(FakeSession):
    def __init__(self, routes):
        super().__init__(routes)
        self.closed = 0

    def close(self):
        self.closed += 1


def test_kraken_burst_reuses_the_connection_and_the_next_tick_resets_it():
    session = ClosingFakeSession({
        "AssetPairs": {"error": [], "result": {"QNTUSD": {"altname": "QNTUSD"}}},
        "Ticker": {"error": [], "result": {"QNTUSD": {"c": ["1", "1"], "v": ["1", "1"]}}},
    })
    clock = Clock()
    client = KrakenClient("ua", session, sleep=clock.sleep, monotonic=clock, clock=clock)
    client.markets()
    client.tickers(["QNTUSD"])                 # 1.1 s later, same burst
    client.tickers(["QNTUSD"])
    assert session.closed == 0 and len(session.calls) == 3
    clock.t += 300                             # the next ticker poll
    client.tickers(["QNTUSD"])
    assert session.closed == 1
    assert fetch.IDLE_RESET_SEC < 300


class BrokenVenue(FakeVenue):
    def __init__(self, error, **kwargs):
        super().__init__(linear_prices, **kwargs)
        self.error = error

    def tickers(self, market_ids):
        if self.error is not None:
            raise self.error
        return super().tickers(market_ids)


def runs(conn):
    return {r["source_id"]: r for r in conn.execute(
        "SELECT * FROM runs WHERE source_id GLOB 'market:*' ORDER BY id")}


def test_ticker_polls_are_recorded_in_runs_and_failures_are_isolated(harness):
    ctx, *_ = harness
    upbit = FakeVenue(linear_prices)
    upbit.ticker_prices = {"KRW-BTC": 100.0, "KRW-HBAR": 10.0}
    kraken = BrokenVenue(FetchError("ConnectionError: ('Connection aborted.', "
                                    "ConnectionResetError(54, 'Connection reset by peer'))"),
                         name="kraken", listed={"USD-BTC", "USD-QNT"})
    bithumb = BrokenVenue(KeyError("trade_price"), name="bithumb",
                          listed={"KRW-BTC", "KRW-XRP"})
    c = cfg(venue("bithumb", "KRW", ("XRP",)), venue("kraken", "USD", ("QNT",)), venue())
    runner = MarketRunner(ctx, c, {"bithumb": bithumb, "kraken": kraken, "upbit": upbit})
    runner.tick(T0)                             # bithumb and kraken fail first
    rows = runs(ctx.conn)
    assert rows["market:upbit"]["status"] == "ok"
    assert rows["market:upbit"]["items_seen"] == 2          # BTC and HBAR stored
    assert rows["market:kraken"]["status"] == "error"
    assert "ConnectionResetError(54" in rows["market:kraken"]["error"]
    assert rows["market:bithumb"]["error"] == "KeyError: 'trade_price'"
    assert ctx.conn.execute("SELECT COUNT(*) FROM price_reactions").fetchone()[0] == 0

    kraken.error = FetchError("HTTP 520", 520)
    runner.tick(T0 + timedelta(minutes=5))
    health = market_status(ctx.conn, "kraken")
    assert health["failures"] == 2 and health["last_error"] == "HTTP 520"
    assert market_status(ctx.conn, "upbit")["failures"] == 0

    text = build_report(ctx.conn, T0 + timedelta(minutes=10), days=1)
    line = next(x for x in text.splitlines() if x.startswith("market:kraken"))
    assert line.split()[1:5] == ["0", "-", "2", "-"]       # ok, 304, err, skip
    assert line.endswith("2026-09-24 23:35 KST HTTP 520")   # last error of the period
    line = next(x for x in text.splitlines() if x.startswith("market:upbit"))
    assert line.split()[1:4] == ["2", "-", "0"]
    assert "100.0" not in text and "10.0 " not in text        # no prices

    # `collector status` counts failures since the last ok poll: error, ok, error -> 1.
    kraken.error = None
    kraken.ticker_prices = {"USD-BTC": 100.0, "USD-QNT": 10.0}
    runner.tick(T0 + timedelta(minutes=10))
    kraken.error = FetchError("HTTP 502", 502)
    runner.tick(T0 + timedelta(minutes=15))
    ok_at = ctx.conn.execute("""SELECT started_at FROM runs WHERE source_id = 'market:kraken'
                                    AND status = 'ok'""").fetchall()
    assert len(ok_at) == 1
    health = market_status(ctx.conn, "kraken")
    assert health["failures"] == 1 and health["last_error"] == "HTTP 502"
    assert health["last_ok_at"] == ok_at[0][0]


def test_manual_market_poll_records_a_run_even_when_it_raises(harness):
    ctx, *_ = harness
    kraken = BrokenVenue(FetchError("HTTP 503", 503), name="kraken",
                         listed={"USD-BTC", "USD-QNT"})
    runner = MarketRunner(ctx, cfg(venue("kraken", "USD", ("QNT",))), {"kraken": kraken})
    with pytest.raises(FetchError):
        runner.run_tickers("kraken", T0)       # `collector market` calls this directly
    assert runs(ctx.conn)["market:kraken"]["error"] == "HTTP 503"

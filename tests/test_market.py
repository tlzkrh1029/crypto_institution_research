from datetime import datetime, timedelta, timezone

import pytest

from collector.market.jobs import (
    MarketConfig, compute_reactions, ensure_candles, poll_tickers, price_at)
from collector.market.upbit import Candle, Ticker

T0 = datetime(2026, 9, 24, 14, 30, tzinfo=timezone.utc)


def cfg(**overrides) -> MarketConfig:
    base = dict(enabled=True, terms_checked="test", quote="KRW", symbols=("HBAR", "QNT"),
                reference="BTC", ticker_interval_sec=300, anomaly_window_min=60,
                anomaly_excess_pct=5.0, anomaly_cooldown_hours=6, reactions_interval_sec=1800,
                reactions_lookback_days=30)
    base.update(overrides)
    return MarketConfig(**base)


class FakeUpbit:
    """Hourly candles from a price function; tickers from a dict."""

    def __init__(self, price_fn):
        self.price_fn = price_fn
        self.ticker_prices: dict[str, float] = {}
        self.candle_calls = 0

    def markets(self):
        return {"KRW-BTC", "KRW-HBAR"}

    def tickers(self, markets):
        return [Ticker(m, self.ticker_prices[m], None, T0) for m in markets]

    def hourly_candles(self, market, to, count=200):
        self.candle_calls += 1
        end = to.replace(minute=0, second=0, microsecond=0)
        if end == to:
            end -= timedelta(hours=1)
        out = []
        for i in range(count):
            start = end - timedelta(hours=i)
            p = self.price_fn(market, start + timedelta(hours=1))
            out.append(Candle(market, start, p, p, p, p, 1.0))
        return out


def linear_prices(market, when):
    """BTC flat at 100; HBAR 10 before T0 and +1% per hour after it."""
    if market == "KRW-BTC":
        return 100.0
    hours = (when - T0).total_seconds() / 3600
    return 10.0 if hours <= 0 else 10.0 * (1 + 0.01 * hours)


def seed_event(conn, symbol="HBAR"):
    conn.execute("INSERT INTO events (id, title, first_published_at, first_seen_at, "
                 "last_seen_at) VALUES (1, 't', ?, ?, ?)",
                 ("2026-09-24T14:30:00Z", "2026-09-24T14:35:00Z", "2026-09-24T14:35:00Z"))
    conn.execute("INSERT INTO event_assets (event_id, symbol) VALUES (1, ?)", (symbol,))
    conn.commit()


def test_price_at_uses_last_completed_candle(harness):
    ctx, *_ = harness
    client = FakeUpbit(linear_prices)
    now = T0 + timedelta(days=10)
    ensure_candles(ctx.conn, client, "KRW-HBAR", T0 - timedelta(hours=25),
                   T0 + timedelta(hours=7), now)
    # At 14:30 the last completed candle is 13:00-14:00, before the event.
    assert price_at(ctx.conn, "KRW-HBAR", T0) == pytest.approx(10.0)
    assert price_at(ctx.conn, "KRW-HBAR", T0 + timedelta(hours=6)) == pytest.approx(
        linear_prices("KRW-HBAR", datetime(2026, 9, 24, 20, 0, tzinfo=timezone.utc)))


def test_reactions_measured_pending_and_no_market(harness):
    ctx, *_ = harness
    seed_event(ctx.conn, "HBAR")
    ctx.conn.execute("INSERT INTO event_assets (event_id, symbol) VALUES (1, 'QNT')")
    client = FakeUpbit(linear_prices)
    now = T0 + timedelta(hours=30)
    compute_reactions(ctx.conn, client, cfg(), client.markets(), now)
    rows = {(r["symbol"], r["window_name"]): r for r in ctx.conn.execute(
        "SELECT * FROM price_reactions")}
    assert rows[("HBAR", "pre_24h")]["asset_return"] == pytest.approx(0.0)
    assert rows[("HBAR", "24h")]["status"] == "measured"
    assert rows[("HBAR", "24h")]["excess_return"] > 0.2
    assert rows[("HBAR", "3d")]["status"] == "pending"
    assert rows[("QNT", "1h")]["status"] == "no_market"
    # Measured windows are not fetched again; pending ones are finished later.
    calls = client.candle_calls
    compute_reactions(ctx.conn, client, cfg(), client.markets(), T0 + timedelta(days=8))
    rows = {(r["symbol"], r["window_name"]): r["status"] for r in ctx.conn.execute(
        "SELECT * FROM price_reactions")}
    assert rows[("HBAR", "7d")] == "measured" and client.candle_calls > calls


def test_ticker_anomaly_alert_and_cooldown(harness):
    ctx, *_ = harness
    client = FakeUpbit(linear_prices)
    listed = client.markets()
    c = cfg(symbols=("HBAR",))
    client.ticker_prices = {"KRW-BTC": 100.0, "KRW-HBAR": 10.0}
    assert poll_tickers(ctx.conn, client, c, listed, T0) == []     # no history yet
    client.ticker_prices = {"KRW-BTC": 101.0, "KRW-HBAR": 11.0}
    alerts = poll_tickers(ctx.conn, client, c, listed, T0 + timedelta(minutes=60))
    assert len(alerts) == 1 and alerts[0].message.startswith("HBAR +10.0% vs BTC +1.0%")
    ctx.conn.execute("INSERT INTO alerts (created_at, level, source_id, message) "
                     "VALUES (?, 'medium', 'market:upbit', ?)",
                     ("2026-09-24T15:30:00Z", alerts[0].message))
    client.ticker_prices = {"KRW-BTC": 101.0, "KRW-HBAR": 12.0}
    assert poll_tickers(ctx.conn, client, c, listed, T0 + timedelta(minutes=65)) == []

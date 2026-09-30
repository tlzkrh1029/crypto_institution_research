"""Market jobs: ticker snapshots with an anomaly check (fast path, only while
market.yaml tickers.enabled is true; off since docs/decisions.md D-015) and
price reactions around events (slow path, always on). docs/collector-spec.md
sections 2 and 5, docs/research-principles.md section 7.

Each symbol is priced on one venue (config/market.yaml) against that venue's
reference symbol (BTC), so returns never mix currencies or venues.
"""

from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import yaml

from ..config import ConfigError
from ..fetch import FetchError
from ..notify import Alert
from ..timeutil import from_iso, to_iso
from .base import VenueClient

log = logging.getLogger("collector.market")

CANDLE_MIN = 60
MAX_CANDLE_GAP = timedelta(hours=3)   # tolerate hours without trades
WINDOWS: dict[str, tuple[timedelta, timedelta]] = {
    "pre_24h": (timedelta(hours=-24), timedelta(0)),
    "1h": (timedelta(0), timedelta(hours=1)),
    "6h": (timedelta(0), timedelta(hours=6)),
    "24h": (timedelta(0), timedelta(hours=24)),
    "3d": (timedelta(0), timedelta(days=3)),
    "7d": (timedelta(0), timedelta(days=7)),
}


@dataclass(frozen=True)
class VenueConfig:
    name: str
    enabled: bool
    terms_checked: str
    quote: str
    reference: str
    symbols: tuple[str, ...]
    ticker_interval_sec: int
    # Symbols polled for tickers and checked for anomalies (market.yaml `watch`).
    # `symbols` is the reaction venue map; None (no `watch` key) watches them all.
    watch: tuple[str, ...] | None = None

    @property
    def watch_symbols(self) -> tuple[str, ...]:
        return self.symbols if self.watch is None else self.watch


@dataclass(frozen=True)
class MarketConfig:
    venues: tuple[VenueConfig, ...]
    anomaly_window_min: int
    anomaly_excess_pct: float
    anomaly_cooldown_hours: int
    reactions_interval_sec: int
    reactions_lookback_days: int
    # Real-time ticker polling and its anomaly alerts (market.yaml tickers.enabled).
    # Price reactions do not depend on it.
    tickers_enabled: bool = True

    @property
    def enabled_venues(self) -> tuple[VenueConfig, ...]:
        return tuple(v for v in self.venues if v.enabled)

    def venue_for(self, symbol: str) -> VenueConfig | None:
        for venue in self.enabled_venues:
            if symbol in venue.symbols:
                return venue
        return None


TOP_LEVEL_KEYS = {"venues", "tickers", "anomaly", "reactions"}
TICKERS_KEYS = {"enabled"}


def load_market_config(path: Path) -> MarketConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    # A misspelled key (e.g. 'ticker:' or 'tickers: {enable: false}') must not
    # silently leave ticker polling and anomaly alerts on.
    unknown = sorted(map(str, set(raw) - TOP_LEVEL_KEYS))
    if unknown:
        raise ConfigError(f"market.yaml: unknown top-level key(s) {unknown}; "
                          f"allowed: {sorted(TOP_LEVEL_KEYS)}")
    venues = []
    seen: set[str] = set()
    for name, v in (raw.get("venues") or {}).items():
        if v.get("enabled", False) and not v.get("terms_checked"):
            raise ConfigError(f"market.yaml: venues.{name}.terms_checked is required")
        interval = int(v.get("ticker_interval_sec", 300))
        if interval < 60:
            raise ConfigError(f"market.yaml: venues.{name}.ticker_interval_sec must be >= 60")
        symbols = tuple(v.get("symbols", []))
        watch = v.get("watch")
        if watch is not None:
            watch = tuple(watch)
            extra = sorted(set(watch) - set(symbols))
            if extra:
                raise ConfigError(f"market.yaml: venues.{name}.watch {extra} not in symbols")
        if v.get("enabled", False):
            dup = seen & set(symbols)
            if dup:
                raise ConfigError(f"market.yaml: {sorted(dup)} listed on more than one venue")
            seen |= set(symbols)
        venues.append(VenueConfig(
            name=name,
            enabled=bool(v.get("enabled", False)),
            terms_checked=str(v.get("terms_checked", "")),
            quote=v["quote"],
            reference=v.get("reference", "BTC"),
            symbols=symbols,
            ticker_interval_sec=interval,
            watch=watch,
        ))
    anomaly = raw.get("anomaly", {})
    reactions = raw.get("reactions", {})
    tickers = raw.get("tickers")
    if tickers is None:
        tickers = {}   # no block: tickers stay on, as before the block existed
    if not isinstance(tickers, dict):
        raise ConfigError("market.yaml: tickers must be a mapping, e.g. 'tickers: "
                          "{enabled: false}'")
    unknown = sorted(map(str, set(tickers) - TICKERS_KEYS))
    if unknown:
        raise ConfigError(f"market.yaml: unknown key(s) under tickers {unknown}; "
                          "only 'enabled' is allowed")
    tickers_enabled = tickers.get("enabled", True)
    if not isinstance(tickers_enabled, bool):
        raise ConfigError(f"market.yaml: tickers.enabled must be true or false, "
                          f"got {tickers_enabled!r}")
    cfg = MarketConfig(
        venues=tuple(venues),
        anomaly_window_min=int(anomaly.get("window_minutes", 60)),
        anomaly_excess_pct=float(anomaly.get("excess_return_pct", 3.0)),
        anomaly_cooldown_hours=int(anomaly.get("cooldown_hours", 6)),
        reactions_interval_sec=int(reactions.get("interval_sec", 1800)),
        reactions_lookback_days=int(reactions.get("lookback_days", 30)),
        tickers_enabled=tickers_enabled,
    )
    if cfg.reactions_interval_sec < 300:
        raise ConfigError("market.yaml: reactions.interval_sec must be >= 300")
    return cfg


# --- tickers and anomalies ---------------------------------------------------

def poll_tickers(conn: sqlite3.Connection, client: VenueClient, venue: VenueConfig,
                 cfg: MarketConfig, listed: set[str], now: datetime) -> list[Alert]:
    by_market = {client.market_id(s, venue.quote): s
                 for s in (venue.reference, *venue.watch_symbols)}
    wanted = [m for m in by_market if m in listed]
    tickers = client.tickers(wanted)
    with conn:
        for t in tickers:
            symbol = by_market.get(t.market)
            if symbol is None:
                continue
            conn.execute(
                "INSERT OR REPLACE INTO market_snapshots VALUES (?, ?, ?, ?, ?, ?)",
                (client.name, symbol, venue.quote, to_iso(now), t.price, t.acc_trade_value_24h))
    return _anomalies(conn, client.name, venue, cfg, now)


def _price_near(conn: sqlite3.Connection, venue: str, symbol: str, target: datetime,
                tolerance: timedelta) -> float | None:
    row = conn.execute(
        """SELECT price FROM market_snapshots WHERE venue = ? AND symbol = ?
               AND ts BETWEEN ? AND ?
           ORDER BY abs(julianday(ts) - julianday(?)) LIMIT 1""",
        (venue, symbol, to_iso(target - tolerance), to_iso(target + tolerance),
         to_iso(target))).fetchone()
    return row["price"] if row else None


def _anomalies(conn: sqlite3.Connection, venue_name: str, venue: VenueConfig,
               cfg: MarketConfig, now: datetime) -> list[Alert]:
    window = timedelta(minutes=cfg.anomaly_window_min)
    tolerance = timedelta(minutes=max(10, venue.ticker_interval_sec // 60 * 2))
    past_ref = _price_near(conn, venue_name, venue.reference, now - window, tolerance)
    now_ref = _price_near(conn, venue_name, venue.reference, now, timedelta(minutes=1))
    if not past_ref or not now_ref:
        return []
    ref_return = now_ref / past_ref - 1
    source = f"market:{venue_name}"
    alerts = []
    for symbol in venue.watch_symbols:
        past = _price_near(conn, venue_name, symbol, now - window, tolerance)
        current = _price_near(conn, venue_name, symbol, now, timedelta(minutes=1))
        if not past or not current:
            continue
        ret = current / past - 1
        excess = ret - ref_return
        if abs(excess) * 100 < cfg.anomaly_excess_pct:
            continue
        recent = conn.execute(
            "SELECT 1 FROM alerts WHERE source_id = ? AND message LIKE ? AND created_at >= ?",
            (source, f"{symbol} %",
             to_iso(now - timedelta(hours=cfg.anomaly_cooldown_hours)))).fetchone()
        if recent:
            continue
        alerts.append(Alert(
            level="medium",
            message=(f"{symbol} {ret:+.1%} vs {venue.reference} {ref_return:+.1%} over "
                     f"{cfg.anomaly_window_min}m ({venue_name} {venue.quote}, "
                     f"excess {excess:+.1%})"),
            source_id=source,
        ))
    return alerts


# --- price reactions ----------------------------------------------------------

def _store_candles(conn: sqlite3.Connection, venue: str, candles, now: datetime) -> None:
    with conn:
        for c in candles:
            if c.start_at + timedelta(minutes=CANDLE_MIN) > now:
                continue  # the current hour is not complete yet
            conn.execute(
                "INSERT OR REPLACE INTO candles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (venue, c.market, CANDLE_MIN, to_iso(c.start_at), c.open, c.high, c.low,
                 c.close, c.volume))


def ensure_candles(conn: sqlite3.Connection, client: VenueClient, market: str,
                   t_from: datetime, t_to: datetime, now: datetime) -> None:
    """Make sure completed hourly candles cover [t_from, t_to] in the cache,
    as far as the venue's history allows."""
    t_to = min(t_to, now)
    have = conn.execute(
        """SELECT min(start_at), max(start_at) FROM candles
           WHERE venue = ? AND market = ? AND unit_min = ? AND start_at BETWEEN ? AND ?""",
        (client.name, market, CANDLE_MIN, to_iso(t_from - MAX_CANDLE_GAP),
         to_iso(t_to))).fetchone()
    last_needed = t_to - timedelta(minutes=CANDLE_MIN)
    if (have[0] and from_iso(have[0]) <= t_from
            and from_iso(have[1]) >= last_needed - MAX_CANDLE_GAP):
        return
    cursor = t_to
    for _ in range(10):  # 10 x 200 hours is far more than one event needs
        candles = client.hourly_candles(market, cursor)
        if not candles:
            break
        _store_candles(conn, client.name, candles, now)
        oldest = min(c.start_at for c in candles)
        if not client.pages_backward or oldest <= t_from - MAX_CANDLE_GAP or oldest >= cursor:
            break
        cursor = oldest


def price_at(conn: sqlite3.Connection, venue: str, market: str, when: datetime) -> float | None:
    """Close of the last completed hourly candle at `when`."""
    latest_start = when - timedelta(minutes=CANDLE_MIN)
    row = conn.execute(
        """SELECT close FROM candles WHERE venue = ? AND market = ? AND unit_min = ?
               AND start_at <= ? AND start_at >= ?
           ORDER BY start_at DESC LIMIT 1""",
        (venue, market, CANDLE_MIN, to_iso(latest_start),
         to_iso(latest_start - MAX_CANDLE_GAP))).fetchone()
    return row["close"] if row else None


def compute_reactions(conn: sqlite3.Connection, clients: dict[str, VenueClient],
                      cfg: MarketConfig, listed: dict[str, set[str]], now: datetime,
                      event_ids: list[int] | None = None) -> int:
    """Fill price_reactions for recent events. Returns the number of rows written."""
    query = """SELECT e.id, COALESCE(e.first_published_at, e.first_seen_at) AS t0, a.symbol
               FROM events e JOIN event_assets a ON a.event_id = e.id"""
    if event_ids:
        rows = conn.execute(query + f" WHERE e.id IN ({','.join('?' * len(event_ids))})",
                            event_ids).fetchall()
    else:
        since = to_iso(now - timedelta(days=cfg.reactions_lookback_days))
        rows = conn.execute(
            query + " WHERE COALESCE(e.first_published_at, e.first_seen_at) >= ?",
            (since,)).fetchall()
    written = 0
    for row in rows:
        event_id, symbol, t0 = row["id"], row["symbol"], from_iso(row["t0"])
        venue = cfg.venue_for(symbol)
        client = clients.get(venue.name) if venue else None
        market = client.market_id(symbol, venue.quote) if client else None
        has_market = client is not None and market in listed.get(venue.name, set())
        # no_market is final only while the symbol still has no listed market, so
        # events recorded before a venue was configured for it are measured later.
        final = ("measured",) if has_market else ("measured", "no_market")
        done = {r["window_name"] for r in conn.execute(
            f"""SELECT window_name FROM price_reactions WHERE event_id = ? AND symbol = ?
                   AND status IN ({','.join('?' * len(final))})""",
            (event_id, symbol, *final))}
        todo = [w for w in WINDOWS if w not in done]
        if not todo:
            continue
        if not has_market:
            written += _write(conn, event_id, symbol, todo, t0, now, venue="none",
                              status="no_market")
            continue
        ref_market = client.market_id(venue.reference, venue.quote)
        try:
            span_from = t0 + min(WINDOWS[w][0] for w in todo)
            span_to = t0 + max(WINDOWS[w][1] for w in todo)
            ensure_candles(conn, client, market, span_from, span_to, now)
            ensure_candles(conn, client, ref_market, span_from, span_to, now)
        except FetchError as exc:
            log.warning("candles for %s on %s failed: %s", market, client.name, exc)
            continue
        for name in todo:
            start, end = (t0 + d for d in WINDOWS[name])
            if end > now:
                written += _write(conn, event_id, symbol, [name], t0, now, venue=client.name,
                                  status="pending")
                continue
            prices = [price_at(conn, client.name, m, t)
                      for m in (market, ref_market) for t in (start, end)]
            if None in prices:
                written += _write(conn, event_id, symbol, [name], t0, now, venue=client.name,
                                  status="no_data")
                continue
            asset = prices[1] / prices[0] - 1
            ref = prices[3] / prices[2] - 1
            written += _write(conn, event_id, symbol, [name], t0, now, venue=client.name,
                              status="measured", asset=asset, ref=ref)
    return written


def _write(conn: sqlite3.Connection, event_id: int, symbol: str, windows: list[str],
           t0: datetime, now: datetime, *, venue: str, status: str,
           asset: float | None = None, ref: float | None = None) -> int:
    with conn:
        for name in windows:
            start, end = (t0 + d for d in WINDOWS[name])
            conn.execute(
                """INSERT OR REPLACE INTO price_reactions
                   (event_id, symbol, window_name, venue, t_start, t_end, asset_return,
                    btc_return, excess_return, bucket_median_return, status, computed_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?)""",
                (event_id, symbol, name, venue, to_iso(start), to_iso(end), asset, ref,
                 None if asset is None or ref is None else asset - ref, status, to_iso(now)))
    return len(windows)

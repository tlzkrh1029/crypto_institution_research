"""Market jobs: ticker snapshots with an anomaly check (fast path) and price
reactions around events (slow path). docs/collector-spec.md sections 2 and 5,
docs/research-principles.md section 7.
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
from .upbit import UpbitClient

log = logging.getLogger("collector.market")

VENUE = "upbit"
ALERT_SOURCE = "market:upbit"
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
class MarketConfig:
    enabled: bool
    terms_checked: str
    quote: str
    symbols: tuple[str, ...]
    reference: str
    ticker_interval_sec: int
    anomaly_window_min: int
    anomaly_excess_pct: float
    anomaly_cooldown_hours: int
    reactions_interval_sec: int
    reactions_lookback_days: int

    def market(self, symbol: str) -> str:
        return f"{self.quote}-{symbol}"


def load_market_config(path: Path) -> MarketConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    upbit = raw.get("upbit", {})
    anomaly = raw.get("anomaly", {})
    reactions = raw.get("reactions", {})
    if upbit.get("enabled", False) and not upbit.get("terms_checked"):
        raise ConfigError("market.yaml: upbit.terms_checked is required")
    cfg = MarketConfig(
        enabled=bool(upbit.get("enabled", False)),
        terms_checked=str(upbit.get("terms_checked", "")),
        quote=upbit.get("quote", "KRW"),
        symbols=tuple(upbit.get("symbols", [])),
        reference=upbit.get("reference", "BTC"),
        ticker_interval_sec=int(upbit.get("ticker_interval_sec", 300)),
        anomaly_window_min=int(anomaly.get("window_minutes", 60)),
        anomaly_excess_pct=float(anomaly.get("excess_return_pct", 5.0)),
        anomaly_cooldown_hours=int(anomaly.get("cooldown_hours", 6)),
        reactions_interval_sec=int(reactions.get("interval_sec", 1800)),
        reactions_lookback_days=int(reactions.get("lookback_days", 30)),
    )
    if cfg.ticker_interval_sec < 60 or cfg.reactions_interval_sec < 300:
        raise ConfigError("market.yaml: intervals are too short")
    return cfg


# --- tickers and anomalies ---------------------------------------------------

def poll_tickers(conn: sqlite3.Connection, client: UpbitClient, cfg: MarketConfig,
                 listed: set[str], now: datetime) -> list[Alert]:
    symbols = [s for s in (cfg.reference, *cfg.symbols) if cfg.market(s) in listed]
    tickers = client.tickers([cfg.market(s) for s in symbols])
    with conn:
        for t in tickers:
            conn.execute(
                "INSERT OR REPLACE INTO market_snapshots VALUES (?, ?, ?, ?, ?, ?)",
                (VENUE, t.market.split("-", 1)[1], cfg.quote, to_iso(now), t.price,
                 t.acc_trade_value_24h))
    return _anomalies(conn, cfg, now)


def _price_near(conn: sqlite3.Connection, symbol: str, target: datetime,
                tolerance: timedelta) -> float | None:
    row = conn.execute(
        """SELECT price FROM market_snapshots WHERE venue = ? AND symbol = ?
               AND ts BETWEEN ? AND ?
           ORDER BY abs(julianday(ts) - julianday(?)) LIMIT 1""",
        (VENUE, symbol, to_iso(target - tolerance), to_iso(target + tolerance),
         to_iso(target))).fetchone()
    return row["price"] if row else None


def _anomalies(conn: sqlite3.Connection, cfg: MarketConfig, now: datetime) -> list[Alert]:
    window = timedelta(minutes=cfg.anomaly_window_min)
    tolerance = timedelta(minutes=max(10, cfg.ticker_interval_sec // 60 * 2))
    past_ref = _price_near(conn, cfg.reference, now - window, tolerance)
    now_ref = _price_near(conn, cfg.reference, now, timedelta(minutes=1))
    if not past_ref or not now_ref:
        return []
    ref_return = now_ref / past_ref - 1
    alerts = []
    for symbol in cfg.symbols:
        past = _price_near(conn, symbol, now - window, tolerance)
        current = _price_near(conn, symbol, now, timedelta(minutes=1))
        if not past or not current:
            continue
        ret = current / past - 1
        excess = ret - ref_return
        if abs(excess) * 100 < cfg.anomaly_excess_pct:
            continue
        recent = conn.execute(
            """SELECT 1 FROM alerts WHERE source_id = ? AND message LIKE ? AND created_at >= ?""",
            (ALERT_SOURCE, f"{symbol} %",
             to_iso(now - timedelta(hours=cfg.anomaly_cooldown_hours)))).fetchone()
        if recent:
            continue
        alerts.append(Alert(
            level="medium",
            message=(f"{symbol} {ret:+.1%} vs {cfg.reference} {ref_return:+.1%} over "
                     f"{cfg.anomaly_window_min}m (Upbit {cfg.quote}, excess {excess:+.1%})"),
            source_id=ALERT_SOURCE,
        ))
    return alerts


# --- price reactions ----------------------------------------------------------

def _store_candles(conn: sqlite3.Connection, candles, now: datetime) -> None:
    with conn:
        for c in candles:
            if c.start_at + timedelta(minutes=CANDLE_MIN) > now:
                continue  # the current hour is not complete yet
            conn.execute(
                "INSERT OR REPLACE INTO candles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (VENUE, c.market, CANDLE_MIN, to_iso(c.start_at), c.open, c.high, c.low,
                 c.close, c.volume))


def ensure_candles(conn: sqlite3.Connection, client: UpbitClient, market: str,
                   t_from: datetime, t_to: datetime, now: datetime) -> None:
    """Make sure completed hourly candles cover [t_from, t_to] in the cache."""
    t_to = min(t_to, now)
    have = conn.execute(
        """SELECT min(start_at), max(start_at) FROM candles
           WHERE venue = ? AND market = ? AND unit_min = ? AND start_at BETWEEN ? AND ?""",
        (VENUE, market, CANDLE_MIN, to_iso(t_from - MAX_CANDLE_GAP), to_iso(t_to))).fetchone()
    last_needed = t_to - timedelta(minutes=CANDLE_MIN)
    if have[0] and from_iso(have[0]) <= t_from and from_iso(have[1]) >= last_needed - MAX_CANDLE_GAP:
        return
    cursor = t_to
    for _ in range(10):  # 10 x 200 hours is far more than one event needs
        candles = client.hourly_candles(market, cursor)
        if not candles:
            break
        _store_candles(conn, candles, now)
        oldest = min(c.start_at for c in candles)
        if oldest <= t_from - MAX_CANDLE_GAP:
            break
        cursor = oldest


def price_at(conn: sqlite3.Connection, market: str, when: datetime) -> float | None:
    """Close of the last completed hourly candle at `when`."""
    latest_start = when - timedelta(minutes=CANDLE_MIN)
    row = conn.execute(
        """SELECT close FROM candles WHERE venue = ? AND market = ? AND unit_min = ?
               AND start_at <= ? AND start_at >= ?
           ORDER BY start_at DESC LIMIT 1""",
        (VENUE, market, CANDLE_MIN, to_iso(latest_start),
         to_iso(latest_start - MAX_CANDLE_GAP))).fetchone()
    return row["close"] if row else None


def compute_reactions(conn: sqlite3.Connection, client: UpbitClient, cfg: MarketConfig,
                      listed: set[str], now: datetime,
                      event_ids: list[int] | None = None) -> int:
    """Fill price_reactions for recent events. Returns the number of rows written."""
    query = """SELECT e.id, COALESCE(e.first_published_at, e.first_seen_at) AS t0, a.symbol
               FROM events e JOIN event_assets a ON a.event_id = e.id"""
    if event_ids:
        rows = conn.execute(query + f" WHERE e.id IN ({','.join('?' * len(event_ids))})",
                            event_ids).fetchall()
    else:
        since = to_iso(now - timedelta(days=cfg.reactions_lookback_days))
        rows = conn.execute(query + " WHERE COALESCE(e.first_published_at, e.first_seen_at) >= ?",
                            (since,)).fetchall()
    written = 0
    ref_market = cfg.market(cfg.reference)
    for row in rows:
        event_id, symbol, t0 = row["id"], row["symbol"], from_iso(row["t0"])
        done = {r["window_name"] for r in conn.execute(
            """SELECT window_name FROM price_reactions WHERE event_id = ? AND symbol = ?
                   AND status IN ('measured', 'no_market')""", (event_id, symbol))}
        todo = [w for w in WINDOWS if w not in done]
        if not todo:
            continue
        market = cfg.market(symbol)
        if market not in listed:
            written += _write(conn, event_id, symbol, todo, t0, now, status="no_market")
            continue
        try:
            span_from = t0 + min(WINDOWS[w][0] for w in todo)
            span_to = t0 + max(WINDOWS[w][1] for w in todo)
            ensure_candles(conn, client, market, span_from, span_to, now)
            ensure_candles(conn, client, ref_market, span_from, span_to, now)
        except FetchError as exc:
            log.warning("candles for %s failed: %s", market, exc)
            continue
        for name in todo:
            start, end = (t0 + d for d in WINDOWS[name])
            if end > now:
                written += _write(conn, event_id, symbol, [name], t0, now, status="pending")
                continue
            prices = [price_at(conn, m, t) for m in (market, ref_market) for t in (start, end)]
            if None in prices:
                written += _write(conn, event_id, symbol, [name], t0, now, status="no_data")
                continue
            asset = prices[1] / prices[0] - 1
            ref = prices[3] / prices[2] - 1
            written += _write(conn, event_id, symbol, [name], t0, now, status="measured",
                              asset=asset, ref=ref)
    return written


def _write(conn: sqlite3.Connection, event_id: int, symbol: str, windows: list[str],
           t0: datetime, now: datetime, *, status: str, asset: float | None = None,
           ref: float | None = None) -> int:
    with conn:
        for name in windows:
            start, end = (t0 + d for d in WINDOWS[name])
            conn.execute(
                """INSERT OR REPLACE INTO price_reactions
                   (event_id, symbol, window_name, venue, t_start, t_end, asset_return,
                    btc_return, excess_return, bucket_median_return, status, computed_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?)""",
                (event_id, symbol, name, VENUE, to_iso(start), to_iso(end), asset, ref,
                 None if asset is None or ref is None else asset - ref, status, to_iso(now)))
    return len(windows)

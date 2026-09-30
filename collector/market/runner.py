"""Schedules the market jobs inside the collector's run loop.

Every ticker poll is recorded in the runs table as source 'market:<venue>'
(status ok or error, items_seen = tickers stored), so `collector report` and
`collector status` show market failures next to the news sources. Prices are
never written to runs.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from ..fetch import FetchError
from ..pipeline import Context, deliver_alert
from ..timeutil import to_iso
from .base import VenueClient
from .jobs import MarketConfig, compute_reactions, poll_tickers
from .kraken import KrakenClient
from .upbit import UpbitClient

log = logging.getLogger("collector.market")
LISTING_REFRESH = timedelta(hours=24)
CLIENTS = {"upbit": UpbitClient, "kraken": KrakenClient}
RUN_SOURCE_PREFIX = "market:"
ERROR_CHARS = 500


def run_source_id(venue: str) -> str:
    return f"{RUN_SOURCE_PREFIX}{venue}"


def make_clients(cfg: MarketConfig, user_agent: str) -> dict[str, VenueClient]:
    clients = {}
    for venue in cfg.enabled_venues:
        if venue.name not in CLIENTS:
            raise ValueError(f"no client for market venue {venue.name!r}")
        clients[venue.name] = CLIENTS[venue.name](user_agent)
    return clients


class MarketRunner:
    def __init__(self, ctx: Context, cfg: MarketConfig, clients: dict[str, VenueClient]):
        self.ctx = ctx
        self.cfg = cfg
        self.clients = clients
        self._listed: dict[str, set[str]] = {}
        self._listed_at: dict[str, datetime] = {}
        self.next_ticker: dict[str, datetime] = {}
        self.next_reactions: datetime | None = None

    def listed(self, venue: str, now: datetime) -> set[str]:
        if venue not in self._listed or now - self._listed_at[venue] > LISTING_REFRESH:
            client = self.clients[venue]
            self._listed[venue] = client.markets()
            self._listed_at[venue] = now
            vcfg = next(v for v in self.cfg.venues if v.name == venue)
            missing = [s for s in vcfg.symbols
                       if client.market_id(s, vcfg.quote) not in self._listed[venue]]
            if missing:
                log.info("not listed on %s %s: %s", venue, vcfg.quote, ", ".join(missing))
        return self._listed[venue]

    def run_tickers(self, venue_name: str, now: datetime) -> int:
        venue = next(v for v in self.cfg.venues if v.name == venue_name)
        try:
            alerts = poll_tickers(self.ctx.conn, self.clients[venue_name], venue, self.cfg,
                                  self.listed(venue_name, now), now)
        except Exception as exc:
            error = str(exc) if isinstance(exc, FetchError) else f"{type(exc).__name__}: {exc}"
            self._record_run(venue_name, now, "error", error=error)
            raise
        stored = self.ctx.conn.execute(
            "SELECT COUNT(*) FROM market_snapshots WHERE venue = ? AND ts = ?",
            (venue_name, to_iso(now))).fetchone()[0]
        self._record_run(venue_name, now, "ok", items_seen=stored)
        for alert in alerts:
            deliver_alert(self.ctx, alert, now)
        return len(alerts)

    def _record_run(self, venue_name: str, now: datetime, status: str, *,
                    items_seen: int = 0, error: str | None = None) -> None:
        with self.ctx.conn:
            self.ctx.conn.execute(
                """INSERT INTO runs (source_id, started_at, finished_at, status, items_seen,
                                     error) VALUES (?, ?, ?, ?, ?, ?)""",
                (run_source_id(venue_name), to_iso(now), to_iso(now), status, items_seen,
                 error[:ERROR_CHARS] if error else None))

    def run_reactions(self, now: datetime, event_ids: list[int] | None = None) -> int:
        listed = {}
        for name in self.clients:
            try:
                listed[name] = self.listed(name, now)
            except FetchError as exc:
                log.warning("%s market list: %s", name, exc)
        return compute_reactions(self.ctx.conn, self.clients, self.cfg, listed, now, event_ids)

    def tick(self, now: datetime) -> None:
        for venue in self.cfg.enabled_venues:
            due = self.next_ticker.get(venue.name)
            if due is None or now >= due:
                self.next_ticker[venue.name] = now + timedelta(seconds=venue.ticker_interval_sec)
                # One failing venue must not stop the other venues or the reactions.
                try:
                    self.run_tickers(venue.name, now)
                except FetchError as exc:
                    log.warning("%s tickers: %s", venue.name, exc)
                except Exception:
                    log.exception("unexpected error in %s tickers", venue.name)
        if self.clients and (self.next_reactions is None or now >= self.next_reactions):
            self.next_reactions = now + timedelta(seconds=self.cfg.reactions_interval_sec)
            try:
                written = self.run_reactions(now)
                log.info("price reactions updated: %d rows", written)
            except FetchError as exc:
                log.warning("price reactions: %s", exc)

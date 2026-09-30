"""Schedules the market jobs inside the collector's run loop."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from ..fetch import FetchError
from ..pipeline import Context, deliver_alert
from .jobs import MarketConfig, compute_reactions, poll_tickers
from .upbit import UpbitClient

log = logging.getLogger("collector.market")
LISTING_REFRESH = timedelta(hours=24)


class MarketRunner:
    def __init__(self, ctx: Context, cfg: MarketConfig, client: UpbitClient):
        self.ctx = ctx
        self.cfg = cfg
        self.client = client
        self._listed: set[str] | None = None
        self._listed_at: datetime | None = None
        self.next_ticker: datetime | None = None
        self.next_reactions: datetime | None = None

    def listed(self, now: datetime) -> set[str]:
        if self._listed is None or now - self._listed_at > LISTING_REFRESH:
            self._listed = self.client.markets()
            self._listed_at = now
            missing = [s for s in self.cfg.symbols if self.cfg.market(s) not in self._listed]
            if missing:
                log.info("not listed on Upbit %s: %s", self.cfg.quote, ", ".join(missing))
        return self._listed

    def run_tickers(self, now: datetime) -> int:
        alerts = poll_tickers(self.ctx.conn, self.client, self.cfg, self.listed(now), now)
        for alert in alerts:
            deliver_alert(self.ctx, alert, now)
        return len(alerts)

    def run_reactions(self, now: datetime, event_ids: list[int] | None = None) -> int:
        return compute_reactions(self.ctx.conn, self.client, self.cfg, self.listed(now), now,
                                 event_ids)

    def tick(self, now: datetime) -> None:
        if not self.cfg.enabled:
            return
        if self.next_ticker is None or now >= self.next_ticker:
            self.next_ticker = now + timedelta(seconds=self.cfg.ticker_interval_sec)
            try:
                self.run_tickers(now)
            except FetchError as exc:
                log.warning("upbit tickers: %s", exc)
        if self.next_reactions is None or now >= self.next_reactions:
            self.next_reactions = now + timedelta(seconds=self.cfg.reactions_interval_sec)
            try:
                written = self.run_reactions(now)
                log.info("price reactions updated: %d rows", written)
            except FetchError as exc:
                log.warning("price reactions: %s", exc)

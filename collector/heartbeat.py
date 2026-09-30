"""Optional ping to an external monitor, so a stopped collector is noticed.

The ping URL is a credential: keep it in .env (AGENTS.md).
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

import requests

log = logging.getLogger("collector.heartbeat")


class Heartbeat:
    def __init__(self, url: str, user_agent: str, min_interval: timedelta = timedelta(minutes=5),
                 session: requests.Session | None = None):
        self.url = url
        self.user_agent = user_agent
        self.min_interval = min_interval
        self.session = session or requests.Session()
        self.last_sent: datetime | None = None

    def beat(self, now: datetime) -> bool:
        if not self.url:
            return False
        if self.last_sent is not None and now - self.last_sent < self.min_interval:
            return False
        try:
            self.session.get(self.url, headers={"User-Agent": self.user_agent}, timeout=10)
        except requests.RequestException as exc:
            # Never log the URL itself.
            log.warning("heartbeat failed: %s", type(exc).__name__)
            return False
        self.last_sent = now
        return True

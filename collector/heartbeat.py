"""Optional ping to an external monitor, so a stopped collector is noticed.

The ping URL is a credential: keep it in .env (AGENTS.md). It is registered
with collector.fetch.register_secret_url so urllib3's log lines omit it.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta

import requests

from .fetch import CONNECT_TIMEOUT_SEC, IdleReset, make_session, register_secret_url

log = logging.getLogger("collector.heartbeat")


class Heartbeat:
    def __init__(self, url: str, user_agent: str, min_interval: timedelta = timedelta(minutes=5),
                 session: requests.Session | None = None, clock=time.time):
        register_secret_url(url)
        self.url = url
        self.user_agent = user_agent
        self.min_interval = min_interval
        self.session = session or make_session()
        self.idle = IdleReset(self.session, clock)
        self.last_sent: datetime | None = None

    def beat(self, now: datetime) -> bool:
        if not self.url:
            return False
        if self.last_sent is not None and now - self.last_sent < self.min_interval:
            return False
        self.idle.before(self.url)
        try:
            self.session.get(self.url, headers={"User-Agent": self.user_agent},
                             timeout=(CONNECT_TIMEOUT_SEC, 10))
        except requests.RequestException as exc:
            # Never log the URL itself.
            log.warning("heartbeat failed: %s", type(exc).__name__)
            return False
        finally:
            self.idle.used(self.url)
        self.last_sent = now
        return True

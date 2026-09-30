"""Alert delivery. Only a log notifier exists until the channel is decided
(docs/open-questions.md Q3)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

log = logging.getLogger("collector.alert")


@dataclass(frozen=True)
class Alert:
    level: str
    message: str
    url: str | None = None
    event_id: int | None = None
    source_id: str | None = None


class Notifier(Protocol):
    name: str

    def send(self, alert: Alert) -> bool: ...


class LogNotifier:
    name = "log"

    def send(self, alert: Alert) -> bool:
        log.warning("[%s] %s %s", alert.level.upper(), alert.message, alert.url or "")
        return True


def make_notifier(name: str) -> Notifier:
    if name == "log":
        return LogNotifier()
    raise ValueError(f"unknown notifier {name!r}; only 'log' is available (open-questions Q3)")

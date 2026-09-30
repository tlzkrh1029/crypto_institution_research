from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from collector import db
from collector.config import Settings, SourceConfig, load_entities
from collector.fetch import FetchError, FetchResult
from collector.notify import Alert
from collector.pipeline import Context, sync_sources

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"


class FakeFetcher:
    """Returns canned responses per URL; records the headers it was asked for."""

    def __init__(self):
        self.responses: dict[str, object] = {}
        self.calls: list[dict] = []

    def set(self, url: str, content: bytes | None = None, *, status: int = 200,
            etag: str | None = None, error: FetchError | None = None) -> None:
        self.responses[url] = error or FetchResult(status, content, etag, None)

    def get(self, url, *, etag=None, last_modified=None, user_agent=None):
        self.calls.append({"url": url, "etag": etag, "user_agent": user_agent})
        response = self.responses[url]
        if isinstance(response, FetchError):
            raise response
        return response


class RecordingNotifier:
    name = "test"

    def __init__(self):
        self.alerts: list[Alert] = []

    def send(self, alert: Alert) -> bool:
        self.alerts.append(alert)
        return True


class Clock:
    def __init__(self, now: datetime):
        self.now = now

    def __call__(self) -> datetime:
        return self.now


def make_source(sid: str, url: str, kind: str = "feed", publisher_kind: str = "newswire",
                **extra) -> SourceConfig:
    return SourceConfig(id=sid, name=sid, kind=kind, url=url, interval_sec=300,
                        publisher_kind=publisher_kind, terms_checked="test", **extra)


@pytest.fixture
def entities():
    return load_entities(ROOT / "config" / "entities.yaml")


@pytest.fixture
def harness(entities, tmp_path):
    conn = db.connect(":memory:")
    settings = Settings(root=tmp_path, user_agent="test-agent", sec_user_agent="",
                        heartbeat_url="", data_dir=tmp_path, notifier="log")
    fetcher = FakeFetcher()
    notifier = RecordingNotifier()
    clock = Clock(datetime(2026, 9, 25, 0, 0, tzinfo=timezone.utc))
    ctx = Context(settings=settings, conn=conn, fetcher=fetcher, entities=entities,
                  notifier=notifier, clock=clock)

    def register(*sources: SourceConfig) -> None:
        sync_sources(conn, list(sources))

    return ctx, fetcher, notifier, clock, register

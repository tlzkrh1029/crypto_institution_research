"""HTTP access rules (docs/collector-spec.md section 4).

- A descriptive User-Agent; never a browser impersonation.
- Conditional requests (ETag / If-Modified-Since).
- Failures raise FetchError; the scheduler applies backoff.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests

TIMEOUT_SEC = 20


class FetchError(Exception):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


@dataclass(frozen=True)
class FetchResult:
    status: int
    content: bytes | None
    etag: str | None
    last_modified: str | None

    @property
    def not_modified(self) -> bool:
        return self.status == 304


class Fetcher:
    def __init__(self, user_agent: str, session: requests.Session | None = None):
        self.user_agent = user_agent
        self.session = session or requests.Session()

    def get(self, url: str, *, etag: str | None = None, last_modified: str | None = None,
            user_agent: str | None = None) -> FetchResult:
        headers = {"User-Agent": user_agent or self.user_agent,
                   "Accept-Encoding": "gzip, deflate"}
        if etag:
            headers["If-None-Match"] = etag
        if last_modified:
            headers["If-Modified-Since"] = last_modified
        try:
            resp = self.session.get(url, headers=headers, timeout=TIMEOUT_SEC)
        except requests.RequestException as exc:
            raise FetchError(f"{type(exc).__name__}: {exc}") from exc
        if resp.status_code == 304:
            return FetchResult(304, None, etag, last_modified)
        if resp.status_code != 200:
            raise FetchError(f"HTTP {resp.status_code}", resp.status_code)
        return FetchResult(
            200,
            resp.content,
            resp.headers.get("ETag"),
            resp.headers.get("Last-Modified"),
        )

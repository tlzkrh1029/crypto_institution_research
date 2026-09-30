"""HTTP access rules (docs/collector-spec.md section 4).

- A descriptive User-Agent; never a browser impersonation.
- Conditional requests (ETag / If-Modified-Since).
- Failures raise FetchError; the scheduler applies backoff.

Connection handling, shared by every HTTP client in the collector (feeds,
market venues, Telegram, heartbeat):

- A home router or ISP NAT can forget an idle keep-alive connection without
  telling either end. The next request on it then fails with a connection
  reset or a read timeout, and the scheduler's retry on a new connection
  succeeds, which shows up as alternating ok/error runs. IdleReset drops the
  pooled connections before a host that sat idle longer than IDLE_RESET_SEC
  is used again. Requests in a burst (Kraken's calls 1.1 s apart) still share
  one connection.
- make_session() mounts a small urllib3 Retry: a TCP connect that fails or
  times out is retried for any method (the request was not sent); a
  connection that breaks after the request went out (reset, closed) only for
  GET and HEAD; read timeouts, other errors (SSLError, ProxyError) and HTTP
  status codes never. The caller's own schedule handles those: news feeds
  back off in the scheduler, market venues wait for the next ticker poll,
  undelivered alerts are sent again every 5 minutes.
- The TLS handshake of a new connection gets its own CONNECT_TIMEOUT_SEC,
  like the TCP connect, but urllib3 (1.26 and 2.x) does not report its
  failures as connect errors. A handshake timeout is a read timeout that
  carries the connect value ("read timeout=10"): it is not retried, and
  describe_error marks it "(TLS handshake)" so it is not mistaken for a
  server that took the request and did not answer. A reset during the
  handshake is a ProtocolError, retried only for GET and HEAD; a TLS error is
  an SSLError, never retried.
- Connect and read timeouts are separate (CONNECT_TIMEOUT_SEC, TIMEOUT_SEC),
  so a host that never accepts costs three connect timeouts, not three read
  timeouts.
- At this layer a Telegram POST that may have reached Telegram is not sent
  again. The alert then stays undelivered, and pipeline.retry_undelivered
  sends it again 5 minutes later, so a rare duplicate alert is possible.
- Secrets that end up in request URLs (the Telegram bot token, the heartbeat
  ping URL) are registered with register_secret(), and SECRET_FILTER removes
  them from log records, including urllib3's own "Retrying ..." warnings.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlsplit

import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import (ConnectTimeoutError, MaxRetryError, NewConnectionError,
                                ReadTimeoutError)
from urllib3.util.retry import Retry

TIMEOUT_SEC = 20
CONNECT_TIMEOUT_SEC = 10   # TCP connect, and separately the TLS handshake
IDLE_RESET_SEC = 60
RETRY_TOTAL = 2
RETRY_BACKOFF_FACTOR = 0.5
RETRY_METHODS = frozenset({"GET", "HEAD"})

REDACTED = "<redacted>"
MIN_SECRET_CHARS = 8
URLLIB3_LOGGERS = ("urllib3", "urllib3.connectionpool", "urllib3.connection",
                   "urllib3.poolmanager", "urllib3.response", "urllib3.util.retry")


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


# --- sessions ------------------------------------------------------------------

class CollectorRetry(Retry):
    """urllib3's Retry, except that a read timeout is never retried.

    A read timeout means the server took the request and did not answer in
    time. Asking again would multiply how long the single-threaded run loop
    waits, and how often a slow server is hit. A stale pooled connection can
    also end in a read timeout (a middlebox that drops packets); IdleReset
    closes those before they are used.
    """

    def increment(self, method=None, url=None, response=None, error=None, _pool=None,
                  _stacktrace=None):
        if isinstance(error, ReadTimeoutError):
            raise error
        try:
            return super().increment(method, url, response, error, _pool, _stacktrace)
        except MaxRetryError as exc:
            # For describe_error: an "other" error (SSLError) gives up at once.
            exc.attempts = len(self.history) + 1
            raise


def make_retry() -> Retry:
    # `other=0` and `allowed_methods` need urllib3 >= 1.26 (pyproject.toml): older
    # versions retry any other error, such as an SSLError, even for a POST.
    return CollectorRetry(total=RETRY_TOTAL, connect=RETRY_TOTAL, read=RETRY_TOTAL, status=0,
                          other=0, backoff_factor=RETRY_BACKOFF_FACTOR,
                          raise_on_status=False, allowed_methods=RETRY_METHODS)


def make_session() -> requests.Session:
    """A Session with the collector's retry policy mounted for http and https."""
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=make_retry())
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _origin(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}".lower()


class IdleReset:
    """Closes a session's pooled connections before reusing a host that sat idle.

    Idle time is tracked per host, because one session (the Fetcher's) serves
    several hosts on different schedules. Closing drops every pooled
    connection of the session; the session itself stays usable. Sessions
    without close() (test doubles) are left alone.

    The default clock is wall-clock time: the monotonic clock stops while the
    machine sleeps (macOS and Linux), but a NAT entry keeps expiring.
    """

    def __init__(self, session, clock: Callable[[], float] = time.time,
                 idle_sec: float | None = None):
        self.session = session
        self._clock = clock
        self._idle_sec = idle_sec
        self._last_used: dict[str, float] = {}
        self.resets = 0

    @property
    def idle_sec(self) -> float:
        return IDLE_RESET_SEC if self._idle_sec is None else self._idle_sec

    def before(self, url: str) -> None:
        last = self._last_used.get(_origin(url))
        if last is None or self._clock() - last <= self.idle_sec:
            return
        close = getattr(self.session, "close", None)
        if callable(close):
            close()
        self._last_used.clear()   # no host has a pooled connection any more
        self.resets += 1

    def used(self, *urls: str | None) -> None:
        now = self._clock()
        for url in urls:
            if isinstance(url, str) and url:
                self._last_used[_origin(url)] = now


def _reason_text(reason: Exception) -> str:
    """A urllib3 connection error without the connection's repr in front, so the
    errno text ("Connection refused", "Network is unreachable") comes first."""
    if isinstance(reason, NewConnectionError):   # "<connection>: <message>"
        return str(reason).split(": ", 1)[-1]
    if (isinstance(reason, ConnectTimeoutError) and len(reason.args) == 2
            and isinstance(reason.args[1], str)):   # (connection, message)
        return reason.args[1]
    return str(reason)


def describe_error(exc: requests.RequestException,
                   timeout: tuple[float, float] | None = None) -> str:
    """Error text for logs and the runs table.

    The report cuts long errors (report.ERROR_CHARS), so the cause comes first.
    When urllib3 gives up, requests wraps its MaxRetryError, whose text starts
    with the pool and URL; the text is then "<type> (<n> attempts): <cause
    type>: <cause>", with n from CollectorRetry (1 when the policy did not
    retry, as for an SSLError). `timeout` is the (connect, read) pair of the
    request: a read timeout that carries the connect value happened during the
    TLS handshake and is marked so.
    """
    inner = exc.args[0] if exc.args else None
    if isinstance(inner, MaxRetryError) and inner.reason is not None:
        attempts = getattr(inner, "attempts", None)
        marker = f" ({attempts} attempt{'' if attempts == 1 else 's'})" if attempts else ""
        return (f"{type(exc).__name__}{marker}: {type(inner.reason).__name__}: "
                f"{_reason_text(inner.reason)}")
    if (isinstance(exc, requests.ReadTimeout) and timeout and timeout[0] != timeout[1]
            and str(exc).endswith(f"(read timeout={timeout[0]})")):
        return f"{type(exc).__name__} (TLS handshake): {exc}"
    return f"{type(exc).__name__}: {exc}"


# --- secrets in logs -------------------------------------------------------------

_SECRETS: set[str] = set()


def redact(text: str) -> str:
    for secret in sorted(_SECRETS, key=len, reverse=True):
        text = text.replace(secret, REDACTED)
    return text


class SecretFilter(logging.Filter):
    """Replaces registered secrets in a record's message and traceback."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not _SECRETS:
            return True
        try:
            message = record.getMessage()
        except Exception:  # a broken format string is not ours to fix here
            return True
        clean = redact(message)
        if clean != message:
            record.msg, record.args = clean, ()
        if record.exc_info and not record.exc_text:
            record.exc_text = logging.Formatter().formatException(record.exc_info)
        if record.exc_text:
            record.exc_text = redact(record.exc_text)
        return True


SECRET_FILTER = SecretFilter()


def register_secret(*values: str | None) -> None:
    """Keep these values out of log records (urllib3 logs request paths)."""
    for value in values:
        if value and len(value) >= MIN_SECRET_CHARS:
            _SECRETS.add(value)
    for name in URLLIB3_LOGGERS:
        logging.getLogger(name).addFilter(SECRET_FILTER)   # no-op if already there


def register_secret_url(url: str | None) -> None:
    """A secret URL: urllib3 logs only its path and query, so register those too."""
    if not url:
        return
    parts = urlsplit(url)
    path = parts.path + (f"?{parts.query}" if parts.query else "")
    register_secret(url, path)


# --- feeds -----------------------------------------------------------------------

class Fetcher:
    def __init__(self, user_agent: str, session: requests.Session | None = None,
                 clock: Callable[[], float] = time.time):
        self.user_agent = user_agent
        self.session = session or make_session()
        self.idle = IdleReset(self.session, clock)

    def get(self, url: str, *, etag: str | None = None, last_modified: str | None = None,
            user_agent: str | None = None) -> FetchResult:
        headers = {"User-Agent": user_agent or self.user_agent,
                   "Accept-Encoding": "gzip, deflate"}
        if etag:
            headers["If-None-Match"] = etag
        if last_modified:
            headers["If-Modified-Since"] = last_modified
        self.idle.before(url)
        resp = None
        timeout = (CONNECT_TIMEOUT_SEC, TIMEOUT_SEC)
        try:
            resp = self.session.get(url, headers=headers, timeout=timeout)
        except requests.RequestException as exc:
            raise FetchError(describe_error(exc, timeout)) from exc
        finally:
            # A redirect may have pooled a connection to another host.
            self.idle.used(url, getattr(resp, "url", None))
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

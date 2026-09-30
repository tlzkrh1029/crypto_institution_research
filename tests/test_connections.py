"""Stale keep-alive connections and the retry policy (collector/fetch.py).

An in-process middlebox stands between the client and a keep-alive HTTP
server, like a home router or ISP NAT. Its forget() stands in for the
router's idle timer running out: it drops every open connection's mapping
without telling the client. In "rst" mode the client's next data gets a
reset; in "blackhole" mode it is swallowed and the client runs into its read
timeout. The idle time itself is a fake clock given to Fetcher, so no test
depends on how fast threads are scheduled. Everything runs on 127.0.0.1; env
proxies are bypassed.
"""

from __future__ import annotations

import logging
import select
import socket
import struct
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
import requests
from urllib3.connection import HTTPSConnection
from urllib3.exceptions import (ConnectTimeoutError, MaxRetryError, ProtocolError, ProxyError,
                                ReadTimeoutError, SSLError)

from collector import fetch, notify, report
from collector.fetch import FetchError, Fetcher, make_session
from collector.heartbeat import Heartbeat
from collector.market.kraken import KrakenClient
from collector.market.upbit import UpbitClient
from collector.notify import Alert, TelegramNotifier

HUNG_SEC = 2        # a request through the middlebox that takes longer has hung
TOKEN = "123456:CONN-TEST-secret-token"
UA = "collector-test/0.1"


_OPEN: list[requests.Session] = []


@pytest.fixture(autouse=True)
def bypass_env_proxies(monkeypatch):
    for name in ("NO_PROXY", "no_proxy"):
        monkeypatch.setenv(name, "127.0.0.1,localhost")
    yield
    while _OPEN:
        _OPEN.pop().close()


@pytest.fixture(autouse=True)
def isolated_secrets(monkeypatch):
    """No secret registered and no SECRET_FILTER on urllib3's loggers when a test
    starts, so a redaction test proves that the client under test registered its
    own secret. The loggers' previous state is restored afterwards."""
    monkeypatch.setattr(fetch, "_SECRETS", set())
    loggers = [logging.getLogger(name) for name in fetch.URLLIB3_LOGGERS]
    had_filter = [lg for lg in loggers if fetch.SECRET_FILTER in lg.filters]
    for lg in loggers:
        lg.removeFilter(fetch.SECRET_FILTER)
    yield
    for lg in loggers:
        lg.removeFilter(fetch.SECRET_FILTER)
    for lg in had_filter:
        lg.addFilter(fetch.SECRET_FILTER)


def local(session):
    """No env proxies, netrc or CA bundles for a test session; closed after the test."""
    session.trust_env = False
    _OPEN.append(session)
    return session


def closed_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


# --- keep-alive upstream ------------------------------------------------------------

class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"   # keep-alive

    def setup(self):
        super().setup()
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def do_GET(self):  # noqa: N802
        self.server.hits += 1
        status, body = self.server.status, b"<rss version='2.0'><channel/></rss>"
        self.send_response(status)
        if status == 503:
            self.send_header("Retry-After", "30")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):  # noqa: N802
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.server.hits += 1
        body = b'{"ok": true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class Upstream(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, status: int = 200):
        super().__init__(("127.0.0.1", 0), _Handler)
        self.status = status
        self.hits = 0
        threading.Thread(target=self.serve_forever, kwargs={"poll_interval": 0.05},
                         daemon=True).start()

    def handle_error(self, request, client_address):
        pass   # the middlebox tears connections down on purpose

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


# --- middlebox ------------------------------------------------------------------------

def _rst_close(sock: socket.socket) -> None:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    sock.close()


class _Relay:
    """One client connection through the middlebox."""

    def __init__(self, client: socket.socket):
        self.client = client
        self.forget = threading.Event()      # forget() asked for it
        self.forgotten = threading.Event()   # upstream dropped, or the relay ended


class Middlebox:
    def __init__(self, upstream_port: int, mode: str):
        assert mode in ("rst", "blackhole")
        self.upstream_port = upstream_port
        self.mode = mode
        self.accepted = 0
        self.events: list[str] = []
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._sockets: list[socket.socket] = []
        self._relays: list[_Relay] = []
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind(("127.0.0.1", 0))
        self.lsock.listen(8)
        self.lsock.settimeout(0.05)
        threading.Thread(target=self._accept, daemon=True).start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.lsock.getsockname()[1]}"

    def forget(self) -> None:
        """Drop the mapping of every open connection now, as a router's idle timer
        does, without telling the client. Returns once every relay has done it."""
        with self._lock:
            relays = list(self._relays)
        for relay in relays:
            relay.forget.set()
        for relay in relays:
            assert relay.forgotten.wait(HUNG_SEC), "the middlebox did not forget"

    def stale_hits(self) -> int:
        """Requests the client sent on a connection the middlebox had forgotten."""
        return sum("forgotten" in e for e in self.events)

    def wait_for_stale_hits(self, n: int) -> int:
        """In blackhole mode the client times out on its own; wait until the relay
        has seen the request."""
        deadline = time.monotonic() + HUNG_SEC
        while self.stale_hits() < n and time.monotonic() < deadline:
            time.sleep(0.01)
        return self.stale_hits()

    def _event(self, text: str) -> None:
        with self._lock:
            self.events.append(text)

    def _accept(self) -> None:
        while not self._stop.is_set():
            try:
                client, _ = self.lsock.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            relay = _Relay(client)
            with self._lock:
                self.accepted += 1
                self._sockets.append(client)
                self._relays.append(relay)
            threading.Thread(target=self._pump, args=(relay,), daemon=True).start()

    def _pump(self, relay: _Relay) -> None:
        up = None
        try:
            up = socket.create_connection(("127.0.0.1", self.upstream_port))
            with self._lock:
                self._sockets.append(up)
            self._relay(relay, up)
        except (OSError, ValueError):
            pass   # a socket was closed by close() at teardown, or reset by the client
        finally:
            relay.forgotten.set()        # nothing left to forget; never block forget()
            with self._lock:
                self._relays.remove(relay)
            for s in (relay.client, up):
                if s is not None:
                    try:
                        s.close()
                    except OSError:
                        pass

    def _relay(self, relay: _Relay, up: socket.socket) -> None:
        client = relay.client
        for s in (client, up):
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        while not self._stop.is_set():
            if not relay.forgotten.is_set():
                if relay.forget.is_set():
                    up.close()          # the mapping is gone; the client is not told
                    relay.forgotten.set()
                    continue
                ready, _, _ = select.select([client, up], [], [], 0.01)
                for src, dst in ((client, up), (up, client)):
                    if src in ready:
                        data = src.recv(65536)
                        if not data:
                            return
                        dst.sendall(data)
                continue
            ready, _, _ = select.select([client], [], [], 0.01)
            if client not in ready:
                continue
            data = client.recv(65536)
            if not data:
                return
            self._event(f"data on forgotten connection -> {self.mode}")
            if self.mode == "rst":
                _rst_close(client)
                return
            # blackhole: swallow it and keep silent

    def close(self) -> None:
        self._stop.set()
        with self._lock:
            sockets = [self.lsock, *self._sockets]
        for s in sockets:
            try:
                s.close()
            except OSError:
                pass


@pytest.fixture
def upstream():
    server = Upstream()
    yield server
    server.shutdown()
    server.server_close()


@pytest.fixture
def middlebox(upstream, monkeypatch):
    monkeypatch.setattr(fetch, "TIMEOUT_SEC", HUNG_SEC)   # a stalled harness fails fast
    boxes: list[Middlebox] = []

    def make(mode: str) -> Middlebox:
        box = Middlebox(upstream.server_address[1], mode)
        boxes.append(box)
        return box

    yield make
    for box in boxes:
        box.close()


# --- the failure, and the two ways the collector now avoids it ----------------------------

def test_plain_session_fails_after_idle_drop(middlebox):
    """What the collector did before: one long-lived Session without retries."""
    box = middlebox("rst")
    session = local(requests.Session())
    assert session.get(f"{box.url}/feed.xml", timeout=HUNG_SEC).status_code == 200
    box.forget()
    with pytest.raises(requests.ConnectionError):
        session.get(f"{box.url}/feed.xml", timeout=HUNG_SEC)
    assert box.stale_hits() == 1 and box.accepted == 1
    # The broken connection is discarded, so the next attempt works: the
    # alternating ok/error pattern in the operating report.
    assert session.get(f"{box.url}/feed.xml", timeout=HUNG_SEC).status_code == 200


def test_fetcher_idle_reset_avoids_the_stale_connection(middlebox, monkeypatch):
    monkeypatch.setattr(fetch, "RETRY_TOTAL", 0)       # prove it without retries
    box = middlebox("rst")
    clock = FakeClock()
    fetcher = Fetcher(UA, clock=clock)
    local(fetcher.session)
    assert fetcher.get(f"{box.url}/feed.xml").status == 200
    box.forget()
    clock.now += fetch.IDLE_RESET_SEC + 1
    assert fetcher.get(f"{box.url}/feed.xml").status == 200
    assert box.stale_hits() == 0            # the stale socket was never written to
    assert box.accepted == 2 and fetcher.idle.resets == 1


def test_fetcher_retry_recovers_from_a_reset_when_idle_reset_is_off(middlebox):
    box = middlebox("rst")
    fetcher = Fetcher(UA, clock=FakeClock())    # the clock stands still: no idle reset
    local(fetcher.session)
    assert fetcher.get(f"{box.url}/feed.xml").status == 200
    box.forget()
    assert fetcher.get(f"{box.url}/feed.xml").status == 200
    assert box.stale_hits() == 1            # the stale socket failed, the retry did not
    assert box.accepted == 2 and fetcher.idle.resets == 0


def test_fetcher_does_not_retry_a_read_timeout(middlebox, monkeypatch):
    """A black-holed stale connection ends in a read timeout, like a hung server.
    Asking again would multiply the wait in the run loop; IdleReset is what
    avoids this case, and the next poll opens a new connection."""
    box = middlebox("blackhole")
    fetcher = Fetcher(UA, clock=FakeClock())    # the clock stands still: no idle reset
    local(fetcher.session)
    assert fetcher.get(f"{box.url}/feed.xml").status == 200
    box.forget()
    monkeypatch.setattr(fetch, "TIMEOUT_SEC", 0.3)       # only for the stale request
    with pytest.raises(FetchError) as info:
        fetcher.get(f"{box.url}/feed.xml")
    assert str(info.value).startswith("ReadTimeout: ")
    assert box.wait_for_stale_hits(1) == 1 and box.accepted == 1   # sent once, not again
    monkeypatch.setattr(fetch, "TIMEOUT_SEC", HUNG_SEC)
    assert fetcher.get(f"{box.url}/feed.xml").status == 200
    assert box.accepted == 2


def test_fetcher_does_not_retry_http_status(monkeypatch):
    server = Upstream(status=503)           # with Retry-After: 30
    try:
        fetcher = Fetcher(UA)
        local(fetcher.session)
        started = time.monotonic()
        with pytest.raises(FetchError) as info:
            fetcher.get(f"{server.url}/feed.xml")
        assert info.value.status == 503 and str(info.value) == "HTTP 503"
        assert server.hits == 1 and time.monotonic() - started < 5
    finally:
        server.shutdown()
        server.server_close()


def test_exhausted_retries_name_the_cause_first(monkeypatch):
    monkeypatch.setattr(fetch, "RETRY_BACKOFF_FACTOR", 0)
    fetcher = Fetcher(UA)
    local(fetcher.session)
    with pytest.raises(FetchError) as info:
        fetcher.get(f"http://127.0.0.1:{closed_port()}/feed.xml")
    text = str(info.value)
    assert text.startswith(f"ConnectionError ({fetch.RETRY_TOTAL + 1} attempts): "
                           "NewConnectionError: Failed to establish a new connection: ")
    # The errno text tells Wi-Fi down from a refusing server; the report keeps it.
    assert "Connection refused" in text[:report.ERROR_CHARS]


def test_connect_timeout_text_drops_the_connection_repr():
    reason = ConnectTimeoutError(HTTPSConnection("www.dtcc.com", 443),
                                 "Connection to www.dtcc.com timed out. (connect timeout=10)")
    exc = requests.ConnectTimeout(MaxRetryError(None, "/insights/rss", reason))
    assert fetch.describe_error(exc) == ("ConnectTimeout: ConnectTimeoutError: Connection to "
                                         "www.dtcc.com timed out. (connect timeout=10)")


class NotTLS:
    """Takes TCP connections and never completes a TLS handshake: "silent" never
    answers, "plain" answers in plain HTTP. Counts the connections."""

    def __init__(self, mode: str):
        self.mode = mode
        self.accepted = 0
        self._stop = threading.Event()
        self._held: list[socket.socket] = []
        self.lsock = socket.socket()
        self.lsock.bind(("127.0.0.1", 0))
        self.lsock.listen(8)
        self.lsock.settimeout(0.05)
        threading.Thread(target=self._serve, daemon=True).start()

    @property
    def url(self) -> str:
        return f"https://127.0.0.1:{self.lsock.getsockname()[1]}"

    def _serve(self) -> None:
        while not self._stop.is_set():
            try:
                conn, _ = self.lsock.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            self.accepted += 1
            if self.mode == "silent":
                self._held.append(conn)
                continue
            conn.settimeout(HUNG_SEC)
            try:
                conn.recv(65536)                     # the TLS ClientHello
                conn.sendall(b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n")
            except OSError:
                pass
            conn.close()

    def close(self) -> None:
        self._stop.set()
        for s in (self.lsock, *self._held):
            s.close()


def test_tls_handshake_timeout_is_marked_and_not_retried(monkeypatch):
    """urllib3 reports a stalled TLS handshake as a read timeout that carries the
    connect value. It is not retried, and the text says where it happened, so it
    is not mistaken for a server that took the request and did not answer."""
    monkeypatch.setattr(fetch, "CONNECT_TIMEOUT_SEC", 0.3)
    server = NotTLS("silent")
    try:
        fetcher = Fetcher(UA)
        local(fetcher.session)
        with pytest.raises(FetchError) as info:
            fetcher.get(f"{server.url}/feed.xml")
        text = str(info.value)
        assert text.startswith("ReadTimeout (TLS handshake): ")
        assert text.endswith("(read timeout=0.3)")
        assert server.accepted == 1
    finally:
        server.close()


def test_an_error_the_policy_never_retries_is_not_labelled_retried():
    """An SSLError (here: a plain HTTP answer to https) gives up at once."""
    server = NotTLS("plain")
    try:
        fetcher = Fetcher(UA)
        local(fetcher.session)
        with pytest.raises(FetchError) as info:
            fetcher.get(f"{server.url}/feed.xml")
        assert str(info.value).startswith("SSLError (1 attempt): SSLError: ")
        assert server.accepted == 1
    finally:
        server.close()


# --- Telegram POST and secrets ---------------------------------------------------------------

class AcceptThenFail:
    """Reads one request per connection, then closes it ("close") or never answers
    ("hang"). Counts the requests it received."""

    def __init__(self, mode: str):
        self.mode = mode
        self.requests = 0
        self._stop = threading.Event()
        self._held: list[socket.socket] = []
        self.lsock = socket.socket()
        self.lsock.bind(("127.0.0.1", 0))
        self.lsock.listen(8)
        self.lsock.settimeout(0.05)
        threading.Thread(target=self._serve, daemon=True).start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.lsock.getsockname()[1]}"

    def _serve(self) -> None:
        while not self._stop.is_set():
            try:
                conn, _ = self.lsock.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            conn.settimeout(2)
            data = b""
            try:
                while b"\r\n\r\n" not in data:
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    data += chunk
            except OSError:
                pass
            if data:
                self.requests += 1
            if self.mode == "hang":
                self._held.append(conn)
            else:
                conn.close()

    def close(self) -> None:
        self._stop.set()
        for s in (self.lsock, *self._held):
            s.close()


@pytest.mark.parametrize("mode", ["close", "hang"])
def test_telegram_post_is_not_retried_after_it_was_sent(monkeypatch, caplog, mode):
    monkeypatch.setattr(fetch, "RETRY_BACKOFF_FACTOR", 0)
    monkeypatch.setattr(notify, "TELEGRAM_TIMEOUT_SEC", 0.3)
    server = AcceptThenFail(mode)
    monkeypatch.setattr(notify, "TELEGRAM_API", server.url)
    try:
        notifier = TelegramNotifier(TOKEN, "1")
        local(notifier.session)
        assert notifier.send(Alert("high", "m")) is False
        assert server.requests == 1           # sent once, never repeated
        if mode == "close":
            # The same session does retry a GET on the same failure.
            with pytest.raises(requests.ConnectionError):
                notifier.session.get(f"{server.url}/x", timeout=1)
            assert server.requests == 1 + 3
    finally:
        server.close()
    assert "CONN-TEST" not in caplog.text


def test_telegram_connect_errors_are_retried_and_logs_hide_the_token(monkeypatch, caplog):
    monkeypatch.setattr(fetch, "RETRY_BACKOFF_FACTOR", 0)
    monkeypatch.setattr(notify, "TELEGRAM_API", f"http://127.0.0.1:{closed_port()}")
    caplog.set_level(logging.WARNING, logger="urllib3")
    notifier = TelegramNotifier(TOKEN, "1")
    local(notifier.session)
    assert notifier.send(Alert("high", "m")) is False
    retries = [r for r in caplog.records if r.getMessage().startswith("Retrying")]
    assert len(retries) == 2                  # connection refused: nothing was sent
    assert "/bot<redacted>/sendMessage" in caplog.text
    assert "CONN-TEST" not in caplog.text


def test_debug_logs_hide_the_token(monkeypatch, caplog, upstream):
    """`collector run -v` logs urllib3 at DEBUG: retry counters and request lines."""
    monkeypatch.setattr(fetch, "RETRY_BACKOFF_FACTOR", 0)
    caplog.set_level(logging.DEBUG, logger="urllib3")
    token = "654321:DEBUG-LEAK-check-token"
    notifier = TelegramNotifier(token, "1")
    local(notifier.session)
    monkeypatch.setattr(notify, "TELEGRAM_API", f"http://127.0.0.1:{closed_port()}")
    assert notifier.send(Alert("high", "m")) is False
    monkeypatch.setattr(notify, "TELEGRAM_API", upstream.url)
    assert notifier.send(Alert("high", "m")) is True
    debug = [r for r in caplog.records
             if r.levelno == logging.DEBUG and r.name.startswith("urllib3")]
    assert any(r.name == "urllib3.util.retry" for r in debug)          # "Incremented Retry"
    assert any("POST /bot<redacted>/sendMessage" in r.getMessage() for r in debug)
    assert "DEBUG-LEAK" not in caplog.text


def test_heartbeat_url_is_hidden_from_urllib3_logs(monkeypatch, caplog):
    monkeypatch.setattr(fetch, "RETRY_BACKOFF_FACTOR", 0)
    caplog.set_level(logging.WARNING, logger="urllib3")
    beat = Heartbeat(f"http://127.0.0.1:{closed_port()}/ping/hb-secret-uuid-0001", UA)
    local(beat.session)
    assert beat.beat(datetime(2026, 10, 1, tzinfo=timezone.utc)) is False
    assert any(r.getMessage().startswith("Retrying") for r in caplog.records)
    assert "hb-secret-uuid" not in caplog.text


def test_secret_filter_redacts_tracebacks():
    token = "777777:TRACEBACK-only-token"
    fetch.register_secret(token)
    try:
        raise RuntimeError(f"failed on /bot{token}/sendMessage")
    except RuntimeError:
        record = logging.LogRecord("x", logging.ERROR, __file__, 1, "boom %s", (token,),
                                   exc_info=sys.exc_info())
    assert fetch.SECRET_FILTER.filter(record)
    assert token not in record.getMessage() and token not in record.exc_text
    assert "<redacted>" in record.exc_text


def test_log_handlers_redact_secrets_from_any_logger(tmp_path, capsys):
    """The handlers of `collector run` filter records of our own loggers too,
    not only urllib3's."""
    from collector.__main__ import _log_handlers

    ping = "https://hc-ping.example/hb-secret-uuid-0003"
    fetch.register_secret_url(ping)
    log_path = tmp_path / "data" / "collector.log"
    handlers = _log_handlers(log_path)
    log = logging.getLogger("collector.test-handlers")
    log.propagate = False
    for handler in handlers:
        log.addHandler(handler)
    try:
        try:
            raise RuntimeError(f"GET {ping} failed")
        except RuntimeError:
            log.exception("ping %s failed", ping)
    finally:
        log.propagate = True
        for handler in handlers:
            log.removeHandler(handler)
            handler.close()
    written = log_path.read_text(encoding="utf-8")
    assert "RuntimeError" in written and "<redacted>" in written
    assert "hb-secret-uuid" not in written
    err = capsys.readouterr().err
    assert "<redacted>" in err and "hb-secret-uuid" not in err


def test_make_session_mounts_the_retry_policy():
    session = local(make_session())
    retry = session.get_adapter("https://example.org").max_retries
    assert isinstance(retry, fetch.CollectorRetry)
    assert (retry.total, retry.connect, retry.read, retry.status, retry.other) == (2, 2, 2, 0, 0)
    assert retry.raise_on_status is False
    assert "POST" not in retry.allowed_methods and "GET" in retry.allowed_methods
    assert session.get_adapter("http://example.org").max_retries.total == 2


RESET = ConnectionResetError(54, "Connection reset by peer")


@pytest.mark.parametrize("method, error, raised", [
    # Anything that may have reached the server: never again for a POST. SSLError
    # and ProxyError are "other" errors, which urllib3 < 1.26 retried for any method.
    ("POST", SSLError("bad record mac"), MaxRetryError),
    ("POST", ProxyError("Cannot connect to proxy.", RESET), MaxRetryError),
    ("POST", ProtocolError("Connection aborted.", RESET), ProtocolError),
    # A read timeout is not retried for any method.
    ("POST", ReadTimeoutError(None, "/x", "Read timed out."), ReadTimeoutError),
    ("GET", ReadTimeoutError(None, "/x", "Read timed out."), ReadTimeoutError),
])
def test_retry_policy_gives_up(method, error, raised):
    with pytest.raises(raised):
        fetch.make_retry().increment(method=method, url="/x", error=error)


@pytest.mark.parametrize("method, error", [
    ("POST", ConnectTimeoutError("connect timed out")),     # nothing was sent yet
    ("GET", ConnectTimeoutError("connect timed out")),
    ("GET", ProtocolError("Connection aborted.", RESET)),    # a stale connection
])
def test_retry_policy_retries(method, error):
    retry = fetch.make_retry().increment(method=method, url="/x", error=error)
    assert isinstance(retry, fetch.CollectorRetry) and retry.total == fetch.RETRY_TOTAL - 1


# --- idle reset (unit) ---------------------------------------------------------------------------

class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


class ClosingSession:
    def __init__(self):
        self.closed = 0
        self.urls: list[str] = []
        self.timeouts: list = []

    def close(self):
        self.closed += 1

    def get(self, url, headers=None, timeout=None):
        self.urls.append(url)
        self.timeouts.append(timeout)
        return type("Resp", (), {"status_code": 304, "url": url})()


def test_idle_reset_closes_only_after_the_threshold():
    session, clock = ClosingSession(), FakeClock()
    idle = fetch.IdleReset(session, clock)
    url = "https://www.sec.gov/news/pressreleases.rss"
    idle.before(url)                              # first use: nothing pooled yet
    idle.used(url)
    clock.now += fetch.IDLE_RESET_SEC             # exactly at the threshold: keep
    idle.before(url)
    idle.used(url)
    assert session.closed == 0
    clock.now += fetch.IDLE_RESET_SEC + 1
    idle.before(url)
    assert session.closed == 1 and idle.resets == 1
    idle.before(url)                              # the pool is already empty
    assert session.closed == 1


def test_idle_time_is_measured_with_the_wall_clock():
    """On macOS the monotonic clock stops while the machine sleeps, but the router's
    NAT entries keep expiring. With time.monotonic, a poll right after a 30-minute
    sleep would count only the seconds the machine was awake and reuse the
    connection the router has already forgotten. Every client defaults to time.time."""
    idles = {
        "IdleReset": fetch.IdleReset(ClosingSession()),
        "Fetcher": Fetcher(UA).idle,
        "UpbitClient": UpbitClient(UA).http.idle,
        "KrakenClient": KrakenClient(UA).http.idle,
        "TelegramNotifier": TelegramNotifier(TOKEN, "1").idle,
        "Heartbeat": Heartbeat("https://hc-ping.example/hb-secret-uuid-0005", UA).idle,
    }
    for name, idle in idles.items():
        if isinstance(idle.session, requests.Session):
            local(idle.session)
        assert idle._clock is time.time, name


def test_idle_reset_tracks_hosts_separately():
    """One Fetcher session serves several hosts on different schedules."""
    session, clock = ClosingSession(), FakeClock()
    idle = fetch.IdleReset(session, clock)
    idle.used("https://www.federalreserve.gov/feeds/press_all.xml")
    clock.now += 570
    idle.used("https://www.sec.gov/news/pressreleases.rss")   # the session is busy...
    clock.now += 30
    idle.before("https://www.federalreserve.gov/feeds/press_all.xml")
    assert session.closed == 1                    # ...but the Fed connection is 10 min old


def test_idle_reset_through_fetcher_and_sessions_without_close():
    session, clock = ClosingSession(), FakeClock()
    fetcher = Fetcher(UA, session, clock)
    url = "https://hedera.com/blog/rss.xml"
    fetcher.get(url)
    clock.now += 1800
    fetcher.get(url, etag='"v1"')
    assert session.closed == 1 and session.urls == [url, url]
    # A separate, short connect timeout keeps connect retries cheap.
    assert session.timeouts == [(fetch.CONNECT_TIMEOUT_SEC, fetch.TIMEOUT_SEC)] * 2

    class NoClose:
        def get(self, url, headers=None, timeout=None):
            return type("Resp", (), {"status_code": 304})()

    fetcher = Fetcher(UA, NoClose(), clock)
    fetcher.get(url)
    clock.now += 1800
    assert fetcher.get(url).not_modified          # nothing to close, still works

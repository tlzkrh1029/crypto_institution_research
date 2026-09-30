"""Alert delivery (docs/decisions.md D-010: Telegram bot).

Every alert is always written to the log. With NOTIFIER=telegram it is also
sent to one Telegram chat through the Bot API. The bot token is a credential:
it lives in .env and is never logged (request errors are logged by type only,
because the token is part of the request URL, and the token is registered
with collector.fetch.register_secret so urllib3's own log lines omit it).

sendMessage is a POST: the session from collector.fetch.make_session() retries
it only when the TCP connection could not be opened, never after the request
may have reached Telegram. A failure in the TLS handshake is not retried
either, although nothing was sent (collector/fetch.py). A send that fails
this way, or whose response is lost (read timeout, reset after the request
went out), returns False, so the alert stays undelivered and
pipeline.retry_undelivered posts it again 5 minutes later. When only the
response was lost, Telegram then shows the same alert twice.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Protocol

import requests

from .fetch import CONNECT_TIMEOUT_SEC, IdleReset, make_session, register_secret

log = logging.getLogger("collector.alert")

TELEGRAM_API = "https://api.telegram.org"
TELEGRAM_TEXT_LIMIT = 4096
TELEGRAM_TIMEOUT_SEC = 15


class NotifierConfigError(ValueError):
    pass


@dataclass(frozen=True)
class Alert:
    level: str
    message: str
    url: str | None = None
    event_id: int | None = None
    source_id: str | None = None

    def text(self) -> str:
        body = f"[{self.level.upper()}] {self.message}"
        if self.url:
            body += f"\n{self.url}"
        return body[:TELEGRAM_TEXT_LIMIT]


class Notifier(Protocol):
    name: str

    def send(self, alert: Alert) -> bool: ...


class LogNotifier:
    name = "log"

    def send(self, alert: Alert) -> bool:
        log.warning("%s", alert.text().replace("\n", " "))
        return True


class TelegramNotifier:
    name = "telegram"

    def __init__(self, token: str, chat_id: str, session: requests.Session | None = None,
                 clock=time.time):
        register_secret(token)
        self.token = token
        self.chat_id = chat_id
        self.session = session or make_session()
        self.idle = IdleReset(self.session, clock)

    def send(self, alert: Alert) -> bool:
        LogNotifier().send(alert)
        url = f"{TELEGRAM_API}/bot{self.token}/sendMessage"
        self.idle.before(url)
        try:
            resp = self.session.post(
                url,
                json={"chat_id": self.chat_id, "text": alert.text(),
                      "link_preview_options": {"is_disabled": True}},
                timeout=(CONNECT_TIMEOUT_SEC, TELEGRAM_TIMEOUT_SEC),
            )
        except requests.RequestException as exc:
            log.warning("telegram send failed: %s", type(exc).__name__)
            return False
        finally:
            self.idle.used(url)
        if resp.status_code != 200:
            description = ""
            try:
                description = resp.json().get("description", "")
            except ValueError:
                pass
            log.warning("telegram send failed: HTTP %s %s", resp.status_code, description)
            return False
        return True


def telegram_chats(token: str, session: requests.Session | None = None) -> list[dict]:
    """Chats that recently messaged the bot (for finding TELEGRAM_CHAT_ID)."""
    register_secret(token)
    own = session is None
    session = session or make_session()
    try:
        resp = session.get(f"{TELEGRAM_API}/bot{token}/getUpdates",
                           timeout=(CONNECT_TIMEOUT_SEC, TELEGRAM_TIMEOUT_SEC))
    except requests.RequestException as exc:
        raise NotifierConfigError(f"getUpdates failed: {type(exc).__name__}") from None
    finally:
        if own:
            session.close()
    try:
        data = resp.json()
    except ValueError:
        data = {}
    if resp.status_code != 200 or not data.get("ok"):
        raise NotifierConfigError(
            f"getUpdates failed: HTTP {resp.status_code} {data.get('description', '')}".strip())
    chats: dict[int, dict] = {}
    for update in data.get("result", []):
        message = update.get("message") or update.get("edited_message") or {}
        chat = message.get("chat")
        if chat:
            chats[chat["id"]] = {"id": chat["id"], "type": chat.get("type"),
                                 "name": chat.get("username") or chat.get("title")
                                 or chat.get("first_name") or ""}
    return list(chats.values())


def make_notifier(name: str, env=None) -> Notifier:
    """`env` is a callable like Settings.env returning .env values."""
    if name == "log":
        return LogNotifier()
    if name == "telegram":
        token = env("TELEGRAM_BOT_TOKEN") if env else ""
        chat_id = env("TELEGRAM_CHAT_ID") if env else ""
        if not token or not chat_id:
            raise NotifierConfigError(
                "NOTIFIER=telegram needs TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env "
                "(docs/setup-macos.md)")
        return TelegramNotifier(token, chat_id)
    raise NotifierConfigError(f"unknown notifier {name!r}; use 'log' or 'telegram'")

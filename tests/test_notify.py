import pytest
import requests

from collector.notify import (
    Alert, NotifierConfigError, TelegramNotifier, make_notifier, telegram_chats)
from collector.pipeline import deliver_alert, retry_undelivered

TOKEN = "123456:SECRET-token"


class Resp:
    def __init__(self, status=200, data=None):
        self.status_code = status
        self._data = data or {"ok": status == 200}

    def json(self):
        return self._data


class TelegramSession:
    def __init__(self, fail=None):
        self.fail = fail
        self.posts = []

    def post(self, url, json=None, timeout=None):
        if self.fail == "network":
            raise requests.ConnectionError(f"cannot reach {url}")
        self.posts.append((url, json))
        if self.fail == "http":
            return Resp(400, {"ok": False, "description": "Bad Request: chat not found"})
        return Resp()

    def get(self, url, timeout=None):
        return Resp(200, {"ok": True, "result": [
            {"update_id": 1, "message": {"chat": {"id": 987654, "type": "private",
                                                  "first_name": "Me"}}}]})


def test_telegram_sends_text_without_link_preview():
    session = TelegramSession()
    ok = TelegramNotifier(TOKEN, "987654", session).send(
        Alert("high", "TCH + Quant (QNT) | title", url="https://x.example/a"))
    assert ok
    url, body = session.posts[0]
    assert url.endswith("/sendMessage") and body["chat_id"] == "987654"
    assert body["text"] == "[HIGH] TCH + Quant (QNT) | title\nhttps://x.example/a"
    assert body["link_preview_options"] == {"is_disabled": True}


def test_telegram_failure_never_logs_the_token(caplog):
    for fail in ("network", "http"):
        assert not TelegramNotifier(TOKEN, "1", TelegramSession(fail)).send(Alert("high", "m"))
    assert "SECRET" not in caplog.text


def test_make_notifier_requires_token_and_chat():
    with pytest.raises(NotifierConfigError):
        make_notifier("telegram", lambda name: "")
    env = {"TELEGRAM_BOT_TOKEN": TOKEN, "TELEGRAM_CHAT_ID": "1"}
    assert make_notifier("telegram", env.get).name == "telegram"
    with pytest.raises(NotifierConfigError):
        make_notifier("kakao", env.get)


def test_telegram_chats_lists_chat_ids():
    assert telegram_chats(TOKEN, TelegramSession()) == [
        {"id": 987654, "type": "private", "name": "Me"}]


class FlakyNotifier:
    name = "flaky"

    def __init__(self):
        self.up = False
        self.sent = []

    def send(self, alert):
        if self.up:
            self.sent.append(alert)
        return self.up


def test_undelivered_alert_is_retried(harness):
    ctx, fetcher, notifier, clock, register = harness
    ctx.notifier = FlakyNotifier()
    deliver_alert(ctx, Alert("high", "important"), clock.now)
    row = ctx.conn.execute("SELECT * FROM alerts").fetchone()
    assert row["delivered_at"] is None and row["attempts"] == 1
    assert retry_undelivered(ctx, clock.now) == 0          # still down
    ctx.notifier.up = True
    assert retry_undelivered(ctx, clock.now) == 1
    row = ctx.conn.execute("SELECT * FROM alerts").fetchone()
    assert row["delivered_via"] == "flaky" and row["attempts"] == 3
    assert retry_undelivered(ctx, clock.now) == 0          # nothing left


def test_check_config_reports_notifier_without_printing_the_token(tmp_path, capsys):
    import shutil
    from pathlib import Path

    from collector.__main__ import main

    repo = Path(__file__).resolve().parent.parent
    shutil.copytree(repo / "config", tmp_path / "config")
    (tmp_path / ".env").write_text('NOTIFIER="telegram"\nTELEGRAM_BOT_TOKEN="123:SECRET"\n')
    assert main(["--root", str(tmp_path), "check-config"]) == 2
    out = capsys.readouterr()
    assert "telegram token set, chat id not set" in out.out
    assert "TELEGRAM_CHAT_ID" in out.err
    assert "SECRET" not in out.out + out.err

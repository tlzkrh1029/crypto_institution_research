"""One polling run of one source: fetch, parse, store, match, group, alert."""

from __future__ import annotations

import logging
import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable

from .config import Entity, Settings, SourceConfig
from .events import place_item
from .fetch import FetchError, Fetcher
from .heartbeat import Heartbeat
from .matching import assess, match_text, publisher_match
from .normalize import canonical_url, content_hash
from .notify import Alert, Notifier
from .sources import RawItem
from .sources.feeds import FeedParseError, parse_feed
from .sources.sitemap import SitemapParseError, parse_sitemap
from .timeutil import to_iso, utcnow

log = logging.getLogger("collector.pipeline")

STALE_AFTER = timedelta(days=3)       # older items are recorded but not alerted
MAX_BACKOFF_SEC = 6 * 3600
RETRY_MAX_ATTEMPTS = 12   # retried every 5 minutes: about one hour of outage
RETRY_WINDOW = timedelta(hours=24)


@dataclass
class Context:
    settings: Settings
    conn: sqlite3.Connection
    fetcher: Fetcher
    entities: list[Entity]
    notifier: Notifier
    heartbeat: Heartbeat | None = None
    clock: Callable[[], datetime] = field(default=utcnow)


@dataclass
class RunOutcome:
    source_id: str
    status: str               # ok, not_modified, error, skipped
    items_seen: int = 0
    items_new: int = 0
    events_new: int = 0
    alerts: int = 0
    error: str | None = None


def backoff_seconds(interval_sec: int, failures: int) -> int:
    return min(interval_sec * 2 ** min(failures, 6), MAX_BACKOFF_SEC)


def sync_sources(conn: sqlite3.Connection, sources: list[SourceConfig]) -> None:
    """Copy config/sources.yaml into the sources table, keeping polling state."""
    with conn:
        for s in sources:
            conn.execute(
                """INSERT INTO sources (id, name, kind, url, poll_interval_sec, publisher_kind,
                                        enabled)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                       name = excluded.name, kind = excluded.kind, url = excluded.url,
                       poll_interval_sec = excluded.poll_interval_sec,
                       publisher_kind = excluded.publisher_kind, enabled = excluded.enabled""",
                (s.id, s.name, s.kind, s.url, s.interval_sec, s.publisher_kind, int(s.enabled)),
            )
        known = [s.id for s in sources]
        marks = ",".join("?" for _ in known) or "''"
        conn.execute(f"UPDATE sources SET enabled = 0 WHERE id NOT IN ({marks})", known)


def due_sources(conn: sqlite3.Connection, sources: list[SourceConfig],
                now: datetime) -> list[SourceConfig]:
    next_due = {r["id"]: r["next_due_at"]
                for r in conn.execute("SELECT id, next_due_at FROM sources")}
    now_iso = to_iso(now)
    return [s for s in sources
            if s.enabled and (next_due.get(s.id) is None or next_due[s.id] <= now_iso)]


def run_source(ctx: Context, source: SourceConfig) -> RunOutcome:
    now = ctx.clock()
    conn = ctx.conn
    state = conn.execute("SELECT * FROM sources WHERE id = ?", (source.id,)).fetchone()
    run_id = conn.execute(
        "INSERT INTO runs (source_id, started_at, status) VALUES (?, ?, 'running')",
        (source.id, to_iso(now)),
    ).lastrowid
    conn.commit()

    user_agent = None
    if source.requires_env:
        user_agent = ctx.settings.env(source.requires_env)
        if not user_agent:
            outcome = RunOutcome(source.id, "skipped",
                                 error=f"{source.requires_env} is not set")
            _finish(conn, run_id, source, now, outcome, success=None)
            return outcome

    try:
        result = ctx.fetcher.get(source.url, etag=state["etag"],
                                 last_modified=state["last_modified"], user_agent=user_agent)
    except FetchError as exc:
        outcome = RunOutcome(source.id, "error", error=str(exc))
        _finish(conn, run_id, source, now, outcome, success=False, http_status=exc.status)
        return outcome

    if result.not_modified:
        outcome = RunOutcome(source.id, "not_modified")
        _finish(conn, run_id, source, now, outcome, success=True, http_status=304)
        return outcome

    try:
        if source.kind == "feed":
            raw_items = parse_feed(result.content or b"")
        else:
            raw_items = parse_sitemap(result.content or b"", source.url_filter, now,
                                      source.max_age_days)
    except (FeedParseError, SitemapParseError) as exc:
        outcome = RunOutcome(source.id, "error", error=f"parse: {exc}")
        _finish(conn, run_id, source, now, outcome, success=False, http_status=200)
        return outcome

    # The first successful run only records a baseline, so that the backlog of
    # an existing feed does not raise a burst of alerts.
    baseline = not state["baseline_done"]
    outcome = RunOutcome(source.id, "ok", items_seen=len(raw_items))
    for raw in raw_items:
        _process_item(ctx, source, raw, now, baseline, outcome)
    with conn:
        conn.execute("UPDATE sources SET etag = ?, last_modified = ?, baseline_done = 1 "
                     "WHERE id = ?", (result.etag, result.last_modified, source.id))
    _finish(conn, run_id, source, now, outcome, success=True, http_status=200)
    return outcome


def _process_item(ctx: Context, source: SourceConfig, raw: RawItem, now: datetime,
                  baseline: bool, outcome: RunOutcome) -> None:
    conn = ctx.conn
    canonical = canonical_url(raw.link)
    if conn.execute("SELECT 1 FROM items WHERE canonical_url = ?", (canonical,)).fetchone():
        return
    # The excerpt is always used for matching, but stored only when the
    # source's terms allow it (store_excerpt: false keeps title, link, date).
    text = f"{raw.title} {raw.excerpt}"
    matches = match_text(text, ctx.entities)
    if source.publisher_entity and all(m.entity_id != source.publisher_entity
                                       for m in matches):
        matches.insert(0, publisher_match(source.publisher_entity, ctx.entities))
    excerpt = raw.excerpt if source.store_excerpt else ""
    with conn:
        item_id = conn.execute(
            """INSERT INTO items (source_id, url, canonical_url, title, published_at,
                                  updated_at, fetched_at, content_hash, excerpt,
                                  matched_entities, baseline)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (source.id, raw.link, canonical, raw.title, to_iso(raw.published_at),
             to_iso(raw.updated_at), to_iso(now), content_hash(raw.title), excerpt,
             ",".join(m.entity_id for m in matches), int(baseline)),
        ).lastrowid
    outcome.items_new += 1

    assessment = assess(matches, source.publisher_kind)
    if not assessment.makes_event:
        return  # kept in items (with matched_entities) for later search
    token_mention = "yes" if any(
        re.search(rf"\b{re.escape(t)}\b", text) for t in assessment.tokens) else "unknown"
    placement = place_item(conn, item_id=item_id, title=raw.title,
                           published_at=raw.published_at, assessment=assessment,
                           token_mention=token_mention, now=now)
    if not placement.created:
        return
    outcome.events_new += 1
    item_time = raw.published_at or raw.updated_at or now
    if baseline or assessment.level is None or now - item_time > STALE_AFTER:
        return
    labels = [m.label for m in matches if m.kind != "theme"]
    tokens = f" ({', '.join(assessment.tokens)})" if assessment.tokens else ""
    alert = Alert(
        level=assessment.level,
        message=f"{' + '.join(labels)}{tokens} | {raw.title}",
        url=raw.link,
        event_id=placement.event_id,
        source_id=source.id,
    )
    deliver_alert(ctx, alert, now)
    outcome.alerts += 1


def deliver_alert(ctx: Context, alert: Alert, now: datetime) -> None:
    conn = ctx.conn
    with conn:
        alert_id = conn.execute(
            """INSERT INTO alerts (created_at, level, event_id, source_id, message, url)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (to_iso(now), alert.level, alert.event_id, alert.source_id, alert.message,
             alert.url),
        ).lastrowid
    _send(ctx, alert_id, alert, now)


def _send(ctx: Context, alert_id: int, alert: Alert, now: datetime) -> bool:
    try:
        delivered = ctx.notifier.send(alert)
    except Exception:  # a broken channel must not stop collection
        log.exception("notifier %s failed", ctx.notifier.name)
        delivered = False
    with ctx.conn:
        ctx.conn.execute("UPDATE alerts SET attempts = attempts + 1 WHERE id = ?", (alert_id,))
        if delivered:
            ctx.conn.execute(
                "UPDATE alerts SET delivered_via = ?, delivered_at = ? WHERE id = ?",
                (ctx.notifier.name, to_iso(now), alert_id))
    return delivered


def retry_undelivered(ctx: Context, now: datetime, max_attempts: int = RETRY_MAX_ATTEMPTS,
                      within: timedelta = RETRY_WINDOW) -> int:
    """Resend alerts that failed to go out (e.g. the network was down)."""
    rows = ctx.conn.execute(
        """SELECT * FROM alerts WHERE delivered_at IS NULL AND attempts < ?
               AND created_at >= ? ORDER BY id""",
        (max_attempts, to_iso(now - within))).fetchall()
    sent = 0
    for r in rows:
        alert = Alert(level=r["level"], message=r["message"], url=r["url"],
                      event_id=r["event_id"], source_id=r["source_id"])
        if _send(ctx, r["id"], alert, now):
            sent += 1
        else:
            break  # the channel is still down; try again on the next tick
    return sent


def _finish(conn: sqlite3.Connection, run_id: int, source: SourceConfig, now: datetime,
            outcome: RunOutcome, *, success: bool | None, http_status: int | None = None) -> None:
    with conn:
        conn.execute(
            """UPDATE runs SET finished_at = ?, status = ?, http_status = ?, items_seen = ?,
                               items_new = ?, error = ? WHERE id = ?""",
            (to_iso(now), outcome.status, http_status, outcome.items_seen, outcome.items_new,
             outcome.error, run_id),
        )
        if success is True:
            conn.execute(
                """UPDATE sources SET last_attempt_at = ?, last_ok_at = ?,
                       consecutive_failures = 0, next_due_at = ? WHERE id = ?""",
                (to_iso(now), to_iso(now),
                 to_iso(now + timedelta(seconds=source.interval_sec)), source.id),
            )
        elif success is False:
            failures = conn.execute("SELECT consecutive_failures FROM sources WHERE id = ?",
                                    (source.id,)).fetchone()[0] + 1
            delay = backoff_seconds(source.interval_sec, failures)
            conn.execute(
                """UPDATE sources SET last_attempt_at = ?, last_error_at = ?, last_error = ?,
                       consecutive_failures = ?, next_due_at = ? WHERE id = ?""",
                (to_iso(now), to_iso(now), outcome.error, failures,
                 to_iso(now + timedelta(seconds=delay)), source.id),
            )
        else:  # skipped: not a failure, try again after the normal interval
            conn.execute(
                """UPDATE sources SET last_attempt_at = ?, last_error = ?, next_due_at = ?
                   WHERE id = ?""",
                (to_iso(now), outcome.error,
                 to_iso(now + timedelta(seconds=source.interval_sec)), source.id),
            )
    if outcome.status == "error":
        log.warning("%s: %s", source.id, outcome.error)
    else:
        log.info("%s: %s seen=%d new=%d events=%d alerts=%d", source.id, outcome.status,
                 outcome.items_seen, outcome.items_new, outcome.events_new, outcome.alerts)

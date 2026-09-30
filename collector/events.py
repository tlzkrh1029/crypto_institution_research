"""Group matched items into events.

An event is one announcement or story. Several items (the same press release
on two wires, follow-up articles) attach to one event. A story that shows up
again long after its first publication is attached with role "rerun"
(docs/research-principles.md section 4: 재확산).
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

from .matching import Assessment
from .normalize import jaccard, title_tokens
from .timeutil import from_iso, to_iso

LOOKBACK_DAYS = 30          # how far back to search for the same story
SIMILARITY_THRESHOLD = 0.4  # title-token Jaccard for "same story"
RERUN_AFTER_DAYS = 14       # published this long after the event's first publication


@dataclass(frozen=True)
class Placement:
    event_id: int
    role: str        # origin, duplicate, rerun
    created: bool


def _candidate_events(conn: sqlite3.Connection, entity_ids: tuple[str, ...],
                      since: datetime) -> list[sqlite3.Row]:
    if not entity_ids:
        return []
    marks = ",".join("?" for _ in entity_ids)
    return conn.execute(
        f"""
        SELECT DISTINCT e.* FROM events e
        JOIN event_entities ee ON ee.event_id = e.id
        WHERE ee.entity_id IN ({marks}) AND e.last_seen_at >= ?
        ORDER BY e.first_seen_at
        """,
        (*entity_ids, to_iso(since)),
    ).fetchall()


def place_item(conn: sqlite3.Connection, *, item_id: int, title: str,
               published_at: datetime | None, assessment: Assessment,
               token_mention: str, now: datetime) -> Placement:
    """Attach the item to an existing event or create a new one."""
    key_entities = assessment.institutions + assessment.projects
    tokens = title_tokens(title)
    item_time = published_at or now
    for event in _candidate_events(conn, key_entities, now - timedelta(days=LOOKBACK_DAYS)):
        if jaccard(tokens, title_tokens(event["title"])) < SIMILARITY_THRESHOLD:
            continue
        first = from_iso(event["first_published_at"]) or from_iso(event["first_seen_at"])
        role = "rerun" if item_time - first > timedelta(days=RERUN_AFTER_DAYS) else "duplicate"
        with conn:
            conn.execute("INSERT OR IGNORE INTO event_items VALUES (?, ?, ?)",
                         (event["id"], item_id, role))
            conn.execute("UPDATE events SET last_seen_at = ? WHERE id = ?",
                         (to_iso(now), event["id"]))
            _add_entities_and_assets(conn, event["id"], assessment)
            if token_mention == "yes":
                conn.execute("UPDATE events SET token_mention = 'yes' WHERE id = ?",
                             (event["id"],))
        return Placement(event["id"], role, created=False)

    with conn:
        cur = conn.execute(
            """INSERT INTO events (title, first_published_at, first_seen_at, last_seen_at,
                                   level, token_mention)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (title, to_iso(published_at), to_iso(now), to_iso(now), assessment.level,
             token_mention),
        )
        event_id = cur.lastrowid
        conn.execute("INSERT INTO event_items VALUES (?, ?, 'origin')", (event_id, item_id))
        _add_entities_and_assets(conn, event_id, assessment)
    return Placement(event_id, "origin", created=True)


def _add_entities_and_assets(conn: sqlite3.Connection, event_id: int,
                             assessment: Assessment) -> None:
    for kind, ids in (("institution", assessment.institutions),
                      ("project", assessment.projects),
                      ("theme", assessment.themes)):
        for entity_id in ids:
            conn.execute("INSERT OR IGNORE INTO event_entities VALUES (?, ?, ?)",
                         (event_id, entity_id, kind))
    for symbol in assessment.tokens:
        # The grade stays "unknown" until review (docs/research-principles.md section 2).
        conn.execute(
            "INSERT OR IGNORE INTO event_assets (event_id, symbol) VALUES (?, ?)",
            (event_id, symbol))

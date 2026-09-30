"""SQLite storage (docs/collector-spec.md section 5). The file lives in data/."""

from __future__ import annotations

import sqlite3
from pathlib import Path

MIGRATIONS: list[str] = [
    # 1: sources, items, events, alerts, runs
    """
    CREATE TABLE sources (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        kind TEXT NOT NULL,
        url TEXT NOT NULL,
        poll_interval_sec INTEGER NOT NULL,
        publisher_kind TEXT NOT NULL,
        enabled INTEGER NOT NULL DEFAULT 1,
        etag TEXT,
        last_modified TEXT,
        last_attempt_at TEXT,
        last_ok_at TEXT,
        last_error_at TEXT,
        last_error TEXT,
        consecutive_failures INTEGER NOT NULL DEFAULT 0,
        next_due_at TEXT,
        baseline_done INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE items (
        id INTEGER PRIMARY KEY,
        source_id TEXT NOT NULL REFERENCES sources(id),
        url TEXT NOT NULL,
        canonical_url TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        published_at TEXT,
        updated_at TEXT,
        fetched_at TEXT NOT NULL,
        content_hash TEXT NOT NULL,
        excerpt TEXT,
        matched_entities TEXT NOT NULL DEFAULT '',
        baseline INTEGER NOT NULL DEFAULT 0
    );
    CREATE INDEX items_content_hash ON items(content_hash);
    CREATE INDEX items_fetched_at ON items(fetched_at);
    CREATE TABLE events (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        first_published_at TEXT,
        first_seen_at TEXT NOT NULL,
        last_seen_at TEXT NOT NULL,
        level TEXT,
        token_mention TEXT NOT NULL DEFAULT 'unknown',
        stage_before TEXT,
        stage_after TEXT,
        summary TEXT,
        next_check TEXT,
        reviewed_by TEXT,
        review_note TEXT
    );
    CREATE INDEX events_last_seen ON events(last_seen_at);
    CREATE TABLE event_items (
        event_id INTEGER NOT NULL REFERENCES events(id),
        item_id INTEGER NOT NULL REFERENCES items(id),
        role TEXT NOT NULL,
        PRIMARY KEY (event_id, item_id)
    );
    CREATE TABLE event_entities (
        event_id INTEGER NOT NULL REFERENCES events(id),
        entity_id TEXT NOT NULL,
        kind TEXT NOT NULL,
        PRIMARY KEY (event_id, entity_id)
    );
    CREATE TABLE event_assets (
        event_id INTEGER NOT NULL REFERENCES events(id),
        symbol TEXT NOT NULL,
        directness TEXT NOT NULL DEFAULT 'unknown',
        evidence_quote TEXT,
        evidence_url TEXT,
        PRIMARY KEY (event_id, symbol)
    );
    CREATE TABLE alerts (
        id INTEGER PRIMARY KEY,
        created_at TEXT NOT NULL,
        level TEXT NOT NULL,
        event_id INTEGER REFERENCES events(id),
        source_id TEXT,
        message TEXT NOT NULL,
        url TEXT,
        delivered_via TEXT,
        delivered_at TEXT
    );
    CREATE TABLE runs (
        id INTEGER PRIMARY KEY,
        source_id TEXT NOT NULL,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        status TEXT NOT NULL,
        http_status INTEGER,
        items_seen INTEGER NOT NULL DEFAULT 0,
        items_new INTEGER NOT NULL DEFAULT 0,
        error TEXT
    );
    """,
    # 2: market data (local only; raw prices are never committed, AGENTS.md)
    """
    CREATE TABLE market_snapshots (
        venue TEXT NOT NULL,
        symbol TEXT NOT NULL,
        quote TEXT NOT NULL,
        ts TEXT NOT NULL,
        price REAL NOT NULL,
        acc_trade_value_24h REAL,
        PRIMARY KEY (venue, symbol, ts)
    );
    CREATE TABLE candles (
        venue TEXT NOT NULL,
        market TEXT NOT NULL,
        unit_min INTEGER NOT NULL,
        start_at TEXT NOT NULL,
        open REAL NOT NULL,
        high REAL NOT NULL,
        low REAL NOT NULL,
        close REAL NOT NULL,
        volume REAL,
        PRIMARY KEY (venue, market, unit_min, start_at)
    );
    CREATE TABLE price_reactions (
        event_id INTEGER NOT NULL REFERENCES events(id),
        symbol TEXT NOT NULL,
        window_name TEXT NOT NULL,
        venue TEXT NOT NULL,
        t_start TEXT NOT NULL,
        t_end TEXT NOT NULL,
        asset_return REAL,
        btc_return REAL,
        excess_return REAL,
        bucket_median_return REAL,
        status TEXT NOT NULL,
        computed_at TEXT NOT NULL,
        PRIMARY KEY (event_id, symbol, window_name)
    );
    """,
    # 3: delivery attempts, so undelivered alerts can be retried
    """
    ALTER TABLE alerts ADD COLUMN attempts INTEGER NOT NULL DEFAULT 0;
    CREATE INDEX alerts_undelivered ON alerts(delivered_at, created_at);
    """,
]


def connect(path: Path | str) -> sqlite3.Connection:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if str(path) != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")
    migrate(conn)
    return conn


def migrate(conn: sqlite3.Connection) -> int:
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    for index in range(version, len(MIGRATIONS)):
        # One transaction per migration, including the version bump.
        conn.executescript(
            f"BEGIN;\n{MIGRATIONS[index]}\nPRAGMA user_version = {index + 1};\nCOMMIT;")
    return len(MIGRATIONS)

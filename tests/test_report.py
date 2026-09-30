from datetime import datetime, timedelta, timezone

from collector import db
from collector.report import build_report
from collector.timeutil import to_iso

NOW = datetime(2026, 10, 7, 0, 0, tzinfo=timezone.utc)


def iso(minutes_ago: float) -> str:
    return to_iso(NOW - timedelta(minutes=minutes_ago))


def seeded():
    conn = db.connect(":memory:")
    conn.execute("""INSERT INTO sources (id, name, kind, url, poll_interval_sec, publisher_kind,
                                         consecutive_failures, last_error)
                    VALUES ('fed-press', 'Fed', 'feed', 'https://example.org/f', 600,
                            'regulator', 2, 'HTTP 503')""")
    for minutes_ago, status, new in [(600, "ok", 2), (590, "not_modified", 0), (20, "error", 0)]:
        conn.execute("""INSERT INTO runs (source_id, started_at, finished_at, status, items_new)
                        VALUES ('fed-press', ?, ?, ?, ?)""",
                     (iso(minutes_ago), iso(minutes_ago), status, new))
    # Published 30 and 90 minutes before being fetched: median delay 1h00m.
    for n, delay in [(1, 30), (2, 90)]:
        conn.execute("""INSERT INTO items (id, source_id, url, canonical_url, title, published_at,
                                           fetched_at, content_hash, baseline)
                        VALUES (?, 'fed-press', ?, ?, ?, ?, ?, ?, 0)""",
                     (n, f"https://example.org/{n}", f"example.org/{n}", f"Item {n}",
                      iso(600 + delay), iso(600), f"h{n}"))
    conn.execute("""INSERT INTO events (id, title, first_seen_at, last_seen_at, level)
                    VALUES (1, 'Bank pilots tokenized deposits with Chainlink', ?, ?, 'high'),
                           (2, 'Quiet theme item', ?, ?, NULL)""",
                 (iso(600), iso(600), iso(610), iso(610)))
    conn.execute("INSERT INTO event_items VALUES (1, 1, 'origin'), (2, 2, 'origin')")
    # An event built from the backlog at the first run is counted but not listed.
    conn.execute("""INSERT INTO items (id, source_id, url, canonical_url, title, fetched_at,
                                       content_hash, baseline)
                    VALUES (3, 'fed-press', 'https://example.org/old', 'example.org/old',
                            'Old item', ?, 'h3', 1)""", (iso(700),))
    conn.execute("""INSERT INTO events (id, title, first_seen_at, last_seen_at)
                    VALUES (3, 'Old backlog event', ?, ?)""", (iso(700), iso(700)))
    conn.execute("INSERT INTO event_items VALUES (3, 3, 'origin')")
    conn.execute("INSERT INTO event_entities VALUES (1, 'chainlink', 'project'), "
                 "(1, 'jpmorgan', 'institution')")
    conn.execute("""INSERT INTO price_reactions VALUES
                    (1, 'LINK', '1h', 'upbit', ?, ?, 0.05, 0.01, 0.04, NULL, 'measured', ?)""",
                 (iso(600), iso(540), iso(500)))
    # Market polls every 5 minutes, then nothing for two hours, then one more poll.
    for minutes_ago in (300, 295, 290, 170):
        conn.execute("INSERT INTO market_snapshots VALUES ('upbit', 'LINK', 'KRW', ?, 12345.67, "
                     "NULL)", (iso(minutes_ago),))
    conn.execute("""INSERT INTO alerts (created_at, level, event_id, source_id, message, url,
                                        delivered_via, delivered_at, attempts)
                    VALUES (?, 'high', 1, 'fed-press', 'first', 'u', 'telegram', ?, 1),
                           (?, 'high', 1, 'fed-press', 'again', 'u', NULL, NULL, 3),
                           (?, 'medium', NULL, 'market:upbit',
                            'LINK +4.0% vs BTC +0.5% over 60m (upbit KRW, excess +3.5%)',
                            NULL, 'telegram', ?, 1),
                           (?, 'test', NULL, NULL, 'collector notification test', NULL,
                            'telegram', ?, 1)""",
                 (iso(600), iso(600), iso(500), iso(290), iso(290), iso(5), iso(5)))
    conn.commit()
    return conn


def test_report_sections():
    text = build_report(seeded(), NOW, days=7)
    source = next(line for line in text.splitlines() if line.startswith("fed-press"))
    assert source.split()[1:5] == ["1", "1", "1", "0"]      # ok, 304, err, skip
    assert "1h00m" in source and "HTTP 503" in source
    assert "new events: 2 (high 1, medium 0, none 1); reviewed 0" in text
    assert "baseline events (backlog at a source's first run, not listed): 1" in text
    assert "Old backlog event" not in text
    assert text.index("#1 [high]") < text.index("#2 [-]")    # alerting events first
    assert "https://example.org/1" in text
    assert "LINK (upbit): 1h +5.0% (vs BTC +4.0%)" in text
    assert "alerts: 3 (news 2, market 1); undelivered 1" in text   # test alert excluded
    assert "events alerted more than once: #1 x2" in text
    assert "market alerts by symbol: LINK 1" in text


def test_report_lists_gaps_and_ongoing_outage():
    text = build_report(seeded(), NOW, days=7)
    # 290 -> 170 minutes ago is a 2h gap; 20 minutes ago -> now is exactly the limit.
    assert "2h00m" in text
    assert "gaps longer than 20m:" in text
    assert "market polls: upbit 4" in text


def test_report_never_prints_prices():
    assert "12345" not in build_report(seeded(), NOW, days=7)


def test_report_on_empty_database():
    text = build_report(db.connect(":memory:"), NOW, days=7)
    assert "no activity recorded in this period" in text
    assert "new events: 0" in text

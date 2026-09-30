"""Operating report for a period (docs/collector-spec.md section 9).

Plain text meant to be pasted into a chat with the user or an AI. It holds no
secrets: source ids, titles, links, error texts and return percentages only.
Raw prices are not printed (market data terms, docs/open-questions.md Q11).
Market ticker polls appear in the sources section as 'market:<venue>' rows
(counts and errors only).
"""

from __future__ import annotations

import sqlite3
import statistics
from datetime import datetime, timedelta

from .market.jobs import WINDOWS
from .timeutil import fmt_kst, from_iso, to_iso

MAX_EVENTS = 40
MAX_GAPS = 20
MAX_MARKET_ALERTS = 30
ERROR_CHARS = 120


def _duration(td: timedelta) -> str:
    minutes = int(td.total_seconds() // 60)
    if minutes < 60:
        return f"{minutes}m"
    hours, minutes = divmod(minutes, 60)
    if hours < 48:
        return f"{hours}h{minutes:02d}m"
    return f"{hours // 24}d{hours % 24:02d}h"


def reaction_lines(conn: sqlite3.Connection, event_id: int, indent: str = "    ") -> list[str]:
    rows = conn.execute(
        """SELECT symbol, venue, window_name, asset_return, excess_return, status
           FROM price_reactions WHERE event_id = ? ORDER BY symbol""", (event_id,)).fetchall()
    by_symbol: dict[str, dict[str, sqlite3.Row]] = {}
    for r in rows:
        by_symbol.setdefault(r["symbol"], {})[r["window_name"]] = r
    lines = []
    for symbol, windows in by_symbol.items():
        cells = []
        for name in WINDOWS:
            r = windows.get(name)
            if r is None:
                continue
            if r["status"] == "measured":
                cells.append(f"{name} {r['asset_return']:+.1%} (vs BTC {r['excess_return']:+.1%})")
            else:
                cells.append(f"{name} {r['status']}")
        venue = next(iter(windows.values()))["venue"]
        lines.append(f"{indent}{symbol} ({venue}): " + ", ".join(cells))
    return lines


def _sources(conn: sqlite3.Connection, since: str) -> list[str]:
    lines = ["## sources",
             f"{'source':<24} {'ok':>5} {'304':>5} {'err':>4} {'skip':>5} {'new':>5} "
             f"{'delay p50':>9} {'max':>7}  last error"]
    for s in conn.execute("SELECT * FROM sources WHERE enabled = 1 ORDER BY id"):
        runs = dict(conn.execute(
            """SELECT status, COUNT(*) FROM runs WHERE source_id = ? AND started_at >= ?
               GROUP BY status""", (s["id"], since)).fetchall())
        new = conn.execute(
            "SELECT COALESCE(SUM(items_new), 0) FROM runs WHERE source_id = ? AND started_at >= ?",
            (s["id"], since)).fetchone()[0]
        # Discovery delay: publication to first fetch, for items that could alert.
        delays = []
        for r in conn.execute(
                """SELECT published_at, fetched_at FROM items
                   WHERE source_id = ? AND fetched_at >= ? AND baseline = 0
                     AND published_at IS NOT NULL""", (s["id"], since)):
            delay = from_iso(r["fetched_at"]) - from_iso(r["published_at"])
            if delay >= timedelta(0):
                delays.append(delay)
        p50 = _duration(statistics.median(delays)) if delays else "-"
        worst = _duration(max(delays)) if delays else "-"
        error = ""
        if s["consecutive_failures"] or runs.get("skipped"):
            error = (s["last_error"] or "")[:ERROR_CHARS]
        lines.append(
            f"{s['id']:<24} {runs.get('ok', 0):>5} {runs.get('not_modified', 0):>5} "
            f"{runs.get('error', 0):>4} {runs.get('skipped', 0):>5} {new:>5} "
            f"{p50:>9} {worst:>7}  {error}")
    lines.extend(_market_sources(conn, since))
    return lines


def _market_sources(conn: sqlite3.Connection, since: str) -> list[str]:
    """Ticker polls per venue (runs rows 'market:<venue>'). Columns that only
    apply to news sources show '-'; the error is the last one in the period,
    with its time, even if later polls succeeded."""
    lines = []
    ids = [r[0] for r in conn.execute(
        """SELECT DISTINCT source_id FROM runs WHERE source_id GLOB 'market:*'
               AND started_at >= ? ORDER BY source_id""", (since,))]
    for source_id in ids:
        runs = dict(conn.execute(
            """SELECT status, COUNT(*) FROM runs WHERE source_id = ? AND started_at >= ?
               GROUP BY status""", (source_id, since)).fetchall())
        last = conn.execute(
            """SELECT started_at, error FROM runs WHERE source_id = ? AND started_at >= ?
                   AND status = 'error' ORDER BY started_at DESC, id DESC LIMIT 1""",
            (source_id, since)).fetchone()
        error = ""
        if last:
            error = f"{fmt_kst(last['started_at'])} {(last['error'] or '')[:ERROR_CHARS]}"
        lines.append(
            f"{source_id:<24} {runs.get('ok', 0):>5} {'-':>5} {runs.get('error', 0):>4} "
            f"{'-':>5} {'-':>5} {'-':>9} {'-':>7}  {error}".rstrip())
    return lines


def market_status(conn: sqlite3.Connection, venue: str) -> dict:
    """Latest health of one venue's ticker polls, for `collector status`."""
    source_id = f"market:{venue}"
    last_ok = conn.execute(
        "SELECT MAX(started_at) FROM runs WHERE source_id = ? AND status = 'ok'",
        (source_id,)).fetchone()[0]
    failures = conn.execute(
        """SELECT COUNT(*) FROM runs WHERE source_id = ? AND status = 'error'
               AND started_at > ?""", (source_id, last_ok or "")).fetchone()[0]
    last_error = conn.execute(
        """SELECT error FROM runs WHERE source_id = ? AND status = 'error'
           ORDER BY started_at DESC, id DESC LIMIT 1""", (source_id,)).fetchone()
    return {"id": source_id, "last_ok_at": last_ok, "failures": failures,
            "last_error": last_error[0] if last_error else None}


def _gaps(conn: sqlite3.Connection, since: datetime, now: datetime,
          gap: timedelta) -> list[str]:
    """Periods in which nothing was collected: the collector was stopped, asleep
    or offline. Only successful work counts (runs that ended ok or 304, stored
    market snapshots). Failed runs do not: market polls write an error row
    every 5 minutes, which would hide an offline period."""
    stamps = sorted({from_iso(r[0]) for r in conn.execute(
        """SELECT started_at FROM runs
            WHERE started_at >= ? AND status IN ('ok', 'not_modified')
           UNION SELECT ts FROM market_snapshots WHERE ts >= ?""",
        (to_iso(since), to_iso(since)))})
    lines = ["## coverage"]
    if not stamps:
        return lines + ["no activity recorded in this period"]
    lines.append(f"first activity: {fmt_kst(stamps[0])}, last activity: {fmt_kst(stamps[-1])}")
    gaps = [(a, b) for a, b in zip(stamps, stamps[1:]) if b - a > gap]
    if now - stamps[-1] > gap:
        gaps.append((stamps[-1], now))
    total = sum((b - a for a, b in gaps), timedelta(0))
    lines.append(f"gaps longer than {_duration(gap)}: {len(gaps)} (total {_duration(total)})")
    for a, b in gaps[:MAX_GAPS]:
        ongoing = " (ongoing)" if b == now else ""
        lines.append(f"  {fmt_kst(a)} ~ {fmt_kst(b)}  {_duration(b - a)}{ongoing}")
    if len(gaps) > MAX_GAPS:
        lines.append(f"  ... {len(gaps) - MAX_GAPS} more")
    for r in conn.execute(
            """SELECT venue, COUNT(DISTINCT ts) AS polls FROM market_snapshots
               WHERE ts >= ? GROUP BY venue ORDER BY venue""", (to_iso(since),)):
        lines.append(f"market polls: {r['venue']} {r['polls']}")
    return lines


def _events(conn: sqlite3.Connection, since: str) -> list[str]:
    rows = conn.execute(
        """SELECT e.*,
                  (SELECT group_concat(entity_id, ',') FROM event_entities
                    WHERE event_id = e.id AND kind != 'theme') AS entities,
                  (SELECT COUNT(*) FROM event_items WHERE event_id = e.id) AS n_items,
                  (SELECT COUNT(*) FROM event_items
                    WHERE event_id = e.id AND role = 'rerun') AS n_rerun,
                  (SELECT i.url FROM event_items ei JOIN items i ON i.id = ei.item_id
                    WHERE ei.event_id = e.id AND ei.role = 'origin') AS origin_url,
                  (SELECT i.source_id FROM event_items ei JOIN items i ON i.id = ei.item_id
                    WHERE ei.event_id = e.id AND ei.role = 'origin') AS origin_source,
                  (SELECT i.baseline FROM event_items ei JOIN items i ON i.id = ei.item_id
                    WHERE ei.event_id = e.id AND ei.role = 'origin') AS origin_baseline
           FROM events e WHERE e.first_seen_at >= ? ORDER BY e.first_seen_at""",
        (since,)).fetchall()
    # Events built from a source's backlog at its first run are old news: count only.
    baseline = sum(1 for r in rows if r["origin_baseline"])
    rows = [r for r in rows if not r["origin_baseline"]]
    levels: dict[str, int] = {}
    for r in rows:
        levels[r["level"] or "none"] = levels.get(r["level"] or "none", 0) + 1
    reviewed = sum(1 for r in rows if r["reviewed_by"])
    lines = ["## events",
             f"new events: {len(rows)} "
             f"(high {levels.get('high', 0)}, medium {levels.get('medium', 0)}, "
             f"none {levels.get('none', 0)}); reviewed {reviewed}; "
             f"with reruns {sum(1 for r in rows if r['n_rerun'])}"]
    if baseline:
        lines.append(f"baseline events (backlog at a source's first run, not listed): {baseline}")
    # Alerting events first, so the list stays useful when it is cut off.
    ordered = sorted(rows, key=lambda r: (r["level"] is None, r["first_seen_at"]))
    for r in ordered[:MAX_EVENTS]:
        lines.append(f"#{r['id']} [{r['level'] or '-'}] {fmt_kst(r['first_seen_at'])} "
                     f"{r['origin_source'] or ''} items={r['n_items']} rerun={r['n_rerun']}"
                     f"{' reviewed' if r['reviewed_by'] else ''}")
        lines.append(f"    {r['title']}")
        lines.append(f"    entities: {r['entities'] or ''}")
        if r["origin_url"]:
            lines.append(f"    {r['origin_url']}")
        lines.extend(reaction_lines(conn, r["id"]))
    if len(rows) > MAX_EVENTS:
        lines.append(f"... {len(rows) - MAX_EVENTS} more (collector events --days N)")
    return lines


def _alerts(conn: sqlite3.Connection, since: str) -> list[str]:
    rows = conn.execute("SELECT * FROM alerts WHERE created_at >= ? AND level != 'test'",
                        (since,)).fetchall()
    news = [r for r in rows if not (r["source_id"] or "").startswith("market:")]
    market = [r for r in rows if (r["source_id"] or "").startswith("market:")]
    undelivered = [r for r in rows if not r["delivered_at"]]
    lines = ["## alerts",
             f"alerts: {len(rows)} (news {len(news)}, market {len(market)}); "
             f"undelivered {len(undelivered)}"]
    by_event: dict[int, int] = {}
    for r in news:
        if r["event_id"] is not None:
            by_event[r["event_id"]] = by_event.get(r["event_id"], 0) + 1
    repeated = {k: v for k, v in by_event.items() if v > 1}
    if repeated:
        lines.append("events alerted more than once: "
                     + ", ".join(f"#{k} x{v}" for k, v in sorted(repeated.items())))
    by_symbol: dict[str, int] = {}
    for r in market:
        symbol = r["message"].split(" ", 1)[0]
        by_symbol[symbol] = by_symbol.get(symbol, 0) + 1
    if by_symbol:
        lines.append("market alerts by symbol: "
                     + ", ".join(f"{k} {v}" for k, v in sorted(by_symbol.items())))
    for r in market[:MAX_MARKET_ALERTS]:
        lines.append(f"  {fmt_kst(r['created_at'])} {r['message']}")
    if len(market) > MAX_MARKET_ALERTS:
        lines.append(f"  ... {len(market) - MAX_MARKET_ALERTS} more market alerts")
    for r in undelivered:
        lines.append(f"  undelivered #{r['id']} {fmt_kst(r['created_at'])} "
                     f"attempts={r['attempts']} {r['message'][:80]}")
    return lines


def build_report(conn: sqlite3.Connection, now: datetime, days: int = 7,
                 gap: timedelta = timedelta(minutes=20)) -> str:
    since = now - timedelta(days=days)
    since_iso = to_iso(since)
    lines = [f"# collector report {fmt_kst(since)} ~ {fmt_kst(now)} ({days}d)", ""]
    for section in (_sources(conn, since_iso), _gaps(conn, since, now, gap),
                    _events(conn, since_iso), _alerts(conn, since_iso)):
        lines.extend(section)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

"""Command line entry point: python -m collector <command>."""

from __future__ import annotations

import argparse
import logging
import logging.handlers
import sys
import time
from datetime import timedelta
from pathlib import Path

from . import db
from .config import ConfigError, load_entities, load_settings, load_sources
from .fetch import Fetcher
from .heartbeat import Heartbeat
from .notify import make_notifier
from .pipeline import Context, due_sources, run_source, sync_sources
from .review import ReviewError, review_event
from .timeutil import fmt_kst, to_iso, utcnow

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
TICK_SEC = 30


def _setup_logging(log_path: Path, verbose: bool) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [
        logging.handlers.RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5,
                                             encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ]
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                        handlers=handlers)


def _load(root: Path):
    settings = load_settings(root)
    sources = load_sources(root / "config" / "sources.yaml")
    entities = load_entities(root / "config" / "entities.yaml")
    return settings, sources, entities


def _context(root: Path, verbose: bool):
    settings, sources, entities = _load(root)
    _setup_logging(settings.log_path, verbose)
    conn = db.connect(settings.db_path)
    sync_sources(conn, sources)
    ctx = Context(
        settings=settings,
        conn=conn,
        fetcher=Fetcher(settings.user_agent),
        entities=entities,
        notifier=make_notifier(settings.notifier),
        heartbeat=Heartbeat(settings.heartbeat_url, settings.user_agent)
        if settings.heartbeat_url else None,
    )
    return ctx, sources


def cmd_check_config(args) -> int:
    settings, sources, entities = _load(args.root)
    print(f"sources: {len(sources)} ({sum(s.enabled for s in sources)} enabled)")
    for s in sources:
        note = ""
        if s.requires_env and not settings.env(s.requires_env):
            note = f"  [skipped: {s.requires_env} not set]"
        print(f"  {s.id:<24} {s.kind:<8} every {s.interval_sec}s  {'on' if s.enabled else 'off'}"
              f"{note}")
    kinds: dict[str, int] = {}
    for e in entities:
        kinds[e.kind] = kinds.get(e.kind, 0) + 1
    print("entities:", ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    return 0


def cmd_once(args) -> int:
    ctx, sources = _context(args.root, args.verbose)
    targets = [s for s in sources if s.enabled and (not args.source or s.id in args.source)]
    for source in targets:
        run_source(ctx, source)
    return 0


def cmd_run(args) -> int:
    ctx, sources = _context(args.root, args.verbose)
    logging.getLogger("collector").info("collector started with %d sources", len(sources))
    while True:
        for source in due_sources(ctx.conn, sources, ctx.clock()):
            run_source(ctx, source)
        if ctx.heartbeat:
            ctx.heartbeat.beat(ctx.clock())
        time.sleep(TICK_SEC)


def cmd_status(args) -> int:
    settings, _, _ = _load(args.root)
    conn = db.connect(settings.db_path)
    rows = conn.execute("SELECT * FROM sources ORDER BY id").fetchall()
    print(f"{'source':<24} {'last ok':<22} {'fails':>5}  last error")
    for r in rows:
        if not r["enabled"]:
            continue
        print(f"{r['id']:<24} {fmt_kst(r['last_ok_at']):<22} {r['consecutive_failures']:>5}  "
              f"{r['last_error'] or ''}")
    counts = conn.execute(
        "SELECT (SELECT COUNT(*) FROM items), (SELECT COUNT(*) FROM events), "
        "(SELECT COUNT(*) FROM alerts)").fetchone()
    print(f"items={counts[0]} events={counts[1]} alerts={counts[2]}")
    return 0


def cmd_events(args) -> int:
    settings, _, _ = _load(args.root)
    conn = db.connect(settings.db_path)
    since = to_iso(utcnow() - timedelta(days=args.days))
    rows = conn.execute(
        """SELECT e.*,
                  (SELECT group_concat(entity_id, ',') FROM event_entities
                    WHERE event_id = e.id AND kind != 'theme') AS entities,
                  (SELECT group_concat(symbol, ',') FROM event_assets
                    WHERE event_id = e.id) AS symbols,
                  (SELECT COUNT(*) FROM event_items WHERE event_id = e.id) AS n_items,
                  (SELECT COUNT(*) FROM event_items
                    WHERE event_id = e.id AND role = 'rerun') AS n_rerun
           FROM events e WHERE e.last_seen_at >= ? ORDER BY e.first_seen_at DESC""",
        (since,)).fetchall()
    for r in rows:
        print(f"#{r['id']} [{r['level'] or '-'}] {fmt_kst(r['first_seen_at'])} "
              f"items={r['n_items']} rerun={r['n_rerun']} {r['symbols'] or ''}")
        print(f"    {r['title']}")
        print(f"    entities: {r['entities'] or ''}")
    if not rows:
        print("no events")
    return 0


def cmd_items(args) -> int:
    settings, _, _ = _load(args.root)
    conn = db.connect(settings.db_path)
    since = to_iso(utcnow() - timedelta(days=args.days))
    query = "SELECT * FROM items WHERE fetched_at >= ?"
    params: list = [since]
    if args.entity:
        query += " AND (',' || matched_entities || ',') LIKE ?"
        params.append(f"%,{args.entity},%")
    elif not args.all:
        query += " AND matched_entities != ''"
    rows = conn.execute(query + " ORDER BY fetched_at DESC LIMIT ?",
                        (*params, args.limit)).fetchall()
    for r in rows:
        print(f"{fmt_kst(r['published_at'] or r['updated_at'] or r['fetched_at'])} "
              f"[{r['matched_entities'] or '-'}] {r['title']}")
        print(f"    {r['url']}")
    if not rows:
        print("no items")
    return 0


def cmd_review(args) -> int:
    settings, _, _ = _load(args.root)
    conn = db.connect(settings.db_path)
    directness = {}
    for pair in args.directness or []:
        symbol, _, grade = pair.partition("=")
        if not grade:
            print(f"--directness expects SYMBOL=GRADE, got {pair!r}", file=sys.stderr)
            return 2
        directness[symbol] = grade
    try:
        review_event(conn, args.event_id, directness=directness,
                     evidence_url=args.evidence_url, evidence_quote=args.evidence_quote,
                     stage_before=args.stage_before, stage_after=args.stage_after,
                     next_check=args.next_check, note=args.note, reviewer=args.reviewer)
    except ReviewError as exc:
        print(f"review error: {exc}", file=sys.stderr)
        return 2
    print(f"event #{args.event_id} updated")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="collector")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                        help="repository root (config/ and .env live here)")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check-config", help="validate config/*.yaml and .env").set_defaults(
        func=cmd_check_config)
    once = sub.add_parser("once", help="poll every enabled source once")
    once.add_argument("--source", action="append", help="limit to this source id")
    once.set_defaults(func=cmd_once)
    sub.add_parser("run", help="poll sources on their schedules until stopped").set_defaults(
        func=cmd_run)
    sub.add_parser("status", help="show per-source health").set_defaults(func=cmd_status)
    events = sub.add_parser("events", help="list recent events")
    events.add_argument("--days", type=int, default=7)
    events.set_defaults(func=cmd_events)
    items = sub.add_parser("items", help="list stored items (matched ones by default)")
    items.add_argument("--days", type=int, default=7)
    items.add_argument("--entity", help="only items that matched this entity id")
    items.add_argument("--all", action="store_true", help="include unmatched items")
    items.add_argument("--limit", type=int, default=50)
    items.set_defaults(func=cmd_items)
    review = sub.add_parser("review", help="record a review of an event")
    review.add_argument("event_id", type=int)
    review.add_argument("--directness", action="append", metavar="SYMBOL=GRADE",
                        help="unknown, direct, project_claim, indirect or association")
    review.add_argument("--evidence-url")
    review.add_argument("--evidence-quote")
    review.add_argument("--stage-before")
    review.add_argument("--stage-after")
    review.add_argument("--next-check")
    review.add_argument("--note")
    review.add_argument("--reviewer", default="human", choices=["human", "ai"])
    review.set_defaults(func=cmd_review)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())

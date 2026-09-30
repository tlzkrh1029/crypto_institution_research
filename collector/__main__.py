"""Command line entry point: python -m collector <command>."""

from __future__ import annotations

import argparse
import logging
import logging.handlers
import os
import sys
import time
from datetime import timedelta
from pathlib import Path

from . import db
from .config import ConfigError, load_entities, load_settings, load_sources, validate
from .fetch import Fetcher
from .heartbeat import Heartbeat
from .market.jobs import load_market_config
from .market.runner import MarketRunner, make_clients
from .notify import Alert, NotifierConfigError, make_notifier, telegram_chats
from .pipeline import (Context, deliver_alert, due_sources, retry_undelivered, run_source,
                       sync_sources)
from .report import build_report, reaction_lines
from .review import ReviewError, review_event
from .timeutil import fmt_kst, to_iso, utcnow

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
TICK_SEC = 30
RETRY_EVERY = timedelta(minutes=5)


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
    validate(sources, entities)
    return settings, sources, entities


def _context(root: Path, verbose: bool):
    settings, sources, entities = _load(root)
    market_cfg = load_market_config(root / "config" / "market.yaml")
    _setup_logging(settings.log_path, verbose)
    conn = db.connect(settings.db_path)
    sync_sources(conn, sources)
    ctx = Context(
        settings=settings,
        conn=conn,
        fetcher=Fetcher(settings.user_agent),
        entities=entities,
        notifier=make_notifier(settings.notifier, settings.env),
        heartbeat=Heartbeat(settings.heartbeat_url, settings.user_agent)
        if settings.heartbeat_url else None,
    )
    market = MarketRunner(ctx, market_cfg, make_clients(market_cfg, settings.user_agent))
    return ctx, sources, market


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
    market = load_market_config(args.root / "config" / "market.yaml")
    for v in market.venues:
        print(f"market: {v.name} {'on' if v.enabled else 'off'}, {v.quote} "
              f"{', '.join(v.symbols)} vs {v.reference}")
    print(f"anomaly: {market.anomaly_excess_pct}%p vs reference over "
          f"{market.anomaly_window_min}m")
    # Only whether values are set; the token itself is never printed.
    flags = {name: "set" if settings.env(name) else "not set"
             for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "HEARTBEAT_URL")}
    print(f"notifier: {settings.notifier} (telegram token {flags['TELEGRAM_BOT_TOKEN']}, "
          f"chat id {flags['TELEGRAM_CHAT_ID']})")
    print(f"heartbeat: {flags['HEARTBEAT_URL']}")
    make_notifier(settings.notifier, settings.env)  # raises on a missing token or chat id
    return 0


def cmd_once(args) -> int:
    ctx, sources, _ = _context(args.root, args.verbose)
    targets = [s for s in sources if s.enabled and (not args.source or s.id in args.source)]
    for source in targets:
        run_source(ctx, source)
    return 0


def cmd_run(args) -> int:
    ctx, sources, market = _context(args.root, args.verbose)
    logging.getLogger("collector").info("collector started with %d sources", len(sources))
    log = logging.getLogger("collector")
    last_retry = ctx.clock()
    while True:
        # One failing source or job must not stop the others.
        for source in due_sources(ctx.conn, sources, ctx.clock()):
            try:
                run_source(ctx, source)
            except Exception:
                log.exception("unexpected error in source %s", source.id)
        try:
            market.tick(ctx.clock())
        except Exception:
            log.exception("unexpected error in market jobs")
        now = ctx.clock()
        if now - last_retry >= RETRY_EVERY:
            last_retry = now
            try:
                retry_undelivered(ctx, now)
            except Exception:
                log.exception("unexpected error while retrying alerts")
        if ctx.heartbeat:
            ctx.heartbeat.beat(ctx.clock())
        time.sleep(TICK_SEC)


def cmd_market(args) -> int:
    ctx, _, market = _context(args.root, args.verbose)
    if not market.clients:
        print("market data is disabled in config/market.yaml")
        return 0
    now = ctx.clock()
    alerts = 0
    for venue in market.cfg.enabled_venues:
        alerts += market.run_tickers(venue.name, now)
    rows = ctx.conn.execute(
        "SELECT venue, symbol, quote, price, ts FROM market_snapshots WHERE ts = ? "
        "ORDER BY venue, symbol", (to_iso(now),)).fetchall()
    for r in rows:
        print(f"{r['venue']:<7} {r['symbol']:<6} {r['price']:>16,.2f} {r['quote']}  "
              f"{fmt_kst(r['ts'])}")
    print(f"anomaly alerts: {alerts}")
    return 0


def cmd_reactions(args) -> int:
    ctx, _, market = _context(args.root, args.verbose)
    now = ctx.clock()
    written = market.run_reactions(now, args.event or None)
    print(f"rows written: {written}")
    return 0


def cmd_telegram_chat_id(args) -> int:
    settings, _, _ = _load(args.root)
    token = settings.env("TELEGRAM_BOT_TOKEN")
    if not token:
        print("TELEGRAM_BOT_TOKEN is not set in .env", file=sys.stderr)
        return 2
    chats = telegram_chats(token)
    if not chats:
        print("no messages yet: open the bot in Telegram, press Start (or send any "
              "message), then run this command again")
        return 1
    for chat in chats:
        print(f"TELEGRAM_CHAT_ID={chat['id']}   ({chat['type']} {chat['name']})")
    return 0


def cmd_notify_test(args) -> int:
    ctx, _, _ = _context(args.root, args.verbose)
    alert = Alert(level="test", message="collector notification test",
                  url="https://github.com/tlzkrh1029/crypto_institution_research")
    deliver_alert(ctx, alert, ctx.clock())
    row = ctx.conn.execute(
        "SELECT delivered_via FROM alerts ORDER BY id DESC LIMIT 1").fetchone()
    if row["delivered_via"]:
        print(f"sent via {row['delivered_via']}")
        return 0
    print("not delivered; see data/collector.log", file=sys.stderr)
    return 1


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
        for line in reaction_lines(conn, r["id"]):
            print(line)
    if not rows:
        print("no events")
    return 0


def cmd_report(args) -> int:
    settings, _, _ = _load(args.root)
    conn = db.connect(settings.db_path)
    print(build_report(conn, utcnow(), days=args.days), end="")
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
    report = sub.add_parser("report", help="operating report for the last N days (to paste)")
    report.add_argument("--days", type=int, default=7)
    report.set_defaults(func=cmd_report)
    sub.add_parser("telegram-chat-id", help="show chat ids that messaged the bot").set_defaults(
        func=cmd_telegram_chat_id)
    sub.add_parser("notify-test", help="send a test alert through NOTIFIER").set_defaults(
        func=cmd_notify_test)
    sub.add_parser("market", help="poll venue tickers once and show prices").set_defaults(
        func=cmd_market)
    reactions = sub.add_parser("reactions", help="compute price reactions for recent events")
    reactions.add_argument("--event", type=int, action="append", help="only this event id")
    reactions.set_defaults(func=cmd_reactions)
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
    except (ConfigError, NotifierConfigError) as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 0
    except BrokenPipeError:  # output piped into head/less that closed early
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0


if __name__ == "__main__":
    sys.exit(main())

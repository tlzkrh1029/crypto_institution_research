from datetime import timedelta

from collector.fetch import FetchError
from collector.pipeline import backoff_seconds, due_sources, run_source

from .conftest import FIXTURES, make_source

RSS = (FIXTURES / "rss_sample.xml").read_bytes()
ATOM = (FIXTURES / "atom_sample.xml").read_bytes()


def rss(*items: str) -> bytes:
    body = "".join(
        f"<item><title>{title}</title><link>{link}</link><pubDate>{date}</pubDate>"
        f"<description>{desc}</description></item>" for title, link, date, desc in items)
    return f'<?xml version="1.0"?><rss version="2.0"><channel><title>t</title>{body}' \
           f"</channel></rss>".encode()


TCH_QUANT = ("The Clearing House Partners with Quant on Tokenized Deposits",
             "https://wire-a.example/tch-quant", "Thu, 24 Sep 2026 14:00:00 GMT",
             "Quant will power clearing and settlement.")


def test_first_run_is_a_silent_baseline(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("wire", "https://wire.example/rss")
    register(source)
    fetcher.set(source.url, RSS)
    outcome = run_source(ctx, source)
    assert outcome.status == "ok" and outcome.items_new == 5
    assert outcome.events_new == 1          # TCH + Quant; false positives create nothing
    assert notifier.alerts == []            # baseline: no alert burst
    matched = ctx.conn.execute(
        "SELECT title, matched_entities FROM items WHERE matched_entities != ''").fetchall()
    assert {r["title"] for r in matched} == {
        "The Clearing House Partners with Quant to Advance the On-Chain Money Initiative",
        "Banks Explore Tokenized Deposits for Cross-Border Payments",
    }


def test_new_item_after_baseline_alerts_once(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("wire", "https://wire.example/rss")
    register(source)
    fetcher.set(source.url, rss())
    run_source(ctx, source)                  # empty baseline
    fetcher.set(source.url, rss(TCH_QUANT))
    outcome = run_source(ctx, source)
    assert outcome.alerts == 1
    alert = notifier.alerts[0]
    assert alert.level == "high" and "(QNT)" in alert.message
    row = ctx.conn.execute("SELECT delivered_via FROM alerts").fetchone()
    assert row["delivered_via"] == "test"
    # The same item again is ignored.
    assert run_source(ctx, source).items_new == 0
    assert len(notifier.alerts) == 1


def test_same_story_on_second_wire_is_a_duplicate(harness):
    ctx, fetcher, notifier, clock, register = harness
    a = make_source("wire_a", "https://wire-a.example/rss")
    b = make_source("wire_b", "https://wire-b.example/rss")
    register(a, b)
    for s in (a, b):
        fetcher.set(s.url, rss())
        run_source(ctx, s)
    fetcher.set(a.url, rss(TCH_QUANT))
    run_source(ctx, a)
    fetcher.set(b.url, rss(("Quant Selected by The Clearing House for Tokenized Deposits",
                            "https://wire-b.example/quant-tch",
                            "Thu, 24 Sep 2026 15:00:00 GMT", "")))
    outcome = run_source(ctx, b)
    assert outcome.events_new == 0 and outcome.alerts == 0
    roles = [r["role"] for r in ctx.conn.execute("SELECT role FROM event_items ORDER BY item_id")]
    assert roles == ["origin", "duplicate"]


def test_late_recirculation_is_marked_rerun(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("wire", "https://wire.example/rss")
    register(source)
    fetcher.set(source.url, rss())
    run_source(ctx, source)
    fetcher.set(source.url, rss(TCH_QUANT))
    run_source(ctx, source)
    clock.now += timedelta(days=20)
    fetcher.set(source.url, rss(
        ("Recap: The Clearing House and Quant Tokenized Deposits Network",
         "https://wire.example/recap", "Wed, 14 Oct 2026 09:00:00 GMT", "")))
    run_source(ctx, source)
    roles = [r["role"] for r in ctx.conn.execute("SELECT role FROM event_items ORDER BY item_id")]
    assert roles == ["origin", "rerun"]
    assert len(notifier.alerts) == 1


def test_stale_item_is_recorded_without_alert(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("wire", "https://wire.example/rss")
    register(source)
    fetcher.set(source.url, rss())
    run_source(ctx, source)
    clock.now += timedelta(days=10)
    fetcher.set(source.url, rss(TCH_QUANT))   # published 2026-09-24, found 10 days later
    outcome = run_source(ctx, source)
    assert outcome.events_new == 1 and outcome.alerts == 0


def test_regulator_feed_project_mention_is_medium(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("reg", "https://example.gov/feed", publisher_kind="regulator")
    register(source)
    fetcher.set(source.url, rss())
    run_source(ctx, source)
    clock.now = clock.now.replace(day=28, hour=13)
    fetcher.set(source.url, ATOM)
    run_source(ctx, source)
    assert [a.level for a in notifier.alerts] == ["medium"]


def test_error_backoff_and_recovery(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("wire", "https://wire.example/rss")
    register(source)
    fetcher.set(source.url, error=FetchError("HTTP 503", 503))
    assert run_source(ctx, source).status == "error"
    assert run_source(ctx, source).status == "error"
    row = ctx.conn.execute("SELECT * FROM sources WHERE id = 'wire'").fetchone()
    assert row["consecutive_failures"] == 2 and row["last_error"] == "HTTP 503"
    assert due_sources(ctx.conn, [source], clock.now) == []
    assert due_sources(ctx.conn, [source], clock.now + timedelta(seconds=1200)) == [source]
    fetcher.set(source.url, rss())
    assert run_source(ctx, source).status == "ok"
    row = ctx.conn.execute("SELECT * FROM sources WHERE id = 'wire'").fetchone()
    assert row["consecutive_failures"] == 0 and row["last_ok_at"] is not None


def test_backoff_is_capped():
    assert backoff_seconds(300, 1) == 600
    assert backoff_seconds(300, 20) == 300 * 2 ** 6
    assert backoff_seconds(3600, 20) == 6 * 3600


def test_not_modified_and_etag(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("wire", "https://wire.example/rss")
    register(source)
    fetcher.set(source.url, rss(), etag='"v1"')
    run_source(ctx, source)
    fetcher.set(source.url, None, status=304)
    assert run_source(ctx, source).status == "not_modified"
    assert fetcher.calls[-1]["etag"] == '"v1"'


def test_source_needing_env_is_skipped(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("sec", "https://example.gov/feed", requires_env="SEC_USER_AGENT")
    register(source)
    outcome = run_source(ctx, source)
    assert outcome.status == "skipped" and fetcher.calls == []


def test_sitemap_source(harness):
    ctx, fetcher, notifier, clock, register = harness
    import re
    source = make_source("dtcc", "https://www.example-dtcc.com/sitemap.xml", kind="sitemap",
                         publisher_kind="institution", url_filter=re.compile(r"/press-releases/"),
                         max_age_days=60)
    register(source)
    fetcher.set(source.url, (FIXTURES / "sitemap_sample.xml").read_bytes())
    outcome = run_source(ctx, source)
    assert outcome.items_new == 1 and outcome.events_new == 1
    entities = {r["entity_id"] for r in ctx.conn.execute("SELECT entity_id FROM event_entities")}
    assert {"dtcc", "ondo"} <= entities


def test_institution_name_alone_is_not_an_event(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("wire", "https://wire.example/rss")
    register(source)
    fetcher.set(source.url, rss())
    run_source(ctx, source)
    fetcher.set(source.url, rss(
        ("DTCC Launches Centralized Hub to Simplify Client Onboarding",
         "https://wire.example/dtcc-hub", "Thu, 24 Sep 2026 20:00:00 GMT", ""),
        ("DTCC Outlines Tokenization Roadmap for Collateral",
         "https://wire.example/dtcc-tokenization", "Thu, 24 Sep 2026 21:00:00 GMT", "")))
    outcome = run_source(ctx, source)
    assert outcome.items_new == 2 and outcome.events_new == 1   # only the one with a theme
    event = ctx.conn.execute("SELECT * FROM events").fetchone()
    assert event["title"].startswith("DTCC Outlines Tokenization") and event["level"] is None
    assert notifier.alerts == []


def test_publisher_entity_turns_project_mention_into_high(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("dtcc", "https://dtcc.example/rss", publisher_kind="institution",
                         publisher_entity="dtcc", store_excerpt=False)
    register(source)
    fetcher.set(source.url, rss())
    run_source(ctx, source)
    fetcher.set(source.url, rss(
        ("Collateral AppChain Integrates Chainlink Runtime Environment",
         "https://dtcc.example/appchain", "Thu, 24 Sep 2026 20:00:00 GMT",
         "A longer excerpt that must not be stored.")))
    run_source(ctx, source)
    assert [a.level for a in notifier.alerts] == ["high"]
    item = ctx.conn.execute("SELECT excerpt, matched_entities FROM items").fetchone()
    assert item["excerpt"] == "" and item["matched_entities"].startswith("dtcc,")

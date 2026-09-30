import pytest

from collector.pipeline import run_source
from collector.review import ReviewError, review_event

from .conftest import make_source
from .test_pipeline import TCH_QUANT, rss


def _event(harness):
    ctx, fetcher, notifier, clock, register = harness
    source = make_source("wire", "https://wire.example/rss")
    register(source)
    fetcher.set(source.url, rss(TCH_QUANT))
    run_source(ctx, source)
    return ctx.conn, ctx.conn.execute("SELECT id FROM events").fetchone()["id"]


def test_review_sets_grade_stage_and_reviewer(harness):
    conn, event_id = _event(harness)
    review_event(conn, event_id, directness={"qnt": "direct"},
                 evidence_url="https://example.com/tch", stage_after="선정·협약",
                 next_check="TCH participant list", note="institution release")
    event = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    asset = conn.execute("SELECT * FROM event_assets WHERE event_id = ?", (event_id,)).fetchone()
    assert (asset["symbol"], asset["directness"]) == ("QNT", "direct")
    assert asset["evidence_url"] == "https://example.com/tch"
    assert event["stage_after"] == "선정·협약" and event["reviewed_by"] == "human"


def test_review_rejects_unknown_values(harness):
    conn, event_id = _event(harness)
    with pytest.raises(ReviewError):
        review_event(conn, event_id, directness={"QNT": "strong"})
    with pytest.raises(ReviewError):
        review_event(conn, event_id, stage_after="launched")
    with pytest.raises(ReviewError):
        review_event(conn, 999)

import re
from datetime import datetime, timezone

import pytest

from collector.normalize import canonical_url, jaccard, title_from_slug, title_tokens
from collector.sources import EXCERPT_LIMIT
from collector.sources.feeds import FeedParseError, parse_feed
from collector.sources.sitemap import parse_sitemap

from .conftest import FIXTURES


def test_canonical_url_drops_tracking_and_fragment():
    assert canonical_url("HTTPS://Example.com/a/b/?utm_source=x&id=3#top") == \
        "https://example.com/a/b?id=3"


def test_title_from_slug():
    url = "https://x.com/press-releases/2026/DTCC-FundSERV-Adds-Ondo-Finance-as-First-Member"
    assert title_from_slug(url) == "DTCC FundSERV Adds Ondo Finance as First Member"


def test_jaccard_similar_titles():
    a = title_tokens("The Clearing House Partners with Quant on Tokenized Deposits")
    b = title_tokens("Quant Selected by The Clearing House for Tokenized Deposits Network")
    assert jaccard(a, b) >= 0.4


def test_parse_rss():
    items = parse_feed((FIXTURES / "rss_sample.xml").read_bytes())
    assert len(items) == 5
    first = items[0]
    assert first.title.startswith("The Clearing House Partners with Quant")
    assert first.published_at == datetime(2026, 9, 24, 14, 0, tzinfo=timezone.utc)
    assert "<p>" not in first.excerpt and len(first.excerpt) <= EXCERPT_LIMIT


def test_parse_atom():
    items = parse_feed((FIXTURES / "atom_sample.xml").read_bytes())
    assert len(items) == 1
    assert items[0].link == "https://example.gov/news/statement-collateral"
    assert items[0].updated_at == datetime(2026, 9, 28, 12, 30, tzinfo=timezone.utc)


def test_parse_feed_rejects_garbage():
    with pytest.raises(FeedParseError):
        parse_feed(b"<<< not xml")


def test_parse_sitemap_filters_and_ages():
    now = datetime(2026, 9, 30, tzinfo=timezone.utc)
    items = parse_sitemap((FIXTURES / "sitemap_sample.xml").read_bytes(),
                          re.compile(r"/press-releases/"), now, max_age_days=60)
    assert [i.title for i in items] == [
        "DTCC FundSERV Adds Ondo Finance as First Tokenization Member"]
    assert items[0].published_at is None
    assert items[0].updated_at == datetime(2026, 9, 16, 10, 0, tzinfo=timezone.utc)

"""RSS and Atom feeds."""

from __future__ import annotations

import feedparser

from ..normalize import clean_text
from ..timeutil import from_struct_time
from . import EXCERPT_LIMIT, RawItem


class FeedParseError(ValueError):
    pass


def parse_feed(content: bytes) -> list[RawItem]:
    parsed = feedparser.parse(content)
    if parsed.bozo and not parsed.entries:
        raise FeedParseError(f"unparseable feed: {parsed.get('bozo_exception')!r}")
    items: list[RawItem] = []
    for entry in parsed.entries:
        link = entry.get("link")
        title = clean_text(entry.get("title"))
        if not link or not title:
            continue
        items.append(RawItem(
            title=title,
            link=link,
            # dict.get skips feedparser's deprecated updated->published fallback.
            published_at=from_struct_time(dict.get(entry, "published_parsed")),
            updated_at=from_struct_time(dict.get(entry, "updated_parsed")),
            excerpt=clean_text(entry.get("summary"), EXCERPT_LIMIT),
        ))
    return items

"""XML sitemaps (e.g. DTCC press releases, which have no RSS feed)."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from ..normalize import title_from_slug
from ..timeutil import parse_w3c
from . import RawItem

_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class SitemapParseError(ValueError):
    pass


def parse_sitemap(content: bytes, url_filter: re.Pattern | None, now: datetime,
                  max_age_days: int | None = None) -> list[RawItem]:
    """Return one item per matching <url>. The title comes from the URL slug.

    lastmod is stored as updated_at; sitemaps carry no publication time.
    """
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise SitemapParseError(str(exc)) from exc
    cutoff = now - timedelta(days=max_age_days) if max_age_days else None
    items: list[RawItem] = []
    for node in root.findall("sm:url", _NS):
        loc = (node.findtext("sm:loc", default="", namespaces=_NS) or "").strip()
        if not loc or (url_filter is not None and not url_filter.search(loc)):
            continue
        lastmod = parse_w3c(node.findtext("sm:lastmod", default=None, namespaces=_NS))
        if cutoff is not None and (lastmod is None or lastmod < cutoff):
            continue
        items.append(RawItem(
            title=title_from_slug(loc),
            link=loc,
            published_at=None,
            updated_at=lastmod,
            excerpt="",
        ))
    return items

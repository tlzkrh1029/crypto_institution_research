"""UTC timestamp helpers. Storage is UTC ISO 8601; display is KST."""

from __future__ import annotations

import calendar
import time
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9), "KST")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def to_iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def from_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def from_struct_time(value: time.struct_time | None) -> datetime | None:
    """feedparser returns *_parsed fields as UTC struct_time."""
    if value is None:
        return None
    return datetime.fromtimestamp(calendar.timegm(value), tz=timezone.utc)


def parse_w3c(value: str | None) -> datetime | None:
    """Parse a sitemap <lastmod> value (W3C datetime, date or full timestamp)."""
    if not value:
        return None
    value = value.strip()
    try:
        if len(value) == 10:
            return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def fmt_kst(value: str | datetime | None) -> str:
    if value is None:
        return "-"
    dt = from_iso(value) if isinstance(value, str) else value
    return dt.astimezone(KST).strftime("%Y-%m-%d %H:%M KST")

"""Parsers that turn a fetched document into RawItem records."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

EXCERPT_LIMIT = 300  # docs/collector-spec.md section 4: short excerpts only


@dataclass(frozen=True)
class RawItem:
    title: str
    link: str
    published_at: datetime | None
    updated_at: datetime | None
    excerpt: str

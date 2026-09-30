"""URL canonicalization, title normalization and title similarity."""

from __future__ import annotations

import hashlib
import html
import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_PARAMS = re.compile(r"^(utm_|fbclid$|gclid$|mc_cid$|mc_eid$|ref$|cmpid$)")
_TAGS = re.compile(r"<[^>]+>")
_SPACES = re.compile(r"\s+")
_WORDS = re.compile(r"[a-z0-9]+")
STOPWORDS = frozenset(
    "the a an and or of to for in on at by with from as is are be its it this that "
    "new announces announced launches launch partners partnership inc llc ltd corp "
    "company group first".split()
)


def canonical_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not TRACKING_PARAMS.match(k.lower())]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


def clean_text(value: str | None, limit: int | None = None) -> str:
    if not value:
        return ""
    text = html.unescape(_TAGS.sub(" ", value))
    text = unicodedata.normalize("NFKC", text)
    text = _SPACES.sub(" ", text).strip()
    if limit is not None and len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def title_tokens(title: str) -> frozenset[str]:
    words = _WORDS.findall(clean_text(title).lower())
    return frozenset(w for w in words if len(w) >= 3 and w not in STOPWORDS)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def content_hash(title: str) -> str:
    return hashlib.sha1(" ".join(sorted(title_tokens(title))).encode()).hexdigest()


def title_from_slug(url: str) -> str:
    """Turn '/press-releases/2026/DTCC-FundSERV-Adds-Ondo' into a readable title."""
    slug = urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
    slug = re.sub(r"\.(html?|aspx)$", "", slug)
    return clean_text(re.sub(r"[-_]+", " ", slug))

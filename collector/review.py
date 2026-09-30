"""Record a human review of an event: connection grade per token, business stage,
next check and a note (docs/research-principles.md sections 2 and 4)."""

from __future__ import annotations

import sqlite3

DIRECTNESS = {"unknown", "direct", "project_claim", "indirect", "association"}
STAGES = {"선정·협약 전", "선정·협약", "시험", "가동", "실제 고객·거래액", "반복 수입", "토큰 수요",
          "재확산", "확인 필요"}


class ReviewError(ValueError):
    pass


def review_event(conn: sqlite3.Connection, event_id: int, *,
                 directness: dict[str, str] | None = None,
                 evidence_url: str | None = None, evidence_quote: str | None = None,
                 stage_before: str | None = None, stage_after: str | None = None,
                 next_check: str | None = None, note: str | None = None,
                 reviewer: str = "human") -> None:
    if not conn.execute("SELECT 1 FROM events WHERE id = ?", (event_id,)).fetchone():
        raise ReviewError(f"no event #{event_id}")
    for stage in (stage_before, stage_after):
        if stage is not None and stage not in STAGES:
            raise ReviewError(f"unknown stage {stage!r}; use one of {sorted(STAGES)}")
    if reviewer not in {"human", "ai"}:
        raise ReviewError("reviewer must be 'human' or 'ai'")
    with conn:
        for symbol, grade in (directness or {}).items():
            if grade not in DIRECTNESS:
                raise ReviewError(f"unknown directness {grade!r}; use one of {sorted(DIRECTNESS)}")
            conn.execute(
                """INSERT INTO event_assets (event_id, symbol, directness, evidence_quote,
                                             evidence_url)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(event_id, symbol) DO UPDATE SET
                       directness = excluded.directness,
                       evidence_quote = COALESCE(excluded.evidence_quote, evidence_quote),
                       evidence_url = COALESCE(excluded.evidence_url, evidence_url)""",
                (event_id, symbol.upper(), grade, evidence_quote, evidence_url),
            )
        updates = {"stage_before": stage_before, "stage_after": stage_after,
                   "next_check": next_check, "review_note": note}
        for column, value in updates.items():
            if value is not None:
                conn.execute(f"UPDATE events SET {column} = ? WHERE id = ?", (value, event_id))
        conn.execute("UPDATE events SET reviewed_by = ? WHERE id = ?", (reviewer, event_id))

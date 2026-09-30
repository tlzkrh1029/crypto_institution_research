"""Match item text against the entity list (config/entities.yaml).

Matching only proposes candidates. The connection grade and business stage
(docs/research-principles.md sections 2 and 4) are decided later by review.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import Entity


@dataclass(frozen=True)
class Match:
    entity_id: str
    kind: str
    label: str
    tokens: tuple[str, ...]
    text: str
    control: bool = False


def match_text(text: str, entities: list[Entity]) -> list[Match]:
    """Return at most one match per entity, in entity-list order."""
    matches: list[Match] = []
    for entity in entities:
        for rule in entity.rules:
            found = rule.pattern.search(text)
            if not found:
                continue
            if rule.requires is not None and not rule.requires.search(text):
                continue
            matches.append(Match(
                entity_id=entity.id,
                kind=entity.kind,
                label=entity.label,
                tokens=entity.tokens,
                text=found.group(0),
                control=entity.control,
            ))
            break
    return matches


def publisher_match(entity_id: str, entities: list[Entity]) -> Match:
    """A feed published by an institution speaks for that institution."""
    for entity in entities:
        if entity.id == entity_id:
            return Match(entity.id, entity.kind, entity.label, entity.tokens, "(publisher)",
                         entity.control)
    raise KeyError(f"publisher_entity {entity_id!r} is not in the entity list")


@dataclass(frozen=True)
class Assessment:
    institutions: tuple[str, ...]
    projects: tuple[str, ...]
    themes: tuple[str, ...]
    tokens: tuple[str, ...]
    level: str | None  # "high", "medium" or None (record only)

    @property
    def makes_event(self) -> bool:
        """Projects always; institutions only together with a theme.

        An institution name alone (e.g. every post in DTCC's own feed) is kept
        as an item but does not become an event.
        """
        return bool(self.projects or (self.institutions and self.themes))


def assess(matches: list[Match], publisher_kind: str) -> Assessment:
    """Decide how loudly to report a new event (docs/collector-spec.md section 6).

    high:   an institution and a project/token appear together
            (a candidate for docs/institution-map.md).
    medium: a project/token appears in a source published by an institution
            or a regulator.
    None:   stored for the dashboard and later review only.
    """
    institutions = tuple(m.entity_id for m in matches if m.kind == "institution")
    projects = tuple(m.entity_id for m in matches if m.kind == "project")
    themes = tuple(m.entity_id for m in matches if m.kind == "theme")
    tokens = tuple(sorted({t for m in matches for t in m.tokens}))
    level = None
    if institutions and projects:
        level = "high"
    elif projects and publisher_kind in {"institution", "regulator"}:
        level = "medium"
    return Assessment(institutions, projects, themes, tokens, level)

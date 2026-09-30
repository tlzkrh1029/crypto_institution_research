"""Settings (.env), source list and entity list (config/*.yaml)."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DEFAULT_USER_AGENT = (
    "crypto_institution_research-collector/0.1 "
    "(+https://github.com/tlzkrh1029/crypto_institution_research)"
)
SOURCE_KINDS = {"feed", "sitemap"}
ENTITY_KINDS = {"institution", "project", "theme"}
MIN_INTERVAL_SEC = 60


class ConfigError(ValueError):
    pass


# --- .env -------------------------------------------------------------------

def load_dotenv(path: Path) -> dict[str, str]:
    """Minimal KEY=VALUE reader. Existing environment variables win."""
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


@dataclass(frozen=True)
class Settings:
    root: Path
    user_agent: str
    sec_user_agent: str
    heartbeat_url: str
    data_dir: Path
    notifier: str
    file_values: dict[str, str] = field(default_factory=dict, repr=False)

    @property
    def db_path(self) -> Path:
        return self.data_dir / "collector.db"

    @property
    def log_path(self) -> Path:
        return self.data_dir / "collector.log"

    def env(self, name: str, default: str = "") -> str:
        return os.environ.get(name) or self.file_values.get(name) or default


def load_settings(root: Path) -> Settings:
    file_values = load_dotenv(root / ".env")

    def get(name: str, default: str = "") -> str:
        return os.environ.get(name) or file_values.get(name) or default

    data_dir = Path(get("COLLECTOR_DATA_DIR", "data"))
    if not data_dir.is_absolute():
        data_dir = root / data_dir
    return Settings(
        root=root,
        user_agent=get("COLLECTOR_USER_AGENT", DEFAULT_USER_AGENT),
        sec_user_agent=get("SEC_USER_AGENT"),
        heartbeat_url=get("HEARTBEAT_URL"),
        data_dir=data_dir,
        notifier=get("NOTIFIER", "log"),
        file_values=file_values,
    )


# --- sources ----------------------------------------------------------------

@dataclass(frozen=True)
class SourceConfig:
    id: str
    name: str
    kind: str
    url: str
    interval_sec: int
    publisher_kind: str
    terms_checked: str
    enabled: bool = True
    requires_env: str | None = None
    url_filter: re.Pattern | None = None
    max_age_days: int | None = None
    store_excerpt: bool = True
    publisher_entity: str | None = None


def load_sources(path: Path) -> list[SourceConfig]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    sources: list[SourceConfig] = []
    seen: set[str] = set()
    for raw in data.get("sources", []):
        try:
            sid = raw["id"]
            kind = raw["kind"]
            if kind not in SOURCE_KINDS:
                raise ConfigError(f"{sid}: unknown kind {kind!r}")
            if sid in seen:
                raise ConfigError(f"duplicate source id {sid!r}")
            interval = int(raw.get("interval_sec", 300))
            if interval < MIN_INTERVAL_SEC:
                raise ConfigError(f"{sid}: interval_sec must be >= {MIN_INTERVAL_SEC}")
            if not raw.get("terms_checked"):
                raise ConfigError(
                    f"{sid}: terms_checked is required (AGENTS.md: check terms before implementing)")
            url_filter = raw.get("url_filter")
            sources.append(SourceConfig(
                id=sid,
                name=raw["name"],
                kind=kind,
                url=raw["url"],
                interval_sec=interval,
                publisher_kind=raw.get("publisher_kind", "unknown"),
                terms_checked=str(raw["terms_checked"]),
                enabled=bool(raw.get("enabled", True)),
                requires_env=raw.get("requires_env"),
                url_filter=re.compile(url_filter) if url_filter else None,
                max_age_days=raw.get("max_age_days"),
                store_excerpt=bool(raw.get("store_excerpt", True)),
                publisher_entity=raw.get("publisher_entity"),
            ))
            seen.add(sid)
        except KeyError as exc:
            raise ConfigError(f"source entry missing field {exc}: {raw}") from exc
    return sources


def validate(sources: list[SourceConfig], entities: list["Entity"]) -> None:
    known = {e.id for e in entities}
    for s in sources:
        if s.publisher_entity and s.publisher_entity not in known:
            raise ConfigError(f"{s.id}: publisher_entity {s.publisher_entity!r} "
                              "is not in config/entities.yaml")


# --- entities ---------------------------------------------------------------

@dataclass(frozen=True)
class MatchRule:
    pattern: re.Pattern
    requires: re.Pattern | None = None


@dataclass(frozen=True)
class Entity:
    id: str
    kind: str
    label: str
    rules: tuple[MatchRule, ...]
    tokens: tuple[str, ...] = field(default_factory=tuple)
    control: bool = False


def _compile(pattern: str, ignore_case: bool) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE if ignore_case else 0)


def load_entities(path: Path) -> list[Entity]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    entities: list[Entity] = []
    seen: set[str] = set()
    for raw in data.get("entities", []):
        eid = raw["id"]
        kind = raw["kind"]
        if kind not in ENTITY_KINDS:
            raise ConfigError(f"{eid}: unknown kind {kind!r}")
        if eid in seen:
            raise ConfigError(f"duplicate entity id {eid!r}")
        rules = []
        for rule in raw.get("match", []):
            ignore_case = bool(rule.get("ignore_case", False))
            try:
                pattern = _compile(rule["pattern"], ignore_case)
                requires = rule.get("requires")
                rules.append(MatchRule(
                    pattern=pattern,
                    # Context words are matched case-insensitively.
                    requires=_compile(requires, True) if requires else None,
                ))
            except re.error as exc:
                raise ConfigError(f"{eid}: bad regex: {exc}") from exc
        if not rules:
            raise ConfigError(f"{eid}: at least one match rule is required")
        entities.append(Entity(
            id=eid,
            kind=kind,
            label=raw.get("label", eid),
            rules=tuple(rules),
            tokens=tuple(raw.get("tokens", [])),
            control=bool(raw.get("control", False)),
        ))
        seen.add(eid)
    return entities

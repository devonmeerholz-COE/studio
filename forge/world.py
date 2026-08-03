"""Canonical world domain model for Forge."""

from __future__ import annotations

from dataclasses import dataclass
import re


_STABLE_KEY_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def _require_nonblank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonblank")


def _require_nonempty_texts(name: str, values: tuple[str, ...]) -> None:
    if not values:
        raise ValueError(f"{name} must not be empty")
    for value in values:
        _require_nonblank(f"{name} entry", value)


@dataclass(frozen=True, slots=True)
class Era:
    lines: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_nonempty_texts("lines", self.lines)


@dataclass(frozen=True, slots=True)
class Beacon:
    identity: str
    emotional_purpose: str
    natural_aging: str

    def __post_init__(self) -> None:
        _require_nonblank("identity", self.identity)
        _require_nonblank("emotional_purpose", self.emotional_purpose)
        _require_nonblank("natural_aging", self.natural_aging)


@dataclass(frozen=True, slots=True)
class BonsaiRelationship:
    identity: str
    life_stage: str
    beacon_relationship: str

    def __post_init__(self) -> None:
        _require_nonblank("identity", self.identity)
        _require_nonblank("life_stage", self.life_stage)
        _require_nonblank("beacon_relationship", self.beacon_relationship)


@dataclass(frozen=True, slots=True)
class Soundscape:
    music: str
    ambient_world: str
    silence: str

    def __post_init__(self) -> None:
        _require_nonblank("music", self.music)
        _require_nonblank("ambient_world", self.ambient_world)
        _require_nonblank("silence", self.silence)


@dataclass(frozen=True, slots=True)
class World:
    stable_key: str
    canonical_name: str
    catalog_number: int
    chronological_stage: int
    era: Era
    purpose: str
    resident_identity: str
    emotional_core: tuple[str, ...]
    first_impression: str
    leaving_this_world: tuple[str, ...]
    setting: str
    beacon: Beacon
    bonsai_relationship: BonsaiRelationship
    soundscape: Soundscape
    personal_artifacts: tuple[str, ...]
    passage_of_time: str
    immutable_elements: tuple[str, ...]
    motto: str | None = None
    naming_note: str | None = None

    def __post_init__(self) -> None:
        _require_nonblank("stable_key", self.stable_key)
        if _STABLE_KEY_PATTERN.fullmatch(self.stable_key) is None:
            raise ValueError("stable_key must use lowercase kebab-case")

        _require_nonblank("canonical_name", self.canonical_name)
        if self.catalog_number <= 0:
            raise ValueError("catalog_number must be positive")
        if self.chronological_stage <= 0:
            raise ValueError("chronological_stage must be positive")

        _require_nonblank("purpose", self.purpose)
        _require_nonblank("resident_identity", self.resident_identity)
        _require_nonempty_texts("emotional_core", self.emotional_core)
        _require_nonblank("first_impression", self.first_impression)
        _require_nonempty_texts("leaving_this_world", self.leaving_this_world)
        _require_nonblank("setting", self.setting)
        _require_nonempty_texts("personal_artifacts", self.personal_artifacts)
        _require_nonblank("passage_of_time", self.passage_of_time)
        _require_nonempty_texts("immutable_elements", self.immutable_elements)

        if self.motto is not None:
            _require_nonblank("motto", self.motto)
        if self.naming_note is not None:
            _require_nonblank("naming_note", self.naming_note)

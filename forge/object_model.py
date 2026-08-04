"""Canonical Studio object domain model for Forge."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


_STABLE_ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def _require_nonblank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonblank")


def _require_stable_id(name: str, value: str) -> None:
    _require_nonblank(name, value)
    if _STABLE_ID_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} must use lowercase kebab-case")


def _require_nonempty_texts(name: str, values: tuple[str, ...]) -> None:
    if not values:
        raise ValueError(f"{name} must not be empty")
    for value in values:
        _require_nonblank(f"{name} entry", value)


class ObjectCategory(str, Enum):
    CANON = "Canon"
    BEACON = "Beacon"
    IDENTITY = "Identity"
    TOOL = "Tool"
    MEMORY = "Memory"


class RecognitionLevel(str, Enum):
    IMMEDIATE = "Immediate"
    FAMILIAR = "Familiar"
    SUBTLE = "Subtle"
    HIDDEN = "Hidden"


@dataclass(frozen=True, slots=True)
class WorldMoment:
    world_key: str
    description: str

    def __post_init__(self) -> None:
        _require_stable_id("world_key", self.world_key)
        _require_nonblank("description", self.description)


def _require_nonempty_moments(
    name: str,
    values: tuple[WorldMoment, ...],
) -> None:
    if not values:
        raise ValueError(f"{name} must not be empty")
    for value in values:
        if not isinstance(value, WorldMoment):
            raise ValueError(f"{name} entries must be WorldMoment instances")


@dataclass(frozen=True, slots=True)
class StudioObject:
    canonical_name: str
    canonical_id: str
    category: ObjectCategory
    recognition_level: RecognitionLevel
    first_appearance: WorldMoment
    purpose: tuple[str, ...]
    studio_rules: str
    evolution: tuple[WorldMoment, ...]
    continuity_notes: str
    appearances: tuple[WorldMoment, ...]

    def __post_init__(self) -> None:
        _require_nonblank("canonical_name", self.canonical_name)
        _require_stable_id("canonical_id", self.canonical_id)

        if not isinstance(self.category, ObjectCategory):
            raise ValueError("category must be an ObjectCategory")
        if not isinstance(self.recognition_level, RecognitionLevel):
            raise ValueError("recognition_level must be a RecognitionLevel")
        if not isinstance(self.first_appearance, WorldMoment):
            raise ValueError("first_appearance must be a WorldMoment")

        _require_nonempty_texts("purpose", self.purpose)
        _require_nonblank("studio_rules", self.studio_rules)
        _require_nonempty_moments("evolution", self.evolution)
        _require_nonblank("continuity_notes", self.continuity_notes)
        _require_nonempty_moments("appearances", self.appearances)

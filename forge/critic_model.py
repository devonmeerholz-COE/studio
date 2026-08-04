"""Immutable domain model for Studio artwork critique."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re

from forge.world import World


_STABLE_ID_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def _require_nonblank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonblank")


def _require_stable_id(name: str, value: str) -> None:
    _require_nonblank(name, value)
    if _STABLE_ID_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} must use lowercase kebab-case")


def _require_texts(name: str, values: tuple[str, ...]) -> None:
    for value in values:
        _require_nonblank(f"{name} entry", value)


class FindingKind(str, Enum):
    ALIGNED = "aligned"
    CONFLICT = "conflict"
    UNVERIFIED = "unverified"
    ADVISORY = "advisory"


class CameraBehavior(str, Enum):
    UNKNOWN = "unknown"
    STATIONARY = "stationary"
    MOVING = "moving"


class EvidenceState(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    UNKNOWN = "unknown"


class ReadableTextUse(str, Enum):
    NATURAL = "natural"
    SLOGAN = "slogan"
    DECORATIVE = "decorative"
    EXPOSITION = "exposition"
    GIBBERISH = "gibberish"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ContinuityClaim:
    object_id: str
    prior_world_key: str

    def __post_init__(self) -> None:
        _require_stable_id("object_id", self.object_id)
        _require_stable_id("prior_world_key", self.prior_world_key)


@dataclass(frozen=True, slots=True)
class ImmutableElementEvidence:
    canonical_text: str
    state: EvidenceState

    def __post_init__(self) -> None:
        _require_nonblank("canonical_text", self.canonical_text)
        if not isinstance(self.state, EvidenceState):
            raise ValueError("state must be an EvidenceState")


@dataclass(frozen=True, slots=True)
class ReadableTextEvidence:
    description: str
    use: ReadableTextUse

    def __post_init__(self) -> None:
        _require_nonblank("description", self.description)
        if not isinstance(self.use, ReadableTextUse):
            raise ValueError("use must be a ReadableTextUse")


@dataclass(frozen=True, slots=True)
class AdvisoryEvidence:
    principle: str
    observation: str

    def __post_init__(self) -> None:
        _require_nonblank("principle", self.principle)
        _require_nonblank("observation", self.observation)


@dataclass(frozen=True, slots=True)
class ArtworkEvidence:
    world_key: str
    artwork_id: str | None = None
    camera_behavior: CameraBehavior = CameraBehavior.UNKNOWN
    present_object_ids: tuple[str, ...] = ()
    absent_object_ids: tuple[str, ...] = ()
    continuity_claims: tuple[ContinuityClaim, ...] = ()
    immutable_elements: tuple[ImmutableElementEvidence, ...] = ()
    readable_text: tuple[ReadableTextEvidence, ...] = ()
    advisory_observations: tuple[AdvisoryEvidence, ...] = ()

    def __post_init__(self) -> None:
        _require_stable_id("world_key", self.world_key)
        if self.artwork_id is not None:
            _require_nonblank("artwork_id", self.artwork_id)
        if not isinstance(self.camera_behavior, CameraBehavior):
            raise ValueError("camera_behavior must be a CameraBehavior")

        for name, values in (
            ("present_object_ids", self.present_object_ids),
            ("absent_object_ids", self.absent_object_ids),
        ):
            for value in values:
                _require_stable_id(f"{name} entry", value)
            if len(set(values)) != len(values):
                raise ValueError(f"{name} must not contain duplicates")

        overlap = set(self.present_object_ids) & set(self.absent_object_ids)
        if overlap:
            raise ValueError("an object cannot be both present and absent")

        expected_types = (
            ("continuity_claims", self.continuity_claims, ContinuityClaim),
            ("immutable_elements", self.immutable_elements, ImmutableElementEvidence),
            ("readable_text", self.readable_text, ReadableTextEvidence),
            ("advisory_observations", self.advisory_observations, AdvisoryEvidence),
        )
        for name, values, expected_type in expected_types:
            if any(not isinstance(value, expected_type) for value in values):
                raise ValueError(f"{name} entries must be {expected_type.__name__} instances")


@dataclass(frozen=True, slots=True)
class CritiqueFinding:
    kind: FindingKind
    subject: str
    observation: str
    canonical_expectation: str
    principle: str
    world_key: str | None = None
    object_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, FindingKind):
            raise ValueError("kind must be a FindingKind")
        for name in (
            "subject",
            "observation",
            "canonical_expectation",
            "principle",
        ):
            _require_nonblank(name, getattr(self, name))
        if self.world_key is not None:
            _require_stable_id("world_key", self.world_key)
        if self.object_id is not None:
            _require_stable_id("object_id", self.object_id)


@dataclass(frozen=True, slots=True)
class Critique:
    world: World
    findings: tuple[CritiqueFinding, ...]
    world_keeper_questions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.world, World):
            raise ValueError("world must be a World")
        if any(not isinstance(value, CritiqueFinding) for value in self.findings):
            raise ValueError("findings entries must be CritiqueFinding instances")
        _require_texts("world_keeper_questions", self.world_keeper_questions)

    def findings_of_kind(self, kind: FindingKind) -> tuple[CritiqueFinding, ...]:
        if not isinstance(kind, FindingKind):
            raise ValueError("kind must be a FindingKind")
        return tuple(finding for finding in self.findings if finding.kind is kind)

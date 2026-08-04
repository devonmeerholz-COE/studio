"""Load the Studio's strict human-authored artwork evidence format."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re

from forge.critic_model import (
    AdvisoryEvidence,
    ArtworkEvidence,
    CameraBehavior,
    ContinuityClaim,
    EvidenceState,
    ImmutableElementEvidence,
    ReadableTextEvidence,
    ReadableTextUse,
)


MAX_EVIDENCE_BYTES = 1024 * 1024
_BACKTICK_VALUE = re.compile(r"`([^`]+)`")


class EvidenceLoadError(ValueError):
    """An artwork evidence document could not be loaded safely."""


@dataclass(frozen=True, slots=True)
class EvidenceDocument:
    evidence: ArtworkEvidence
    created: str


class _Parser:
    def __init__(self, text: str) -> None:
        self.lines = text.splitlines()
        self.index = 0

    def error(self, message: str) -> EvidenceLoadError:
        return EvidenceLoadError(f"line {self.index + 1}: {message}")

    def current(self) -> str | None:
        return self.lines[self.index] if self.index < len(self.lines) else None

    def expect(self, expected: str) -> None:
        actual = self.current()
        if actual != expected:
            shown = "end of file" if actual is None else repr(actual)
            raise self.error(f"expected {expected!r}, found {shown}")
        self.index += 1

    def blank(self) -> None:
        self.expect("")

    def field(self, label: str) -> str:
        prefix = f"{label}: "
        line = self.current()
        if line is None or not line.startswith(prefix):
            raise self.error(f"expected {label!r} field")
        value = line[len(prefix):]
        self.index += 1
        return value

    def backtick_field(self, label: str) -> str:
        raw = self.field(label)
        match = _BACKTICK_VALUE.fullmatch(raw)
        if match is None:
            raise self.error(f"{label} must contain one backtick-wrapped value")
        return match.group(1)

    def enum_field(self, label: str, enum_type):
        value = self.backtick_field(label)
        try:
            return enum_type(value)
        except ValueError as error:
            choices = ", ".join(item.value for item in enum_type)
            raise self.error(f"{label} must be one of: {choices}") from error

    def text_block(self, label: str) -> str:
        self.expect(f"{label}:")
        self.blank()
        self.expect("```text")
        values = []
        while self.current() is not None and self.current() != "```":
            values.append(self.current())
            self.index += 1
        self.expect("```")
        value = "\n".join(values)
        if not value.strip():
            raise self.error(f"{label} text must be nonblank")
        return value

    def id_collection(self) -> tuple[str, ...]:
        if self.current() == "None supplied.":
            self.index += 1
            return ()
        values = []
        while self.current() is not None and self.current().startswith("- "):
            raw = self.current()[2:]
            match = _BACKTICK_VALUE.fullmatch(raw)
            if match is None:
                raise self.error("object IDs must be backtick-wrapped bullet values")
            values.append(match.group(1))
            self.index += 1
        if not values:
            raise self.error("expected an object ID bullet or 'None supplied.'")
        return tuple(values)


def _parse_document(text: str) -> EvidenceDocument:
    parser = _Parser(text)
    parser.expect("# SUPER CHILLED STUDIO")
    parser.blank()
    parser.expect("# ARTWORK EVIDENCE")
    parser.blank()

    version = parser.field("Evidence Format Version")
    if version != "1":
        raise parser.error("Evidence Format Version must be 1")
    created = parser.backtick_field("Created")
    try:
        date.fromisoformat(created)
    except ValueError as error:
        raise parser.error("Created must be a valid YYYY-MM-DD date") from error
    parser.blank()

    parser.expect("## Artwork")
    parser.blank()
    world_key = parser.backtick_field("World key")
    artwork_raw = parser.field("Artwork ID")
    if artwork_raw == "Not supplied.":
        artwork_id = None
    else:
        match = _BACKTICK_VALUE.fullmatch(artwork_raw)
        if match is None:
            raise parser.error("Artwork ID must be backtick-wrapped or 'Not supplied.'")
        artwork_id = match.group(1)
    parser.blank()

    parser.expect("## Camera Behavior")
    parser.blank()
    camera_raw = parser.current()
    match = _BACKTICK_VALUE.fullmatch(camera_raw or "")
    if match is None:
        raise parser.error("Camera Behavior must contain one backtick-wrapped value")
    parser.index += 1
    try:
        camera_behavior = CameraBehavior(match.group(1))
    except ValueError as error:
        choices = ", ".join(item.value for item in CameraBehavior)
        raise parser.error(f"Camera Behavior must be one of: {choices}") from error
    parser.blank()

    parser.expect("## Confirmed Present Objects")
    parser.blank()
    present_object_ids = parser.id_collection()
    parser.blank()

    parser.expect("## Confirmed Absent Objects")
    parser.blank()
    absent_object_ids = parser.id_collection()
    parser.blank()

    parser.expect("## Continuity Claims")
    parser.blank()
    continuity_claims = []
    if parser.current() == "None supplied.":
        parser.index += 1
        parser.blank()
    else:
        while parser.current() == "### Claim":
            parser.index += 1
            parser.blank()
            continuity_claims.append(
                ContinuityClaim(
                    parser.backtick_field("Object ID"),
                    parser.backtick_field("Prior world key"),
                )
            )
            parser.blank()
        if not continuity_claims:
            raise parser.error("expected '### Claim' or 'None supplied.'")

    parser.expect("## Immutable Elements")
    parser.blank()
    immutable_elements = []
    if parser.current() == "None supplied.":
        parser.index += 1
        parser.blank()
    else:
        while parser.current() == "### Evidence":
            parser.index += 1
            parser.blank()
            state = parser.enum_field("State", EvidenceState)
            parser.blank()
            canonical_text = parser.text_block("Canonical text")
            immutable_elements.append(ImmutableElementEvidence(canonical_text, state))
            parser.blank()
        if not immutable_elements:
            raise parser.error("expected '### Evidence' or 'None supplied.'")

    parser.expect("## Readable Text")
    parser.blank()
    readable_text = []
    if parser.current() == "None supplied.":
        parser.index += 1
        parser.blank()
    else:
        while parser.current() == "### Evidence":
            parser.index += 1
            parser.blank()
            use = parser.enum_field("Use", ReadableTextUse)
            parser.blank()
            description = parser.text_block("Description")
            readable_text.append(ReadableTextEvidence(description, use))
            parser.blank()
        if not readable_text:
            raise parser.error("expected '### Evidence' or 'None supplied.'")

    parser.expect("## Advisory Observations")
    parser.blank()
    advisory_observations = []
    if parser.current() == "None supplied.":
        parser.index += 1
    else:
        while parser.current() == "### Observation":
            parser.index += 1
            parser.blank()
            principle = parser.text_block("Principle")
            parser.blank()
            observation = parser.text_block("Observation")
            advisory_observations.append(AdvisoryEvidence(principle, observation))
            if parser.current() == "":
                parser.index += 1
        if not advisory_observations:
            raise parser.error("expected '### Observation' or 'None supplied.'")

    if parser.current() is not None:
        raise parser.error(f"unexpected content {parser.current()!r}")

    try:
        evidence = ArtworkEvidence(
            world_key=world_key,
            artwork_id=artwork_id,
            camera_behavior=camera_behavior,
            present_object_ids=present_object_ids,
            absent_object_ids=absent_object_ids,
            continuity_claims=tuple(continuity_claims),
            immutable_elements=tuple(immutable_elements),
            readable_text=tuple(readable_text),
            advisory_observations=tuple(advisory_observations),
        )
    except ValueError as error:
        raise EvidenceLoadError(str(error)) from error
    return EvidenceDocument(evidence=evidence, created=created)


def load_evidence(path: str | Path) -> EvidenceDocument:
    resolved = Path(path).resolve()
    try:
        if not resolved.is_file():
            raise EvidenceLoadError(f"evidence file does not exist: {resolved}")
        if resolved.stat().st_size > MAX_EVIDENCE_BYTES:
            raise EvidenceLoadError("evidence file exceeds the 1 MiB size limit")
        text = resolved.read_text(encoding="utf-8")
    except EvidenceLoadError:
        raise
    except UnicodeDecodeError as error:
        raise EvidenceLoadError(f"evidence file is not valid UTF-8: {resolved}") from error
    except OSError as error:
        raise EvidenceLoadError(f"could not read evidence file {resolved}: {error}") from error
    return _parse_document(text)

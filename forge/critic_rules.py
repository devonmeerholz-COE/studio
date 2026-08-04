"""Deterministic canon rules and advisory observations for the Studio Critic."""

from __future__ import annotations

from forge.critic_model import (
    ArtworkEvidence,
    CameraBehavior,
    CritiqueFinding,
    EvidenceState,
    FindingKind,
    ReadableTextUse,
)
from forge.object_model import StudioObject
from forge.world import World


_REQUIRED_OBJECTS = {
    "hacker-apartment": ("protagonist-bonsai",),
    "midnight-library": ("protagonist-bonsai", "library-desk-lamp"),
    "coffee-cafe": ("coffee-cafe-house-bonsai", "coffee-pot"),
    "rainy-loft": ("protagonist-bonsai", "closed-laptop-bag"),
    "space-station": ("protagonist-bonsai", "earth"),
}

_ESTABLISHED_CONTINUITY = {
    "protagonist-bonsai": frozenset(
        ("midnight-library", "hacker-apartment", "rainy-loft", "space-station")
    ),
    "college-laptop": frozenset(("midnight-library", "coffee-cafe")),
}

_DISTINCT_OBJECT_PAIRS = {
    frozenset(("protagonist-bonsai", "coffee-cafe-house-bonsai")),
}


def check_camera(evidence: ArtworkEvidence, world: World) -> tuple[CritiqueFinding, ...]:
    if evidence.camera_behavior is CameraBehavior.STATIONARY:
        kind = FindingKind.ALIGNED
        observation = "The supplied evidence confirms a stationary camera."
    elif evidence.camera_behavior is CameraBehavior.MOVING:
        kind = FindingKind.CONFLICT
        observation = "The supplied evidence declares camera movement."
    else:
        kind = FindingKind.UNVERIFIED
        observation = "The supplied evidence does not establish camera behavior."

    return (
        CritiqueFinding(
            kind=kind,
            subject="Camera",
            observation=observation,
            canonical_expectation="The camera remains stationary.",
            principle="Law I — The Witness",
            world_key=world.stable_key,
        ),
    )


def check_required_objects(
    evidence: ArtworkEvidence,
    world: World,
) -> tuple[CritiqueFinding, ...]:
    findings = []
    present = set(evidence.present_object_ids)
    absent = set(evidence.absent_object_ids)
    for object_id in _REQUIRED_OBJECTS[world.stable_key]:
        if object_id in present:
            kind = FindingKind.ALIGNED
            observation = "The supplied evidence confirms this object is present."
        elif object_id in absent:
            kind = FindingKind.CONFLICT
            observation = "The supplied evidence confirms this object is absent."
        else:
            kind = FindingKind.UNVERIFIED
            observation = "The supplied evidence does not establish whether this object is present."
        findings.append(
            CritiqueFinding(
                kind=kind,
                subject="Required canonical object",
                observation=observation,
                canonical_expectation="This object remains present in this world.",
                principle="Bonsai and Beacon continuity",
                world_key=world.stable_key,
                object_id=object_id,
            )
        )
    return tuple(findings)


def check_immutable_elements(
    evidence: ArtworkEvidence,
    world: World,
) -> tuple[CritiqueFinding, ...]:
    findings = []
    canonical = set(world.immutable_elements)
    for item in evidence.immutable_elements:
        if item.canonical_text not in canonical:
            findings.append(
                CritiqueFinding(
                    kind=FindingKind.UNVERIFIED,
                    subject="Immutable element",
                    observation="The supplied statement does not exactly match a canonical immutable element.",
                    canonical_expectation="Unrecognized wording is not treated as canon evidence.",
                    principle="Humility over confidence",
                    world_key=world.stable_key,
                )
            )
            continue
        if item.state is EvidenceState.PRESENT:
            kind = FindingKind.ALIGNED
            observation = "The supplied evidence confirms the immutable element."
        elif item.state is EvidenceState.ABSENT:
            kind = FindingKind.CONFLICT
            observation = "The supplied evidence contradicts the immutable element."
        else:
            kind = FindingKind.UNVERIFIED
            observation = "The supplied evidence leaves the immutable element uncertain."
        findings.append(
            CritiqueFinding(
                kind=kind,
                subject="Immutable element",
                observation=observation,
                canonical_expectation=item.canonical_text,
                principle="World continuity",
                world_key=world.stable_key,
            )
        )
    return tuple(findings)


def check_readable_text(
    evidence: ArtworkEvidence,
    world: World,
) -> tuple[CritiqueFinding, ...]:
    findings = []
    prohibited = {
        ReadableTextUse.SLOGAN,
        ReadableTextUse.DECORATIVE,
        ReadableTextUse.EXPOSITION,
        ReadableTextUse.GIBBERISH,
    }
    for item in evidence.readable_text:
        if item.use in prohibited:
            kind = FindingKind.CONFLICT
            expectation = "Readable text is rare and must not explain or decorate the room."
        elif item.use is ReadableTextUse.NATURAL:
            kind = FindingKind.ALIGNED
            expectation = "Readable text exists only where a resident would naturally own it."
        else:
            kind = FindingKind.UNVERIFIED
            expectation = "The purpose of readable text must be established before judging it."
        findings.append(
            CritiqueFinding(
                kind=kind,
                subject="Readable text",
                observation=item.description,
                canonical_expectation=expectation,
                principle="Art Direction — Text",
                world_key=world.stable_key,
            )
        )
    return tuple(findings)


def check_continuity(
    evidence: ArtworkEvidence,
    world: World,
    objects_by_id: dict[str, StudioObject] | object,
) -> tuple[CritiqueFinding, ...]:
    findings = []
    for claim in evidence.continuity_claims:
        studio_object = objects_by_id[claim.object_id]  # type: ignore[index]
        established_worlds = _ESTABLISHED_CONTINUITY.get(claim.object_id)
        if established_worlds and {claim.prior_world_key, world.stable_key} <= established_worlds:
            kind = FindingKind.ALIGNED
            observation = "The claimed physical continuity is established by canon."
        else:
            distinct = any(
                claim.object_id in pair
                and any(other in evidence.present_object_ids for other in pair - {claim.object_id})
                for pair in _DISTINCT_OBJECT_PAIRS
            )
            kind = FindingKind.CONFLICT if distinct else FindingKind.UNVERIFIED
            observation = (
                "The claim conflicts with an explicitly distinct canonical object."
                if distinct
                else "Physical continuity is not established by current canon."
            )
        findings.append(
            CritiqueFinding(
                kind=kind,
                subject="Object continuity",
                observation=observation,
                canonical_expectation=studio_object.continuity_notes,
                principle="Object continuity",
                world_key=world.stable_key,
                object_id=claim.object_id,
            )
        )
    return tuple(findings)


def advisory_findings(
    evidence: ArtworkEvidence,
    world: World,
) -> tuple[CritiqueFinding, ...]:
    return tuple(
        CritiqueFinding(
            kind=FindingKind.ADVISORY,
            subject="Art-direction observation",
            observation=item.observation,
            canonical_expectation="This remains a matter for human artistic judgement.",
            principle=item.principle,
            world_key=world.stable_key,
        )
        for item in evidence.advisory_observations
    )

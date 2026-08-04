"""Calm human-readable presentation for Studio critiques."""

from __future__ import annotations

from pathlib import Path

from forge.critic_model import ArtworkEvidence, Critique, CritiqueFinding, FindingKind
from forge.evidence_loader import EvidenceDocument


def _finding_lines(finding: CritiqueFinding) -> list[str]:
    subject = finding.subject
    if finding.object_id is not None:
        subject = f"{subject} — {finding.object_id}"
    return [
        subject,
        finding.observation,
        f"Canon: {finding.canonical_expectation}",
        f"Principle: {finding.principle}",
    ]


def _section(
    lines: list[str],
    title: str,
    findings: tuple[CritiqueFinding, ...],
    empty_message: str,
) -> None:
    lines.extend(("", title, ""))
    if not findings:
        lines.append(empty_message)
        return
    for index, finding in enumerate(findings):
        if index:
            lines.append("")
        lines.extend(_finding_lines(finding))


def format_critique_report(
    document: EvidenceDocument,
    critique: Critique,
    source_path: str | Path,
) -> str:
    evidence: ArtworkEvidence = document.evidence
    artwork = evidence.artwork_id if evidence.artwork_id is not None else "Not supplied."
    lines = [
        critique.world.canonical_name,
        "",
        "Artwork Context",
        "",
        f"Artwork: {artwork}",
        f"World key: {evidence.world_key}",
        f"Created: {document.created}",
        f"Evidence source: {Path(source_path).resolve()}",
        "",
        "This critique considers only the evidence explicitly supplied.",
        "Anything omitted or marked unknown remains unverified.",
    ]

    _section(
        lines,
        "Canon Alignment",
        critique.findings_of_kind(FindingKind.ALIGNED),
        "No canon alignment was established by the supplied evidence.",
    )
    _section(
        lines,
        "Canon Conflicts",
        critique.findings_of_kind(FindingKind.CONFLICT),
        "No canon conflicts were established by the supplied evidence.",
    )
    _section(
        lines,
        "Unverified Requirements",
        critique.findings_of_kind(FindingKind.UNVERIFIED),
        "No unverified requirements were reported from the supplied evidence.",
    )
    _section(
        lines,
        "Advisory Observations",
        critique.findings_of_kind(FindingKind.ADVISORY),
        "No advisory observations were supplied.",
    )

    lines.extend(("", "World Keeper Review", ""))
    if critique.world_keeper_questions:
        for question in critique.world_keeper_questions:
            lines.append(f"- {question}")
        lines.append("")
    else:
        lines.extend(("No explicit World Keeper questions were raised.", ""))
    lines.extend(
        (
            "The Critic does not approve or reject artwork.",
            "Only the World Keeper may decide whether artwork becomes canon.",
        )
    )
    return "\n".join(lines) + "\n"

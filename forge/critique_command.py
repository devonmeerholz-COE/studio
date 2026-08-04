"""Command orchestration for human-authored Studio critique evidence."""

from __future__ import annotations

from forge.critic import StudioCritic
from forge.critique_report import format_critique_report
from forge.evidence_loader import EvidenceLoadError, load_evidence


USAGE = "Usage: python forge/main.py critique <evidence-file>"


def critique_file(path: str | None) -> int:
    if path is None:
        print("An evidence file is required.")
        print()
        print(USAGE)
        return 2

    try:
        document = load_evidence(path)
        critique = StudioCritic().evaluate(document.evidence)
    except (EvidenceLoadError, ValueError) as error:
        print(f"Could not critique artwork: {error}")
        return 2

    print(format_critique_report(document, critique, path), end="")
    return 0


def malformed_critique_usage() -> int:
    print("Critique accepts exactly one evidence file.")
    print()
    print(USAGE)
    return 2

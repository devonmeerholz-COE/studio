from dataclasses import FrozenInstanceError
import unittest

from forge.critic_model import (
    AdvisoryEvidence,
    ArtworkEvidence,
    CameraBehavior,
    ContinuityClaim,
    Critique,
    CritiqueFinding,
    EvidenceState,
    FindingKind,
    ImmutableElementEvidence,
    ReadableTextEvidence,
    ReadableTextUse,
)
from forge.worlds import HACKER_APARTMENT


class ArtworkEvidenceTests(unittest.TestCase):
    def test_evidence_is_immutable_and_preserves_unknowns(self):
        evidence = ArtworkEvidence("hacker-apartment")

        self.assertIs(evidence.camera_behavior, CameraBehavior.UNKNOWN)
        self.assertEqual(evidence.present_object_ids, ())
        with self.assertRaises(FrozenInstanceError):
            evidence.world_key = "rainy-loft"

    def test_rejects_an_object_as_both_present_and_absent(self):
        with self.assertRaises(ValueError):
            ArtworkEvidence(
                "hacker-apartment",
                present_object_ids=("protagonist-bonsai",),
                absent_object_ids=("protagonist-bonsai",),
            )

    def test_rejects_duplicate_and_malformed_ids(self):
        with self.assertRaises(ValueError):
            ArtworkEvidence("Hacker Apartment")
        with self.assertRaises(ValueError):
            ArtworkEvidence(
                "hacker-apartment",
                present_object_ids=("earth", "earth"),
            )

    def test_supporting_evidence_types_are_immutable(self):
        values = (
            ContinuityClaim("college-laptop", "midnight-library"),
            ImmutableElementEvidence("The camera remains stationary.", EvidenceState.PRESENT),
            ReadableTextEvidence("A notebook cover", ReadableTextUse.NATURAL),
            AdvisoryEvidence("Restraint", "The desk may feel visually crowded."),
        )
        for value in values:
            with self.subTest(value=type(value).__name__), self.assertRaises(FrozenInstanceError):
                setattr(value, next(iter(value.__dataclass_fields__)), "changed")


class CritiqueTests(unittest.TestCase):
    def test_finding_and_critique_are_immutable(self):
        finding = CritiqueFinding(
            FindingKind.ADVISORY,
            "Hierarchy",
            "Several objects may compete for attention.",
            "Visual hierarchy remains a human judgement.",
            "Art Direction — Visual Hierarchy",
            world_key="hacker-apartment",
        )
        critique = Critique(HACKER_APARTMENT, (finding,), ("Is this emphasis intentional?",))

        self.assertEqual(critique.findings_of_kind(FindingKind.ADVISORY), (finding,))
        with self.assertRaises(FrozenInstanceError):
            critique.findings = ()

    def test_finding_kind_is_closed_and_required_text_is_nonblank(self):
        with self.assertRaises(ValueError):
            CritiqueFinding("conflict", "Camera", "Moving", "Stationary", "Witness")
        with self.assertRaises(ValueError):
            CritiqueFinding(FindingKind.CONFLICT, " ", "Moving", "Stationary", "Witness")


if __name__ == "__main__":
    unittest.main()

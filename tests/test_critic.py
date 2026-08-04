import unittest

from forge.critic import StudioCritic
from forge.critic_model import (
    AdvisoryEvidence,
    ArtworkEvidence,
    CameraBehavior,
    ContinuityClaim,
    FindingKind,
)
from forge.objects import ALL_OBJECTS
from forge.worlds import ALL_WORLDS, HACKER_APARTMENT


class StudioCriticTests(unittest.TestCase):
    def setUp(self):
        self.critic = StudioCritic()

    def test_all_canonical_worlds_can_be_reviewed(self):
        for world in ALL_WORLDS:
            with self.subTest(world=world.stable_key):
                critique = self.critic.evaluate(ArtworkEvidence(world.stable_key))
                self.assertIs(critique.world, world)

    def test_all_canonical_objects_can_be_referenced(self):
        evidence = ArtworkEvidence(
            "hacker-apartment",
            present_object_ids=tuple(item.canonical_id for item in ALL_OBJECTS),
        )

        self.assertIs(self.critic.evaluate(evidence).world, HACKER_APARTMENT)

    def test_unknown_world_and_object_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown world key"):
            self.critic.evaluate(ArtworkEvidence("unknown-world"))
        with self.assertRaisesRegex(ValueError, "unknown object ID"):
            self.critic.evaluate(
                ArtworkEvidence("hacker-apartment", present_object_ids=("unknown-object",))
            )

    def test_evaluation_is_deterministic_and_uses_approved_rule_order(self):
        evidence = ArtworkEvidence(
            "hacker-apartment",
            camera_behavior=CameraBehavior.STATIONARY,
            present_object_ids=("protagonist-bonsai",),
            advisory_observations=(AdvisoryEvidence("Restraint", "The desk may feel crowded."),),
        )

        first = self.critic.evaluate(evidence)
        second = self.critic.evaluate(evidence)

        self.assertEqual(first, second)
        self.assertEqual(
            tuple(item.kind for item in first.findings),
            (FindingKind.ALIGNED, FindingKind.ALIGNED, FindingKind.ADVISORY),
        )

    def test_uncertain_evidence_never_becomes_a_conflict(self):
        critique = self.critic.evaluate(ArtworkEvidence("hacker-apartment"))

        self.assertFalse(critique.findings_of_kind(FindingKind.CONFLICT))
        self.assertTrue(critique.findings_of_kind(FindingKind.UNVERIFIED))

    def test_established_continuity_is_aligned(self):
        critique = self.critic.evaluate(
            ArtworkEvidence(
                "coffee-cafe",
                continuity_claims=(ContinuityClaim("college-laptop", "midnight-library"),),
            )
        )

        continuity = tuple(item for item in critique.findings if item.subject == "Object continuity")
        self.assertEqual(len(continuity), 1)
        self.assertIs(continuity[0].kind, FindingKind.ALIGNED)

    def test_critique_has_no_approval_rejection_or_score(self):
        critique = self.critic.evaluate(ArtworkEvidence("hacker-apartment"))

        for forbidden in ("approved", "rejected", "score"):
            self.assertFalse(hasattr(critique, forbidden))


if __name__ == "__main__":
    unittest.main()

import unittest

from forge.critic_model import (
    AdvisoryEvidence,
    ArtworkEvidence,
    CameraBehavior,
    ContinuityClaim,
    EvidenceState,
    FindingKind,
    ImmutableElementEvidence,
    ReadableTextEvidence,
    ReadableTextUse,
)
from forge.critic_rules import (
    advisory_findings,
    check_camera,
    check_continuity,
    check_immutable_elements,
    check_readable_text,
    check_required_objects,
)
from forge.objects import OBJECTS_BY_ID
from forge.worlds import COFFEE_CAFE, HACKER_APARTMENT


class ObjectiveRuleTests(unittest.TestCase):
    def test_camera_distinguishes_alignment_conflict_and_uncertainty(self):
        expected = (
            (CameraBehavior.STATIONARY, FindingKind.ALIGNED),
            (CameraBehavior.MOVING, FindingKind.CONFLICT),
            (CameraBehavior.UNKNOWN, FindingKind.UNVERIFIED),
        )
        for behavior, kind in expected:
            with self.subTest(behavior=behavior):
                findings = check_camera(ArtworkEvidence("hacker-apartment", camera_behavior=behavior), HACKER_APARTMENT)
                self.assertIs(findings[0].kind, kind)

    def test_missing_description_is_unverified_not_absent(self):
        findings = check_required_objects(ArtworkEvidence("coffee-cafe"), COFFEE_CAFE)

        self.assertTrue(findings)
        self.assertTrue(all(item.kind is FindingKind.UNVERIFIED for item in findings))

    def test_hacker_bonsai_satisfies_its_required_object(self):
        evidence = ArtworkEvidence(
            "hacker-apartment",
            present_object_ids=("protagonist-bonsai",),
        )

        self.assertIs(check_required_objects(evidence, HACKER_APARTMENT)[0].kind, FindingKind.ALIGNED)

    def test_coffee_cafe_requires_distinct_bonsai_and_beacon(self):
        evidence = ArtworkEvidence(
            "coffee-cafe",
            present_object_ids=("coffee-cafe-house-bonsai",),
            absent_object_ids=("coffee-pot",),
        )
        findings = check_required_objects(evidence, COFFEE_CAFE)

        self.assertEqual(tuple(item.object_id for item in findings), ("coffee-cafe-house-bonsai", "coffee-pot"))
        self.assertEqual(tuple(item.kind for item in findings), (FindingKind.ALIGNED, FindingKind.CONFLICT))

    def test_immutable_element_requires_exact_canonical_wording(self):
        canonical = HACKER_APARTMENT.immutable_elements[0]
        aligned = check_immutable_elements(
            ArtworkEvidence("hacker-apartment", immutable_elements=(ImmutableElementEvidence(canonical, EvidenceState.PRESENT),)),
            HACKER_APARTMENT,
        )
        uncertain = check_immutable_elements(
            ArtworkEvidence("hacker-apartment", immutable_elements=(ImmutableElementEvidence("The room seems right.", EvidenceState.PRESENT),)),
            HACKER_APARTMENT,
        )

        self.assertIs(aligned[0].kind, FindingKind.ALIGNED)
        self.assertIs(uncertain[0].kind, FindingKind.UNVERIFIED)

    def test_readable_text_rules_preserve_uncertainty(self):
        evidence = ArtworkEvidence(
            "hacker-apartment",
            readable_text=(
                ReadableTextEvidence("A motivational slogan", ReadableTextUse.SLOGAN),
                ReadableTextEvidence("Unclassified text", ReadableTextUse.UNKNOWN),
            ),
        )
        findings = check_readable_text(evidence, HACKER_APARTMENT)

        self.assertEqual(tuple(item.kind for item in findings), (FindingKind.CONFLICT, FindingKind.UNVERIFIED))

    def test_unestablished_physical_continuity_remains_unverified(self):
        evidence = ArtworkEvidence(
            "rainy-loft",
            continuity_claims=(ContinuityClaim("tape-deck", "midnight-library"),),
        )
        findings = check_continuity(evidence, HACKER_APARTMENT, OBJECTS_BY_ID)

        self.assertIs(findings[0].kind, FindingKind.UNVERIFIED)


class AdvisoryRuleTests(unittest.TestCase):
    def test_subjective_observations_are_always_advisory(self):
        evidence = ArtworkEvidence(
            "hacker-apartment",
            advisory_observations=(
                AdvisoryEvidence("Calm", "The lighting may feel demanding."),
                AdvisoryEvidence("Hope", "The emotional effect remains uncertain."),
            ),
        )

        findings = advisory_findings(evidence, HACKER_APARTMENT)
        self.assertTrue(all(item.kind is FindingKind.ADVISORY for item in findings))


if __name__ == "__main__":
    unittest.main()

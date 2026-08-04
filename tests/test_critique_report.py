from pathlib import Path
import unittest

from forge.critic import StudioCritic
from forge.critic_model import AdvisoryEvidence, ArtworkEvidence, CameraBehavior
from forge.critique_report import format_critique_report
from forge.evidence_loader import EvidenceDocument


class CritiqueReportTests(unittest.TestCase):
    def report(self):
        evidence = ArtworkEvidence(
            "hacker-apartment",
            artwork_id="rain-and-code-01",
            camera_behavior=CameraBehavior.STATIONARY,
            present_object_ids=("protagonist-bonsai",),
            advisory_observations=(
                AdvisoryEvidence("Visual Hierarchy", "The monitor may feel bright."),
            ),
        )
        document = EvidenceDocument(evidence, "2056-11-08")
        return format_critique_report(
            document,
            StudioCritic().evaluate(evidence),
            Path("evidence") / "rain-and-code.md",
        )

    def test_report_has_deterministic_approved_section_order(self):
        report = self.report()
        sections = (
            "Artwork Context",
            "Canon Alignment",
            "Canon Conflicts",
            "Unverified Requirements",
            "Advisory Observations",
            "World Keeper Review",
        )

        positions = tuple(report.index(section) for section in sections)
        self.assertEqual(positions, tuple(sorted(positions)))

    def test_report_is_humble_and_preserves_utf8(self):
        report = self.report()

        self.assertIn("Anything omitted or marked unknown remains unverified.", report)
        self.assertIn("No canon conflicts were established by the supplied evidence.", report)
        self.assertIn("The Critic does not approve or reject artwork.", report)
        self.assertIn("Only the World Keeper may decide whether artwork becomes canon.", report)
        self.assertIn("The Hacker Apartment", report)
        self.assertNotIn("100%", report)
        self.assertNotIn("Artwork approved", report)
        self.assertNotIn("Artwork rejected", report)
        self.assertNotIn("Score:", report)

    def test_report_preserves_finding_order_within_sections(self):
        report = self.report()

        self.assertLess(report.index("Camera\n"), report.index("Required canonical object — protagonist-bonsai"))


if __name__ == "__main__":
    unittest.main()

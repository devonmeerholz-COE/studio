from pathlib import Path
import tempfile
import unittest

from forge.critic_model import CameraBehavior, EvidenceState, ReadableTextUse
from forge.evidence_loader import EvidenceLoadError, load_evidence


def evidence_text(**changes):
    values = {
        "version": "1",
        "created": "`2056-11-08`",
        "world": "`hacker-apartment`",
        "artwork": "`hacker-apartment-study-01`",
        "camera": "`unknown`",
        "present": "- `protagonist-bonsai`",
        "absent": "- `college-laptop`",
        "continuity": "None supplied.",
        "immutable": "None supplied.",
        "readable": "None supplied.",
        "advisory": "None supplied.",
    }
    values.update(changes)
    return f"""# SUPER CHILLED STUDIO

# ARTWORK EVIDENCE

Evidence Format Version: {values['version']}
Created: {values['created']}

## Artwork

World key: {values['world']}
Artwork ID: {values['artwork']}

## Camera Behavior

{values['camera']}

## Confirmed Present Objects

{values['present']}

## Confirmed Absent Objects

{values['absent']}

## Continuity Claims

{values['continuity']}

## Immutable Elements

{values['immutable']}

## Readable Text

{values['readable']}

## Advisory Observations

{values['advisory']}
"""


class EvidenceLoaderTests(unittest.TestCase):
    def load(self, content):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "artwork-evidence.md"
        path.write_text(content, encoding="utf-8")
        return load_evidence(path)

    def test_valid_complete_document_maps_every_supported_field(self):
        immutable = """### Evidence

State: `present`

Canonical text:

```text
The chair remains empty because the viewer is the hacker. The camera remains stationary. The Bonsai remains present. The desk remains the visual center.
```"""
        readable = """### Evidence

Use: `natural`

Description:

```text
A handwritten café note.
```"""
        advisory = """### Observation

Principle:

```text
Visual Hierarchy
```

Observation:

```text
The monitor may compete for attention.
```"""
        continuity = """### Claim

Object ID: `college-laptop`
Prior world key: `midnight-library`"""

        document = self.load(
            evidence_text(
                camera="`stationary`",
                continuity=continuity,
                immutable=immutable,
                readable=readable,
                advisory=advisory,
            )
        )
        evidence = document.evidence

        self.assertEqual(document.created, "2056-11-08")
        self.assertIs(evidence.camera_behavior, CameraBehavior.STATIONARY)
        self.assertEqual(evidence.continuity_claims[0].object_id, "college-laptop")
        self.assertIs(evidence.immutable_elements[0].state, EvidenceState.PRESENT)
        self.assertIs(evidence.readable_text[0].use, ReadableTextUse.NATURAL)
        self.assertEqual(evidence.advisory_observations[0].principle, "Visual Hierarchy")
        self.assertIn("café", evidence.readable_text[0].description)

    def test_omitted_knowledge_remains_unknown(self):
        document = self.load(
            evidence_text(
                artwork="Not supplied.",
                present="None supplied.",
                absent="None supplied.",
            )
        )

        self.assertIsNone(document.evidence.artwork_id)
        self.assertIs(document.evidence.camera_behavior, CameraBehavior.UNKNOWN)
        self.assertEqual(document.evidence.present_object_ids, ())
        self.assertEqual(document.evidence.absent_object_ids, ())

    def test_missing_world_key_and_malformed_structure_are_rejected(self):
        with self.assertRaises(EvidenceLoadError):
            self.load(evidence_text(world=""))
        with self.assertRaises(EvidenceLoadError):
            self.load(evidence_text().replace("## Readable Text", "## Notes"))

    def test_wrong_types_and_unknown_enums_are_rejected(self):
        with self.assertRaisesRegex(EvidenceLoadError, "backtick-wrapped"):
            self.load(evidence_text(camera="stationary"))
        with self.assertRaisesRegex(EvidenceLoadError, "must be one of"):
            self.load(evidence_text(camera="`fixed`"))

    def test_contradictory_present_and_absent_objects_are_rejected(self):
        with self.assertRaisesRegex(EvidenceLoadError, "both present and absent"):
            self.load(evidence_text(absent="- `protagonist-bonsai`"))

    def test_created_date_is_required_but_informational(self):
        first = self.load(evidence_text(created="`2056-11-08`"))
        second = self.load(evidence_text(created="`2096-01-01`"))

        self.assertEqual(first.evidence, second.evidence)
        with self.assertRaisesRegex(EvidenceLoadError, "valid YYYY-MM-DD"):
            self.load(evidence_text(created="`2056-99-99`"))

    def test_extra_content_is_rejected(self):
        with self.assertRaisesRegex(EvidenceLoadError, "unexpected content"):
            self.load(evidence_text() + "Unsupported note.\n")


if __name__ == "__main__":
    unittest.main()

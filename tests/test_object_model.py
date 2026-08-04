from dataclasses import FrozenInstanceError
import unittest

from forge.object_model import (
    ObjectCategory,
    RecognitionLevel,
    StudioObject,
    WorldMoment,
)


def make_object(**changes):
    first_appearance = WorldMoment("midnight-library", "first appearance")
    values = {
        "canonical_name": "A Meaningful Object",
        "canonical_id": "meaningful-object",
        "category": ObjectCategory.IDENTITY,
        "recognition_level": RecognitionLevel.SUBTLE,
        "first_appearance": first_appearance,
        "purpose": ("It carries meaning.",),
        "studio_rules": "It remains purposeful.",
        "evolution": (first_appearance,),
        "continuity_notes": "Its continuity is established.",
        "appearances": (first_appearance,),
    }
    values.update(changes)
    return StudioObject(**values)


class ObjectVocabularyTests(unittest.TestCase):
    def test_categories_are_the_exact_canonical_vocabulary(self):
        self.assertEqual(
            tuple(category.value for category in ObjectCategory),
            ("Canon", "Beacon", "Identity", "Tool", "Memory"),
        )

    def test_recognition_levels_are_the_exact_canonical_vocabulary(self):
        self.assertEqual(
            tuple(level.value for level in RecognitionLevel),
            ("Immediate", "Familiar", "Subtle", "Hidden"),
        )


class WorldMomentTests(unittest.TestCase):
    def test_valid_world_moment_preserves_canon(self):
        moment = WorldMoment("midnight-library", "earliest life stage")

        self.assertEqual(moment.world_key, "midnight-library")
        self.assertEqual(moment.description, "earliest life stage")

    def test_world_moment_is_immutable(self):
        moment = WorldMoment("midnight-library", "earliest life stage")

        with self.assertRaises(FrozenInstanceError):
            moment.description = "changed"

    def test_world_moment_requires_nonblank_description(self):
        with self.assertRaises(ValueError):
            WorldMoment("midnight-library", " ")

    def test_world_moment_requires_kebab_case_world_key(self):
        for value in ("Midnight-Library", "midnight_library", "midnight library"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                WorldMoment(value, "an appearance")


class StudioObjectTests(unittest.TestCase):
    def test_valid_object_preserves_every_field(self):
        studio_object = make_object(
            purpose=("First paragraph.", "Second paragraph."),
        )

        self.assertEqual(studio_object.canonical_name, "A Meaningful Object")
        self.assertEqual(studio_object.canonical_id, "meaningful-object")
        self.assertIs(studio_object.category, ObjectCategory.IDENTITY)
        self.assertIs(studio_object.recognition_level, RecognitionLevel.SUBTLE)
        self.assertIsInstance(studio_object.first_appearance, WorldMoment)
        self.assertEqual(
            studio_object.purpose,
            ("First paragraph.", "Second paragraph."),
        )
        self.assertEqual(studio_object.studio_rules, "It remains purposeful.")
        self.assertEqual(studio_object.continuity_notes, "Its continuity is established.")

    def test_studio_object_and_collections_are_immutable(self):
        studio_object = make_object()

        with self.assertRaises(FrozenInstanceError):
            studio_object.canonical_name = "Changed"
        with self.assertRaises(TypeError):
            studio_object.purpose[0] = "Changed"
        with self.assertRaises(TypeError):
            studio_object.evolution[0] = studio_object.first_appearance

    def test_required_text_rejects_blank_values(self):
        for field in ("canonical_name", "canonical_id", "studio_rules", "continuity_notes"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                make_object(**{field: " "})

    def test_required_collections_reject_empty_values(self):
        for field in ("purpose", "evolution", "appearances"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                make_object(**{field: ()})

    def test_purpose_rejects_blank_paragraphs(self):
        with self.assertRaises(ValueError):
            make_object(purpose=("A purpose.", " "))

    def test_timeline_entries_must_be_world_moments(self):
        for field in ("evolution", "appearances"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                make_object(**{field: ("not a moment",)})

    def test_first_appearance_must_be_a_world_moment(self):
        with self.assertRaises(ValueError):
            make_object(first_appearance="midnight-library")

    def test_category_must_use_canonical_enum(self):
        with self.assertRaises(ValueError):
            make_object(category="Identity")

    def test_recognition_level_must_use_canonical_enum(self):
        with self.assertRaises(ValueError):
            make_object(recognition_level="Subtle")

    def test_canonical_id_accepts_lowercase_kebab_case(self):
        for value in ("earth", "coffee-pot", "world-object-01"):
            with self.subTest(value=value):
                self.assertEqual(make_object(canonical_id=value).canonical_id, value)

    def test_canonical_id_rejects_other_formats(self):
        invalid = (
            "Coffee-Pot",
            "coffee_pot",
            "coffee pot",
            "-coffee-pot",
            "coffee-pot-",
            "coffee--pot",
        )
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                make_object(canonical_id=value)


if __name__ == "__main__":
    unittest.main()

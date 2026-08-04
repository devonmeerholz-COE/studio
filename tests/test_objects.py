from types import MappingProxyType
import unittest

from forge.object_model import ObjectCategory, RecognitionLevel, WorldMoment
from forge.objects import (
    ALL_OBJECTS,
    CLOSED_LAPTOP_BAG,
    COFFEE_CAFE_HOUSE_BONSAI,
    COFFEE_POT,
    COLLEGE_LAPTOP,
    DINER_MUG,
    EARTH,
    EVOLVING_BACKPACK,
    LIBRARY_DESK_LAMP,
    MECH_FIGURE_AND_MEMENTOS,
    OBJECTS_BY_ID,
    PROTAGONIST_BONSAI,
    RED_PANDA_PLUSH,
    TAPE_DECK,
)
from forge.worlds import WORLDS_BY_KEY


CANONICAL_OBJECTS = (
    PROTAGONIST_BONSAI,
    COFFEE_CAFE_HOUSE_BONSAI,
    LIBRARY_DESK_LAMP,
    COFFEE_POT,
    CLOSED_LAPTOP_BAG,
    EARTH,
    RED_PANDA_PLUSH,
    COLLEGE_LAPTOP,
    TAPE_DECK,
    EVOLVING_BACKPACK,
    MECH_FIGURE_AND_MEMENTOS,
    DINER_MUG,
)

EXPECTED_METADATA = (
    ("The Protagonist’s Bonsai", "protagonist-bonsai", ObjectCategory.CANON, RecognitionLevel.FAMILIAR, "midnight-library", "earliest life stage"),
    ("Coffee Café House Bonsai", "coffee-cafe-house-bonsai", ObjectCategory.CANON, RecognitionLevel.SUBTLE, "coffee-cafe", "house Bonsai belonging to the café"),
    ("Library Desk Lamp", "library-desk-lamp", ObjectCategory.BEACON, RecognitionLevel.IMMEDIATE, "midnight-library", "the only lamp still burning"),
    ("Coffee Pot", "coffee-pot", ObjectCategory.BEACON, RecognitionLevel.IMMEDIATE, "coffee-cafe", "left on the table and quietly refilled"),
    ("Closed Laptop Bag", "closed-laptop-bag", ObjectCategory.BEACON, RecognitionLevel.SUBTLE, "rainy-loft", "closed and resting by the door"),
    ("Earth", "earth", ObjectCategory.BEACON, RecognitionLevel.IMMEDIATE, "space-station", "always visible through the largest viewport"),
    ("Red Panda Plush", "red-panda-plush", ObjectCategory.MEMORY, RecognitionLevel.FAMILIAR, "midnight-library", "loved study companion"),
    ("College Laptop", "college-laptop", ObjectCategory.TOOL, RecognitionLevel.FAMILIAR, "midnight-library", "worn student laptop"),
    ("Tape Deck", "tape-deck", ObjectCategory.MEMORY, RecognitionLevel.SUBTLE, "midnight-library", "connected to the learner’s headset"),
    ("Evolving Backpack", "evolving-backpack", ObjectCategory.IDENTITY, RecognitionLevel.FAMILIAR, "midnight-library", "evolving through stickers, study marks, and repeated visits"),
    ("Mech Figure and Mementos", "mech-mementos", ObjectCategory.IDENTITY, RecognitionLevel.HIDDEN, "hacker-apartment", "mech figure"),
    ("Diner Mug", "diner-mug", ObjectCategory.MEMORY, RecognitionLevel.HIDDEN, "space-station", "quiet keepsake from the diner"),
)


class CanonicalObjectsTests(unittest.TestCase):
    def test_exactly_twelve_objects_in_document_order(self):
        self.assertIsInstance(ALL_OBJECTS, tuple)
        self.assertEqual(ALL_OBJECTS, CANONICAL_OBJECTS)
        self.assertEqual(len(ALL_OBJECTS), 12)

    def test_canonical_metadata_and_first_appearances_match(self):
        actual = tuple(
            (
                studio_object.canonical_name,
                studio_object.canonical_id,
                studio_object.category,
                studio_object.recognition_level,
                studio_object.first_appearance.world_key,
                studio_object.first_appearance.description,
            )
            for studio_object in ALL_OBJECTS
        )

        self.assertEqual(actual, EXPECTED_METADATA)

    def test_first_appearance_reuses_world_moment_and_matches_appearances(self):
        for studio_object in ALL_OBJECTS:
            with self.subTest(canonical_id=studio_object.canonical_id):
                self.assertIsInstance(studio_object.first_appearance, WorldMoment)
                self.assertEqual(studio_object.first_appearance, studio_object.appearances[0])

    def test_canonical_ids_are_unique(self):
        canonical_ids = tuple(item.canonical_id for item in ALL_OBJECTS)

        self.assertEqual(len(set(canonical_ids)), len(canonical_ids))

    def test_objects_by_id_is_read_only_and_complete(self):
        self.assertIsInstance(OBJECTS_BY_ID, MappingProxyType)
        self.assertEqual(set(OBJECTS_BY_ID), {item.canonical_id for item in ALL_OBJECTS})

        with self.assertRaises(TypeError):
            OBJECTS_BY_ID["another-object"] = PROTAGONIST_BONSAI

    def test_mapping_values_are_the_canonical_instances(self):
        for studio_object in ALL_OBJECTS:
            with self.subTest(canonical_id=studio_object.canonical_id):
                self.assertIs(OBJECTS_BY_ID[studio_object.canonical_id], studio_object)

    def test_every_referenced_world_is_canonical(self):
        for studio_object in ALL_OBJECTS:
            moments = (
                studio_object.first_appearance,
                *studio_object.evolution,
                *studio_object.appearances,
            )
            for moment in moments:
                with self.subTest(
                    canonical_id=studio_object.canonical_id,
                    world_key=moment.world_key,
                ):
                    self.assertIn(moment.world_key, WORLDS_BY_KEY)

    def test_protagonist_bonsai_preserves_two_purpose_paragraphs(self):
        self.assertEqual(
            PROTAGONIST_BONSAI.purpose,
            (
                "Represents quiet growth across an entire lifetime.",
                "It reminds the viewer that meaningful change is measured in years rather than moments.",
            ),
        )

    def test_uncertain_physical_continuity_remains_uncertain(self):
        for studio_object in (
            RED_PANDA_PLUSH,
            TAPE_DECK,
            MECH_FIGURE_AND_MEMENTOS,
        ):
            with self.subTest(canonical_id=studio_object.canonical_id):
                self.assertIn(
                    "Physical continuity is not yet established.",
                    studio_object.continuity_notes,
                )

    def test_college_laptop_preserves_explicit_continuity(self):
        self.assertEqual(
            COLLEGE_LAPTOP.continuity_notes,
            "The Coffee Café laptop is the same laptop carried forward from college. No later appearance is currently defined.",
        )

    def test_diner_mug_preserves_qualified_continuity(self):
        self.assertEqual(
            DINER_MUG.continuity_notes,
            "Its Space Station appearance references the Coffee Café, but an earlier on-screen appearance of this physical mug is not yet established.",
        )


if __name__ == "__main__":
    unittest.main()

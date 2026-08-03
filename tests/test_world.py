from dataclasses import FrozenInstanceError
import unittest

from forge.world import Beacon, BonsaiRelationship, Era, Soundscape, World


def make_world(**changes):
    values = {
        "stable_key": "quiet-place",
        "canonical_name": "The Quiet Place",
        "catalog_number": 1,
        "chronological_stage": 1,
        "era": Era(("A place", "2056", "A life stage.")),
        "purpose": "A place with purpose.",
        "resident_identity": "You are the resident.",
        "emotional_core": ("Hope",),
        "first_impression": "The room is waiting for you.",
        "leaving_this_world": ("Hopeful.",),
        "setting": "A meaningful place.",
        "beacon": Beacon("A lamp.", "It means home.", "It may age."),
        "bonsai_relationship": BonsaiRelationship(
            "The protagonist's Bonsai.",
            "Young.",
            "It is distinct from the Beacon.",
        ),
        "soundscape": Soundscape("Quiet music.", "Gentle rain.", "Restful."),
        "personal_artifacts": ("A worn notebook.",),
        "passage_of_time": "The notebook fills.",
        "immutable_elements": ("The lamp remains.",),
    }
    values.update(changes)
    return World(**values)


class SupportingValueObjectTests(unittest.TestCase):
    def test_valid_value_objects(self):
        self.assertEqual(Era(("Neo-Tokyo", "2056")).lines, ("Neo-Tokyo", "2056"))
        self.assertEqual(
            Beacon("A lamp", "A welcome", "Natural aging").identity,
            "A lamp",
        )
        self.assertEqual(
            BonsaiRelationship("A Bonsai", "Young", "Also the Beacon").life_stage,
            "Young",
        )
        self.assertEqual(
            Soundscape("Piano", "Rain", "Sheltering").silence,
            "Sheltering",
        )

    def test_value_objects_are_immutable(self):
        era = Era(("Neo-Tokyo", "2056"))

        with self.assertRaises(FrozenInstanceError):
            era.lines = ("2096",)

        with self.assertRaises(TypeError):
            era.lines[0] = "2096"

    def test_era_requires_lines(self):
        with self.assertRaises(ValueError):
            Era(())

    def test_era_rejects_blank_lines(self):
        with self.assertRaises(ValueError):
            Era(("Neo-Tokyo", " "))

    def test_beacon_rejects_blank_text(self):
        valid = ("A lamp", "A welcome", "Natural aging")
        for index in range(len(valid)):
            values = list(valid)
            values[index] = " "
            with self.subTest(index=index), self.assertRaises(ValueError):
                Beacon(*values)

    def test_bonsai_relationship_rejects_blank_text(self):
        valid = ("A Bonsai", "Young", "Also the Beacon")
        for index in range(len(valid)):
            values = list(valid)
            values[index] = " "
            with self.subTest(index=index), self.assertRaises(ValueError):
                BonsaiRelationship(*values)

    def test_soundscape_rejects_blank_text(self):
        valid = ("Piano", "Rain", "Sheltering")
        for index in range(len(valid)):
            values = list(valid)
            values[index] = " "
            with self.subTest(index=index), self.assertRaises(ValueError):
                Soundscape(*values)


class WorldTests(unittest.TestCase):
    def test_valid_world_preserves_full_canon(self):
        world = make_world(motto="Keep going.", naming_note="The place is unnamed.")

        self.assertEqual(world.stable_key, "quiet-place")
        self.assertEqual(world.emotional_core, ("Hope",))
        self.assertEqual(world.leaving_this_world, ("Hopeful.",))
        self.assertEqual(world.personal_artifacts, ("A worn notebook.",))
        self.assertEqual(world.immutable_elements, ("The lamp remains.",))
        self.assertEqual(world.motto, "Keep going.")
        self.assertEqual(world.naming_note, "The place is unnamed.")

    def test_world_is_immutable(self):
        world = make_world()

        with self.assertRaises(FrozenInstanceError):
            world.canonical_name = "Another Place"

        with self.assertRaises(TypeError):
            world.emotional_core[0] = "Calm"

    def test_optional_text_defaults_to_none(self):
        world = make_world()

        self.assertIsNone(world.motto)
        self.assertIsNone(world.naming_note)

    def test_optional_text_rejects_blank_values(self):
        for field in ("motto", "naming_note"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                make_world(**{field: " "})

    def test_required_world_text_rejects_blank_values(self):
        fields = (
            "stable_key",
            "canonical_name",
            "purpose",
            "resident_identity",
            "first_impression",
            "setting",
            "passage_of_time",
        )
        for field in fields:
            with self.subTest(field=field), self.assertRaises(ValueError):
                make_world(**{field: " "})

    def test_required_collections_reject_empty_values(self):
        fields = (
            "emotional_core",
            "leaving_this_world",
            "personal_artifacts",
            "immutable_elements",
        )
        for field in fields:
            with self.subTest(field=field), self.assertRaises(ValueError):
                make_world(**{field: ()})

    def test_required_collections_reject_blank_entries(self):
        fields = (
            "emotional_core",
            "leaving_this_world",
            "personal_artifacts",
            "immutable_elements",
        )
        for field in fields:
            with self.subTest(field=field), self.assertRaises(ValueError):
                make_world(**{field: (" ",)})

    def test_catalog_number_must_be_positive(self):
        for value in (0, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                make_world(catalog_number=value)

    def test_chronological_stage_must_be_positive(self):
        for value in (0, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                make_world(chronological_stage=value)

    def test_stable_key_accepts_lowercase_kebab_case(self):
        for value in ("world", "quiet-place", "world-01"):
            with self.subTest(value=value):
                self.assertEqual(make_world(stable_key=value).stable_key, value)

    def test_stable_key_rejects_other_formats(self):
        invalid = (
            "Quiet-place",
            "quiet place",
            "quiet_place",
            "-quiet-place",
            "quiet-place-",
            "quiet--place",
        )
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                make_world(stable_key=value)

    def test_bonsai_may_also_be_the_beacon(self):
        world = make_world(
            beacon=Beacon("The Bonsai", "It means home.", "It grows naturally."),
            bonsai_relationship=BonsaiRelationship(
                "The Bonsai",
                "Young",
                "It is also the Beacon.",
            ),
        )

        self.assertEqual(world.beacon.identity, world.bonsai_relationship.identity)

    def test_bonsai_may_be_distinct_from_the_beacon(self):
        world = make_world(
            beacon=Beacon("A lamp", "It means home.", "It may age."),
            bonsai_relationship=BonsaiRelationship(
                "The Bonsai",
                "Young",
                "It is distinct from the Beacon.",
            ),
        )

        self.assertNotEqual(world.beacon.identity, world.bonsai_relationship.identity)

    def test_unspecified_bonsai_life_stage_is_canonical_text(self):
        world = make_world(
            bonsai_relationship=BonsaiRelationship(
                "The café's house Bonsai.",
                "Not specified.",
                "It is distinct from the Beacon.",
            )
        )

        self.assertEqual(world.bonsai_relationship.life_stage, "Not specified.")


if __name__ == "__main__":
    unittest.main()

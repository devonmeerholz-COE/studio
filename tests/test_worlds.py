from types import MappingProxyType
import unittest

from forge.worlds import (
    ALL_WORLDS,
    COFFEE_CAFE,
    HACKER_APARTMENT,
    MIDNIGHT_LIBRARY,
    RAINY_LOFT,
    SPACE_STATION,
    WORLDS_BY_KEY,
)


class CanonicalWorldsTests(unittest.TestCase):
    def test_exactly_five_canonical_worlds(self):
        self.assertEqual(len(ALL_WORLDS), 5)

    def test_all_worlds_is_an_immutable_tuple_in_catalog_order(self):
        self.assertIsInstance(ALL_WORLDS, tuple)
        self.assertEqual(
            ALL_WORLDS,
            (
                HACKER_APARTMENT,
                MIDNIGHT_LIBRARY,
                COFFEE_CAFE,
                RAINY_LOFT,
                SPACE_STATION,
            ),
        )

    def test_stable_keys_are_unique(self):
        keys = tuple(world.stable_key for world in ALL_WORLDS)

        self.assertEqual(len(set(keys)), len(keys))

    def test_catalog_numbers_are_unique_and_complete(self):
        numbers = tuple(world.catalog_number for world in ALL_WORLDS)

        self.assertEqual(len(set(numbers)), len(numbers))
        self.assertEqual(numbers, (1, 2, 3, 4, 5))

    def test_chronological_stages_are_unique_and_complete(self):
        stages = tuple(world.chronological_stage for world in ALL_WORLDS)

        self.assertEqual(len(set(stages)), len(stages))
        self.assertEqual(set(stages), {1, 2, 3, 4, 5})

    def test_worlds_by_key_is_read_only_and_contains_every_world(self):
        self.assertIsInstance(WORLDS_BY_KEY, MappingProxyType)
        self.assertEqual(set(WORLDS_BY_KEY), {world.stable_key for world in ALL_WORLDS})

        with self.assertRaises(TypeError):
            WORLDS_BY_KEY["another-world"] = HACKER_APARTMENT

    def test_worlds_by_key_values_are_the_canonical_instances(self):
        for world in ALL_WORLDS:
            with self.subTest(stable_key=world.stable_key):
                self.assertIs(WORLDS_BY_KEY[world.stable_key], world)


if __name__ == "__main__":
    unittest.main()

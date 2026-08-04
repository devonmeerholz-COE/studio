import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest

from forge import main as forge_main
from forge.inspection import inspect_world
from forge.worlds import ALL_WORLDS, COFFEE_CAFE, HACKER_APARTMENT, SPACE_STATION


SECTION_TITLES = (
    "First Impression",
    "Era",
    "Purpose",
    "Resident Identity",
    "Emotional Core",
    "Leaving This World",
    "Setting",
    "Beacon",
    "Bonsai Relationship",
    "Soundscape",
    "Personal Artifacts",
    "Passage of Time",
    "Immutable Elements",
)


def expected_output(world):
    lines = [
        world.canonical_name,
        "",
        f"Stable key: {world.stable_key}",
        f"Catalog number: {world.catalog_number}",
        f"Chronological stage: {world.chronological_stage}",
        "",
        "First Impression",
        "",
        world.first_impression,
        "",
        "Era",
        "",
        *(f"- {line}" for line in world.era.lines),
        "",
        "Purpose",
        "",
        world.purpose,
        "",
        "Resident Identity",
        "",
        world.resident_identity,
        "",
        "Emotional Core",
        "",
        *world.emotional_core,
        "",
        "Leaving This World",
        "",
        *(f"- {state}" for state in world.leaving_this_world),
        "",
        "Setting",
        "",
        world.setting,
        "",
        "Beacon",
        "",
        f"Identity: {world.beacon.identity}",
        f"Emotional purpose: {world.beacon.emotional_purpose}",
        f"Natural aging: {world.beacon.natural_aging}",
        "",
        "Bonsai Relationship",
        "",
        f"Identity: {world.bonsai_relationship.identity}",
        f"Life stage: {world.bonsai_relationship.life_stage}",
        f"Beacon relationship: {world.bonsai_relationship.beacon_relationship}",
        "",
        "Soundscape",
        "",
        f"Music: {world.soundscape.music}",
        f"Ambient World: {world.soundscape.ambient_world}",
        f"Silence: {world.soundscape.silence}",
        "",
        "Personal Artifacts",
        "",
        *world.personal_artifacts,
        "",
        "Passage of Time",
        "",
        world.passage_of_time,
        "",
        "Immutable Elements",
        "",
        *world.immutable_elements,
    ]
    if world.motto is not None:
        lines.extend(("", "Motto", "", world.motto))
    if world.naming_note is not None:
        lines.extend(("", "Naming", "", world.naming_note))
    return "\n".join(lines) + "\n"


class InspectWorldTests(unittest.TestCase):
    def capture_inspection(self, world_key):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = inspect_world(world_key)
        return exit_code, output.getvalue()

    def test_every_canonical_world_has_an_exact_complete_reference_view(self):
        for world in ALL_WORLDS:
            with self.subTest(stable_key=world.stable_key):
                exit_code, output = self.capture_inspection(world.stable_key)

                self.assertEqual(exit_code, 0)
                self.assertEqual(output, expected_output(world))

    def test_required_sections_appear_in_approved_order(self):
        _, output = self.capture_inspection(HACKER_APARTMENT.stable_key)

        positions = [output.index(f"\n{title}\n") for title in SECTION_TITLES]
        self.assertEqual(positions, sorted(positions))

    def test_canonical_tuple_boundaries_are_preserved(self):
        _, output = self.capture_inspection(HACKER_APARTMENT.stable_key)

        self.assertIn("\n- Neo-Tokyo\n- 2056\n", output)
        self.assertIn("\n- Inspired to build.\n", output)
        self.assertIn(
            "\nFreedom, ownership, determination, possibility, hope.\n",
            output,
        )
        self.assertNotIn("\n- Freedom\n", output)
        self.assertIn(f"\n{HACKER_APARTMENT.personal_artifacts[0]}\n", output)
        self.assertIn(f"\n{HACKER_APARTMENT.immutable_elements[0]}\n", output)

    def test_space_station_setting_preserves_paragraph_break(self):
        _, output = self.capture_inspection(SPACE_STATION.stable_key)

        self.assertIn(SPACE_STATION.setting, output)
        self.assertIn("faces Earth.\n\nThe station feels", output)

    def test_motto_is_printed_only_when_defined(self):
        _, with_motto = self.capture_inspection(COFFEE_CAFE.stable_key)
        _, without_motto = self.capture_inspection(HACKER_APARTMENT.stable_key)

        self.assertIn("\nMotto\n\n", with_motto)
        self.assertIn(COFFEE_CAFE.motto, with_motto)
        self.assertNotIn("\nMotto\n\n", without_motto)

    def test_naming_is_printed_only_when_defined(self):
        _, with_naming = self.capture_inspection(COFFEE_CAFE.stable_key)
        _, without_naming = self.capture_inspection(HACKER_APARTMENT.stable_key)

        self.assertIn("\nNaming\n\n", with_naming)
        self.assertIn(COFFEE_CAFE.naming_note, with_naming)
        self.assertNotIn("\nNaming\n\n", without_naming)

    def test_missing_key_lists_valid_keys_in_catalog_order(self):
        exit_code, output = self.capture_inspection(None)

        self.assertEqual(exit_code, 2)
        self.assertIn("A world key is required.", output)
        self.assert_keys_are_listed_in_catalog_order(output)

    def test_unknown_key_is_exact_and_case_sensitive(self):
        exit_code, output = self.capture_inspection("Hacker-Apartment")

        self.assertEqual(exit_code, 2)
        self.assertIn("Unknown world key: Hacker-Apartment", output)
        self.assert_keys_are_listed_in_catalog_order(output)

    def assert_keys_are_listed_in_catalog_order(self, output):
        positions = [output.index(f"- {world.stable_key}") for world in ALL_WORLDS]
        self.assertEqual(positions, sorted(positions))


class InspectCommandTests(unittest.TestCase):
    def capture_main(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = forge_main.main(args)
        return exit_code, output.getvalue()

    def test_main_routes_inspect_command(self):
        exit_code, output = self.capture_main(["inspect", "hacker-apartment"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output, expected_output(HACKER_APARTMENT))

    def test_main_routes_missing_inspect_key(self):
        exit_code, output = self.capture_main(["inspect"])

        self.assertEqual(exit_code, 2)
        self.assertIn("A world key is required.", output)

    def test_main_routes_unknown_inspect_key(self):
        exit_code, output = self.capture_main(["inspect", "unknown-place"])

        self.assertEqual(exit_code, 2)
        self.assertIn("Unknown world key: unknown-place", output)

    def test_main_rejects_malformed_inspect_usage(self):
        exit_code, output = self.capture_main(
            ["inspect", "hacker-apartment", "extra"]
        )

        self.assertEqual(exit_code, 2)
        self.assertIn("Inspect accepts exactly one world key.", output)
        positions = [output.index(f"- {world.stable_key}") for world in ALL_WORLDS]
        self.assertEqual(positions, sorted(positions))

    def test_direct_script_execution_uses_utf8(self):
        studio_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "forge/main.py", "inspect", "coffee-cafe"],
            cwd=studio_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, expected_output(COFFEE_CAFE))
        self.assertIn("The Coffee Café", result.stdout)
        self.assertIn("The visitor’s booth remains.", result.stdout)


if __name__ == "__main__":
    unittest.main()

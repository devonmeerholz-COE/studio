import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest

from forge import main as forge_main
from forge.visit import visit
from forge.worlds import ALL_WORLDS


class VisitTests(unittest.TestCase):
    def capture_visit(self, world_key):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = visit(world_key)
        return exit_code, output.getvalue()

    def test_every_canonical_world_can_be_visited(self):
        for world in ALL_WORLDS:
            with self.subTest(stable_key=world.stable_key):
                exit_code, output = self.capture_visit(world.stable_key)

                self.assertEqual(exit_code, 0)
                self.assertIn(world.canonical_name, output)
                self.assertIn(world.first_impression, output)
                self.assertIn(world.resident_identity, output)
                self.assertIn(world.purpose, output)
                for state in world.leaving_this_world:
                    self.assertIn(f"- {state}", output)

    def test_missing_world_key_lists_valid_keys_in_catalog_order(self):
        exit_code, output = self.capture_visit(None)

        self.assertEqual(exit_code, 2)
        self.assertIn("A world key is required.", output)
        self.assert_keys_are_listed_in_catalog_order(output)

    def test_unknown_world_key_lists_valid_keys_in_catalog_order(self):
        exit_code, output = self.capture_visit("unknown-place")

        self.assertEqual(exit_code, 2)
        self.assertIn("Unknown world key: unknown-place", output)
        self.assert_keys_are_listed_in_catalog_order(output)

    def assert_keys_are_listed_in_catalog_order(self, output):
        positions = [output.index(f"- {world.stable_key}") for world in ALL_WORLDS]
        self.assertEqual(positions, sorted(positions))


class VisitCommandTests(unittest.TestCase):
    def capture_main(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = forge_main.main(args)
        return exit_code, output.getvalue()

    def test_main_routes_visit_command(self):
        exit_code, output = self.capture_main(["visit", "hacker-apartment"])

        self.assertEqual(exit_code, 0)
        self.assertIn("The Hacker Apartment", output)

    def test_main_routes_missing_visit_key(self):
        exit_code, output = self.capture_main(["visit"])

        self.assertEqual(exit_code, 2)
        self.assertIn("A world key is required.", output)

    def test_main_routes_unknown_visit_key(self):
        exit_code, output = self.capture_main(["visit", "unknown-place"])

        self.assertEqual(exit_code, 2)
        self.assertIn("Unknown world key: unknown-place", output)

    def test_main_rejects_malformed_visit_usage(self):
        exit_code, output = self.capture_main(
            ["visit", "hacker-apartment", "extra"]
        )

        self.assertEqual(exit_code, 2)
        self.assertIn("Visit accepts exactly one world key.", output)
        for world in ALL_WORLDS:
            self.assertIn(f"- {world.stable_key}", output)

    def test_direct_script_visit_uses_utf8(self):
        studio_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "forge/main.py", "visit", "coffee-cafe"],
            cwd=studio_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("The Coffee Café", result.stdout)
        self.assertIn("Someone has already poured your coffee.", result.stdout)


if __name__ == "__main__":
    unittest.main()

import json
from pathlib import Path
import subprocess
import sys
import unittest

from forge.compiler import compile_render_spec


STUDIO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = STUDIO_ROOT / "build/render_specs/hacker-apartment.render.json"


class CompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, "forge/main.py", "compile", "hacker-apartment"],
            cwd=STUDIO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout)
        cls.command_result = result
        cls.spec = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))

    def test_compile_command_succeeds(self):
        self.assertEqual(self.command_result.returncode, 0)
        self.assertIn("hacker-apartment.render.json", self.command_result.stdout)

    def test_render_spec_is_valid_json(self):
        self.assertEqual(self.spec["world"], "hacker-apartment")

    def test_required_renderer_data_is_populated(self):
        for field in ("immutable", "objects", "lighting", "motion_candidates"):
            with self.subTest(field=field):
                self.assertTrue(self.spec[field])

    def test_camera_is_static(self):
        self.assertEqual(self.spec["camera"]["movement"], "static")

    def test_desk_is_primary_focus(self):
        self.assertEqual(self.spec["composition"]["primary_focus"], "desk")

    def test_file_matches_compiler_output(self):
        self.assertEqual(self.spec, compile_render_spec("hacker-apartment"))


if __name__ == "__main__":
    unittest.main()

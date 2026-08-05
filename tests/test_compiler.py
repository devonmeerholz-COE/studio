import json
from pathlib import Path
import subprocess
import sys
import unittest

from forge.compiler import compile_render_spec, compile_scene_graph


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
        for field in (
            "immutable_canon", "episode_brief", "scene_graph", "camera",
            "composition", "hero_objects", "room_layout", "workstation",
            "future_markers", "city", "canonical_objects", "bonsai", "materials",
            "lighting", "colour_script", "story", "non_negotiable", "forbidden",
            "motion_candidates",
        ):
            with self.subTest(field=field):
                self.assertTrue(self.spec[field])

    def test_immutable_canon_is_concise_and_complete(self):
        immutable = self.spec["immutable_canon"]
        rendered = "\n".join(f"- {fact}" for fact in immutable)
        self.assertLess(len(rendered.splitlines()), 35)
        for fact in (
            "static eye-level 35mm wide 16:9 camera",
            "exactly three identical large monitors",
            "large mature Bonsai in the foreground, inside the room, left of centre",
            "no missing hero objects",
        ):
            self.assertIn(fact, immutable)

    def test_episode_brief_describes_episode_thirteen(self):
        brief = self.spec["episode_brief"]
        self.assertEqual(brief["episode"], 13)
        self.assertEqual(brief["time_advanced"], "three months")
        self.assertEqual(len(brief["changes"]), 9)
        self.assertIn("coffee mug has moved", brief["changes"])

    def test_camera_is_static(self):
        self.assertEqual(self.spec["camera"]["movement"], "static")

    def test_camera_defines_complete_view(self):
        self.assertEqual(
            self.spec["camera"]["height"],
            "eye-level, approximately 1.6 metres",
        )
        self.assertEqual(self.spec["camera"]["framing"], "wide cinematic 16:9 view")
        self.assertEqual(
            self.spec["camera"]["viewpoint"],
            "viewer positioned naturally inside the room",
        )
        self.assertEqual(
            self.spec["camera"]["angle"],
            "straight and calm with no dramatic angle",
        )
        self.assertEqual(self.spec["camera"]["resident"], "no visible resident")

    def test_major_visual_anchors_are_explicit(self):
        anchors = {
            "room_layout": (
                "floor-to-ceiling rain-covered windows occupy the rear wall",
                "compact lounge occupies the left third",
                "Bonsai separates the lounge from the workstation",
            ),
            "workstation": (
                "three identical large widescreen monitors",
                "visible repaired cable",
            ),
            "city": ("distant flying traffic", "city remains secondary to the apartment"),
            "canonical_objects": (
                "evolving repaired backpack", "red-panda plush", "practical tools",
            ),
            "forbidden": ("one-monitor desk", "minimalist empty room", "daylight"),
        }
        for section, facts in anchors.items():
            with self.subTest(section=section):
                self.assertTrue(set(facts).issubset(self.spec[section]))

    def test_scene_graph_is_a_normalized_compiler_stage(self):
        graph = self.spec["scene_graph"]
        self.assertEqual(graph, compile_scene_graph("hacker-apartment"))
        self.assertEqual(graph["stage"], "Scene Graph")
        self.assertEqual(
            [node["id"] for node in graph["nodes"]],
            [
                "WINDOW_WALL", "LOUNGE", "COFFEE_TABLE", "BONSAI",
                "WORKSTATION", "PEGBOARD", "SHELVING", "BACKPACK",
                "PURPLE_NEON",
            ],
        )
        bonsai = next(node for node in graph["nodes"] if node["id"] == "BONSAI")
        self.assertEqual(
            bonsai["constraints"],
            [
                "positioned between lounge and workstation",
                "prominent foreground hero object",
                "never pushed against the window",
                "never replaced by a generic plant",
                "does not block the workstation",
            ],
        )

    def test_scene_graph_stage_covers_every_world(self):
        for world_key in (
            "hacker-apartment", "midnight-library", "coffee-cafe",
            "rainy-loft", "space-station",
        ):
            with self.subTest(world_key=world_key):
                graph = compile_scene_graph(world_key)
                self.assertEqual(graph["stage"], "Scene Graph")
                self.assertEqual(graph["world"], world_key)
                self.assertTrue(graph["nodes"])
                for node in graph["nodes"]:
                    self.assertRegex(node["id"], r"^[A-Z][A-Z_]*$")
                    self.assertTrue(node["constraints"])

    def test_desk_is_primary_focus(self):
        self.assertEqual(
            self.spec["composition"]["primary_focus"],
            "triple-monitor workstation",
        )

    def test_file_matches_compiler_output(self):
        self.assertEqual(self.spec, compile_render_spec("hacker-apartment"))


if __name__ == "__main__":
    unittest.main()

import base64
import contextlib
import io
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from forge import main as forge_main
from forge.renderers.fal import (
    CORRECTIVE_MODEL_ID,
    MODEL_ID,
    OUTPUT_IMAGE,
    REQUEST_METADATA,
    SOURCE_IMAGE,
    _load_validator,
    render_hacker_apartment,
)
from forge.vision_inspector import OBSERVATION_FIELDS, VISION_ENDPOINT


STUDIO_ROOT = Path(__file__).resolve().parents[1]


class DownloadResponse:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return b"generated image"


class FalRendererTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        for relative in (
            "WORLD_BIBLE.md",
            "ART_DIRECTION.md",
            "OBJECTS.md",
            "artwork_briefs/hacker-apartment-v2.md",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                (STUDIO_ROOT / relative).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        source = self.root / SOURCE_IMAGE
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(b"source image")

        self.fal = Mock()
        self.fal.subscribe.side_effect = self.subscribe

    def subscribe(self, model_id, **kwargs):
        if model_id == VISION_ENDPOINT:
            observations = {key: True for key in OBSERVATION_FIELDS}
            return {"choices": [{"message": {"content": json.dumps(observations)}}]}
        return {"images": [{"url": "https://result.example/output.png"}]}

    def call_for(self, model_id):
        return next(
            call for call in self.fal.subscribe.call_args_list
            if call.args[0] == model_id
        )

    def tearDown(self):
        self.temporary.cleanup()

    def render(self):
        with patch.dict(os.environ, {"FAL_KEY": "secret-test-key"}, clear=False):
            return render_hacker_apartment(
                self.root,
                fal_module=self.fal,
                load_environment=Mock(),
                open_url=Mock(return_value=DownloadResponse()),
            )

    def test_calls_text_to_image_model_without_source_image(self):
        self.assertEqual(self.render(), 0)
        self.fal.upload_file.assert_not_called()
        arguments = self.call_for(MODEL_ID).kwargs["arguments"]
        self.assertNotIn("image_url", arguments)
        self.assertEqual(arguments["image_size"], "landscape_16_9")
        self.assertEqual(arguments["num_images"], 1)
        self.assertEqual(arguments["output_format"], "png")

    def test_attempt_one_prompt_contains_only_immutable_and_episode_layers(self):
        self.assertEqual(self.render(), 0)
        prompt = self.call_for(MODEL_ID).kwargs["arguments"]["prompt"]
        for phrase in (
            "IMMUTABLE CANON",
            "static eye-level 35mm wide 16:9 camera",
            "large mature Bonsai in the foreground, inside the room, left of centre",
            "EPISODE BRIEF",
            "Episode: 13",
            "software project has visibly progressed",
            "rain is slightly heavier",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), prompt.casefold())
        self.assertNotIn("CORRECTIVE PATCH", prompt)
        for heading in (
            "POSITIONAL CONSTRAINTS", "HERO OBJECTS", "FORBIDDEN OUTCOMES",
            "MOTION CANDIDATES", "MATERIALS", "VISUAL STORY", "COLOUR SCRIPT",
        ):
            self.assertNotIn(heading, prompt)

    def test_writes_image_and_key_free_exact_request_metadata(self):
        self.assertEqual(self.render(), 0)
        self.assertEqual((self.root / OUTPUT_IMAGE).read_bytes(), b"generated image")
        metadata_text = (self.root / REQUEST_METADATA).read_text(encoding="utf-8")
        metadata = json.loads(metadata_text)
        self.assertNotIn("FAL_KEY", metadata_text)
        self.assertNotIn("secret-test-key", metadata_text)
        self.assertNotIn("data:image/png;base64,", metadata_text)
        self.assertEqual(metadata["model"], MODEL_ID)
        self.assertEqual(
            metadata["prompt"],
            self.call_for(MODEL_ID).kwargs["arguments"]["prompt"],
        )
        self.assertEqual(metadata["render_spec"]["world"], "hacker-apartment")
        self.assertIn("scene_graph", metadata["render_spec"])
        self.assertIn("motion_candidates", metadata["render_spec"])
        self.assertEqual(
            metadata["prompt_layers"],
            {
                "immutable_canon": metadata["render_spec"]["immutable_canon"],
                "episode_brief": metadata["render_spec"]["episode_brief"],
                "corrective_patch": None,
            },
        )
        self.assertEqual(metadata["source_image"], SOURCE_IMAGE.as_posix())
        self.assertNotIn("image_url", metadata)

    def test_missing_observations_fail_validation(self):
        validation = _load_validator().validate({})
        self.assertEqual(validation["passed_rules"], [])
        self.assertEqual(len(validation["failed_rules"]), len(OBSERVATION_FIELDS))
        self.assertEqual(validation["overall_score"]["earned"], 0)

    def test_rendered_pixels_are_inspected_before_scoring(self):
        self.assertEqual(self.render(), 0)
        models = [call.args[0] for call in self.fal.subscribe.call_args_list]
        self.assertEqual(models[:2], [MODEL_ID, VISION_ENDPOINT])
        report = json.loads(
            (self.root / OUTPUT_IMAGE.with_name(
                f"{OUTPUT_IMAGE.stem}-attempt-1.validator.json"
            )).read_text(encoding="utf-8")
        )
        self.assertEqual(set(report["observations"]), set(OBSERVATION_FIELDS))

    def test_corrective_prompt_retains_full_brief_and_pixel_requirements(self):
        first = {key: True for key in OBSERVATION_FIELDS}
        failed_ids = tuple(OBSERVATION_FIELDS[:8])
        for key in failed_ids:
            first[key] = False
        second = {key: True for key in OBSERVATION_FIELDS}
        vision_results = iter((first, second))

        def subscribe(model_id, **kwargs):
            if model_id == VISION_ENDPOINT:
                observed = next(vision_results)
                return {"output": {"text": json.dumps(observed)}}
            return {"images": [{"url": "https://result.example/output.png"}]}

        self.fal.subscribe.side_effect = subscribe
        self.assertEqual(self.render(), 0)
        corrective = self.call_for(CORRECTIVE_MODEL_ID).kwargs["arguments"]["prompt"]
        original = self.call_for(MODEL_ID).kwargs["arguments"]["prompt"]
        validation = _load_validator().validate({"observations": first})
        self.assertTrue(corrective.startswith(original))
        self.assertIn("CORRECTIVE PATCH", corrective)
        self.assertEqual(corrective.rsplit("\n\n", 1)[-1].splitlines()[0], "Preserve these already-passing requirements:")
        for failed_label in validation["failed_rules"]:
            self.assertIn(failed_label, corrective)
        for passed_label in validation["passed_rules"]:
            self.assertIn(f"- {passed_label}\n", corrective + "\n")
        self.assertIn(
            "Preserve these already-passing requirements",
            corrective,
        )
        self.assertGreater(
            corrective.index("CORRECTIVE PATCH"),
            corrective.index("EPISODE BRIEF"),
        )
        metadata = json.loads(
            (self.root / REQUEST_METADATA).read_text(encoding="utf-8")
        )
        self.assertEqual(
            metadata["prompt_layers"]["corrective_patch"],
            {
                "failed_rules": validation["failed_rules"],
                "passed_rules": validation["passed_rules"],
            },
        )
        self.assertEqual(
            self.call_for(CORRECTIVE_MODEL_ID).kwargs["arguments"][
                "image_prompt_strength"
            ],
            0.65,
        )

    def test_corrective_attempts_use_previous_pixels_and_write_each_prompt(self):
        failing = {key: True for key in OBSERVATION_FIELDS}
        for key in OBSERVATION_FIELDS[:8]:
            failing[key] = False
        passing = {key: True for key in OBSERVATION_FIELDS}
        vision_results = iter((failing, failing, passing))
        generated_urls = iter(("https://result/one.png", "https://result/two.png", "https://result/three.png"))

        def subscribe(model_id, **kwargs):
            if model_id == VISION_ENDPOINT:
                return {"text": json.dumps(next(vision_results))}
            return {"images": [{"url": next(generated_urls)}]}

        class AttemptResponse(DownloadResponse):
            def __init__(self, content):
                self.content = content

            def read(self):
                return self.content

        def open_url(url):
            return AttemptResponse(url.encode("ascii"))

        self.fal.subscribe.side_effect = subscribe
        with patch.dict(os.environ, {"FAL_KEY": "secret-test-key"}, clear=False):
            result = render_hacker_apartment(
                self.root,
                fal_module=self.fal,
                load_environment=Mock(),
                open_url=open_url,
            )
        self.assertEqual(result, 0)

        corrective_calls = [
            call for call in self.fal.subscribe.call_args_list
            if call.args[0] == CORRECTIVE_MODEL_ID
        ]
        self.assertEqual(len(corrective_calls), 2)
        original_prompt = self.call_for(MODEL_ID).kwargs["arguments"]["prompt"]
        validation = _load_validator().validate({"observations": failing})
        for call, expected_source in zip(
            corrective_calls,
            (b"https://result/one.png", b"https://result/two.png"),
        ):
            arguments = call.kwargs["arguments"]
            self.assertTrue(arguments["prompt"].startswith(original_prompt))
            for label in validation["failed_rules"] + validation["passed_rules"]:
                self.assertIn(f"- {label}", arguments["prompt"])
            self.assertEqual(arguments["image_prompt_strength"], 0.65)
            image_url = arguments["image_url"]
            encoded = image_url.removeprefix("data:image/png;base64,")
            self.assertEqual(base64.b64decode(encoded), expected_source)

        generation_calls = [
            call for call in self.fal.subscribe.call_args_list
            if call.args[0] in {MODEL_ID, CORRECTIVE_MODEL_ID}
        ]
        for attempt, call in enumerate(generation_calls, start=1):
            prompt_path = self.root / OUTPUT_IMAGE.with_name(
                f"{OUTPUT_IMAGE.stem}-attempt-{attempt}.prompt.txt"
            )
            self.assertTrue(prompt_path.is_file())
            self.assertEqual(
                prompt_path.read_text(encoding="utf-8"),
                call.kwargs["arguments"]["prompt"],
            )

    def test_malformed_render_usage_returns_nonzero(self):
        for args in (["render"], ["render", "hacker-apartment", "extra"]):
            with self.subTest(args=args):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertNotEqual(forge_main.main(args), 0)

    def test_existing_commands_remain_unchanged(self):
        with patch("forge.compiler.compile_world", return_value=17) as compile_world:
            self.assertEqual(forge_main.main(["compile", "hacker-apartment"]), 17)
            compile_world.assert_called_once_with("hacker-apartment")
        with patch("forge.main.doctor", return_value=19) as doctor:
            self.assertEqual(forge_main.main(["doctor"]), 19)
            doctor.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

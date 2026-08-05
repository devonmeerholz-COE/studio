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
    MODEL_ID,
    OUTPUT_IMAGE,
    REQUEST_METADATA,
    SOURCE_IMAGE,
    render_hacker_apartment,
)


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
        self.fal.subscribe.return_value = {
            "images": [{"url": "https://result.example/output.png"}]
        }

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

    def test_embeds_source_as_data_uri_and_calls_correct_model(self):
        self.assertEqual(self.render(), 0)
        self.fal.upload_file.assert_not_called()
        self.assertEqual(self.fal.subscribe.call_args.args[0], MODEL_ID)
        image_url = self.fal.subscribe.call_args.kwargs["arguments"]["image_url"]
        self.assertTrue(image_url.startswith("data:image/png;base64,"))

    def test_instruction_preserves_canon_and_progresses_world(self):
        self.assertEqual(self.render(), 0)
        prompt = self.fal.subscribe.call_args.kwargs["arguments"]["prompt"]
        for phrase in (
            "camera position", "room layout", "desk placement",
            "Neo-Tokyo skyline", "flying cars", "purple code-symbol neon",
            "Bonsai in its current location", "rainy nighttime atmosphere",
            "empty chair", "three months", "careful pruning", "nearly full",
            "new notebook", "software project has visibly progressed",
            "cable carefully repaired", "personal keepsake",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, prompt)

    def test_writes_image_and_key_free_exact_request_metadata(self):
        self.assertEqual(self.render(), 0)
        self.assertEqual((self.root / OUTPUT_IMAGE).read_bytes(), b"generated image")
        metadata_text = (self.root / REQUEST_METADATA).read_text(encoding="utf-8")
        metadata = json.loads(metadata_text)
        self.assertNotIn("FAL_KEY", metadata_text)
        self.assertNotIn("secret-test-key", metadata_text)
        self.assertNotIn("data:image/png;base64,", metadata_text)
        self.assertEqual(metadata["model"], MODEL_ID)
        self.assertEqual(metadata["source_image"], SOURCE_IMAGE.as_posix())
        self.assertNotIn("image_url", metadata)

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

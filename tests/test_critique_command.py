import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from forge import main as forge_main
from forge.critique_command import critique_file
from tests.test_evidence_loader import evidence_text


class CritiqueCommandTests(unittest.TestCase):
    def write_evidence(self, content=None):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "evidence.md"
        path.write_text(evidence_text() if content is None else content, encoding="utf-8")
        return path

    def capture(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = forge_main.main(args)
        return code, output.getvalue()

    def test_valid_file_produces_report_and_returns_zero(self):
        code, output = self.capture(("critique", str(self.write_evidence())))

        self.assertEqual(code, 0)
        self.assertIn("Artwork Context", output)
        self.assertIn("World Keeper Review", output)

    def test_missing_unknown_and_malformed_input_return_two(self):
        code, output = self.capture(("critique",))
        self.assertEqual(code, 2)
        self.assertIn("An evidence file is required.", output)

        unknown = self.write_evidence(evidence_text(world="`unknown-world`"))
        code, output = self.capture(("critique", str(unknown)))
        self.assertEqual(code, 2)
        self.assertIn("unknown world key", output)

        malformed = self.write_evidence("not evidence")
        code, output = self.capture(("critique", str(malformed)))
        self.assertEqual(code, 2)
        self.assertIn("Could not critique artwork", output)

    def test_unknown_object_and_malformed_usage_return_two(self):
        unknown = self.write_evidence(evidence_text(present="- `unknown-object`"))
        code, output = self.capture(("critique", str(unknown)))
        self.assertEqual(code, 2)
        self.assertIn("unknown object ID", output)

        code, output = self.capture(("critique", "one.md", "two.md"))
        self.assertEqual(code, 2)
        self.assertIn("exactly one evidence file", output)

    def test_direct_execution_preserves_utf8(self):
        path = self.write_evidence(
            evidence_text(
                advisory="""### Observation

Principle:

```text
Quiet café detail
```

Observation:

```text
The handwritten note feels familiar.
```""",
            )
        )
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "forge/main.py", "critique", str(path)],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Quiet café detail", result.stdout)

    def test_existing_commands_remain_routed(self):
        for args in ((), ("doctor",), ("visit", "hacker-apartment"), ("inspect", "hacker-apartment")):
            with self.subTest(args=args):
                code, _ = self.capture(list(args))
                self.assertIn(code, (0, 1))


if __name__ == "__main__":
    unittest.main()

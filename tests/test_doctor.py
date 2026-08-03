import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "forge" / "main.py"
SPEC = importlib.util.spec_from_file_location("forge_main", MODULE_PATH)
forge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(forge)


class DoctorChecksTests(unittest.TestCase):
    @mock.patch.object(forge.shutil, "which")
    def test_check_command_reports_available_command(self, which):
        which.return_value = "C:/tools/ffmpeg.exe"

        self.assertEqual(
            forge.check_command("FFmpeg", "ffmpeg", "Install it."),
            ("FFmpeg", True, ""),
        )

    @mock.patch.object(forge.shutil, "which", return_value=None)
    def test_check_command_reports_missing_command_with_fix(self, _which):
        self.assertEqual(
            forge.check_command("FFmpeg", "ffmpeg", "Install it."),
            ("FFmpeg", False, "Install it."),
        )

    def test_check_file_reports_present_and_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            present = root / "PROJECT.md"
            present.write_text("Studio", encoding="utf-8")

            self.assertEqual(forge.check_file("PROJECT.md", present), ("PROJECT.md", True, ""))
            self.assertFalse(forge.check_file("AGENTS.md", root / "AGENTS.md")[1])

    @mock.patch.object(forge.subprocess, "run")
    def test_check_git_repository_accepts_work_tree(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="true\n", stderr="")

        self.assertEqual(forge.check_git_repository(Path("studio")), ("Git repository", True, ""))

    @mock.patch.object(forge, "doctor_checks")
    def test_doctor_reports_success(self, checks):
        checks.return_value = [("Python", True, ""), ("Git", True, "")]
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = forge.doctor()

        self.assertEqual(exit_code, 0)
        self.assertIn("[OK] Python", output.getvalue())
        self.assertIn("All systems operational.", output.getvalue())

    @mock.patch.object(forge, "doctor_checks")
    def test_doctor_reports_missing_items_and_fixes(self, checks):
        checks.return_value = [("Python", True, ""), ("FFmpeg", False, "Install FFmpeg.")]
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            exit_code = forge.doctor()

        self.assertEqual(exit_code, 1)
        self.assertIn("[MISSING] FFmpeg", output.getvalue())
        self.assertIn("- FFmpeg: Install FFmpeg.", output.getvalue())


class CommandTests(unittest.TestCase):
    @mock.patch.object(forge, "open_studio")
    def test_no_command_preserves_welcome_behavior(self, open_studio):
        self.assertEqual(forge.main([]), 0)
        open_studio.assert_called_once_with()

    @mock.patch.object(forge, "doctor", return_value=0)
    def test_doctor_command_runs_doctor(self, doctor):
        self.assertEqual(forge.main(["doctor"]), 0)
        doctor.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

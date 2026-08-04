"""
Super Chilled Studio
Forge

The first line of code.

Every place begins with hope.
"""

from datetime import datetime
from pathlib import Path
import shutil
import subprocess
import sys


STUDIO_ROOT = Path(__file__).resolve().parent.parent


def check_command(name, command, fix):
    if shutil.which(command):
        return name, True, ""
    return name, False, fix


def check_file(name, path):
    if path.is_file():
        return name, True, ""
    return name, False, f"Restore {name} at {path}."


def check_git_repository(root):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return "Git repository", False, "Install Git, then run 'git init' in the Studio root."

    if result.returncode == 0 and result.stdout.strip() == "true":
        return "Git repository", True, ""
    return "Git repository", False, "Run 'git init' in the Studio root."


def doctor_checks(root=STUDIO_ROOT):
    return [
        ("Python", True, ""),
        check_command("Git", "git", "Install Git and ensure it is available on PATH."),
        check_command("FFmpeg", "ffmpeg", "Install FFmpeg and ensure it is available on PATH."),
        check_command("FFprobe", "ffprobe", "Install FFmpeg (which includes FFprobe) and ensure it is available on PATH."),
        check_command("Node.js", "node", "Install Node.js and ensure it is available on PATH."),
        check_command("npm", "npm", "Install Node.js (which includes npm) and ensure it is available on PATH."),
        check_command("Codex CLI", "codex", "Install the Codex CLI and ensure it is available on PATH."),
        check_file("PROJECT.md", root / "PROJECT.md"),
        check_file("AGENTS.md", root / "AGENTS.md"),
        check_git_repository(root),
    ]


def doctor(root=STUDIO_ROOT):
    print("SUPER CHILLED STUDIO")
    print("Forge is warm.")
    print()
    print("Checking Studio...")
    print()

    checks = doctor_checks(root)
    for name, available, _ in checks:
        status = "OK" if available else "MISSING"
        print(f"[{status}] {name}")

    missing = [(name, fix) for name, available, fix in checks if not available]
    print()
    if not missing:
        print("All systems operational.")
        print("Let's build something beautiful.")
        return 0

    print("Studio needs attention:")
    for name, fix in missing:
        print(f"- {name}: {fix}")
    return 1


def open_studio():
    print("=" * 60)
    print("🌧️  SUPER CHILLED STUDIO")
    print("=" * 60)
    print()
    print("Welcome home.")
    print()
    print(f"Studio opened: {datetime.now():%Y-%m-%d %H:%M}")
    print()
    print("Mission:")
    print("Create places worth returning to.")
    print()
    print("Current status:")
    print(" • The Studio is open")
    print(" • Forge is awake")
    print(" • Atlas is standing by")
    print(" • The World Keeper has arrived")
    print()
    print("Let's build something beautiful.")
    print("=" * 60)


def main(args=None):
    args = sys.argv[1:] if args is None else args
    if not args:
        open_studio()
        return 0
    if args == ["doctor"]:
        return doctor()
    if args[0] == "visit":
        from forge.visit import malformed_visit_usage, visit

        if len(args) == 1:
            return visit(None)
        if len(args) == 2:
            return visit(args[1])
        return malformed_visit_usage()
    if args[0] == "inspect":
        from forge.inspection import inspect_world, malformed_inspect_usage

        if len(args) == 1:
            return inspect_world(None)
        if len(args) == 2:
            return inspect_world(args[1])
        return malformed_inspect_usage()

    print(f"Unknown command: {' '.join(args)}")
    print("Usage: python forge/main.py [doctor | visit WORLD_KEY | inspect WORLD_KEY]")
    return 2


if __name__ == "__main__":
    studio_root = str(STUDIO_ROOT)
    if studio_root not in sys.path:
        sys.path.insert(0, studio_root)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())

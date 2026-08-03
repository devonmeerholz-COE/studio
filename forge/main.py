"""
Super Chilled Studio
Forge

The first line of code.

Every place begins with hope.
"""

from datetime import datetime


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


if __name__ == "__main__":
    open_studio()
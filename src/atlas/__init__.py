from pathlib import Path


def get_version() -> str:
    """Return the ATLAS package version."""
    version_file = Path(__file__).with_name("VERSION")
    return version_file.read_text(encoding="utf-8").strip()

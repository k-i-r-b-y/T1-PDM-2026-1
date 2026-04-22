from __future__ import annotations

from pathlib import Path


def ensure_directory(path: Path) -> Path:
    """Create a directory if it does not exist and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def project_root_from(file_path: str) -> Path:
    """Resolve the repository root from a script path."""
    return Path(file_path).resolve().parents[1]

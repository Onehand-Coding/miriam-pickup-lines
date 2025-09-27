import os
from pathlib import Path

def find_project_root(start_path: Path = None) -> Path:
    """Find project root by locating pyproject.toml file."""
    if start_path is None:
        start_path = Path(__file__).resolve()

    # If file path was passed, get its parent directory
    if start_path.is_file():
        start_path = start_path.parent

    # Traverse up the directory tree
    for parent in [start_path, *start_path.parents]:
        if (parent / "pyproject.toml").exists():
            return parent

    # If no pyproject.toml found, return original path
    return start_path


PROJECT_ROOT = find_project_root()

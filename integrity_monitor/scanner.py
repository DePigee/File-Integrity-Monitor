"""
path.relative_to(folder) converts a full path to one relative to the scanned folder. Use relative paths so the baseline still works if the folder moves.
.as_posix() on a path gives forward slashes on every operating system, so baselines are portable.
"""

from pathlib import Path

from .hasher import hash_file


def scan_directory(folder: str) -> dict[str, str]:
    if not Path(folder).is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")

    results = {}

    for item in sorted(Path(folder).rglob("*")):
        if item.is_file():
            relative_path = item.relative_to(folder).as_posix()
            try:
                results[relative_path] = hash_file(str(item))
            except PermissionError:
                print(f"file skipped: {relative_path}")
                continue
    return results



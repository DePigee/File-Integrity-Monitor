import argparse
import sys

from .baseline import load_baseline, save_baseline
from .comparer import compare
from .scanner import scan_directory

DEFAULT_BASELINE = "baseline.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="integrity_monitor",
        description="Detect added, modified, and deleted files using SHA-256 baselines.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    baseline = subparsers.add_parser("baseline", help="Save a baseline of a folder")
    baseline.add_argument("folder", help="Folder to scan")
    baseline.add_argument("--output", default=DEFAULT_BASELINE, help="Baseline file to write")

    check = subparsers.add_parser("check", help="Compare a folder to a saved baseline")
    check.add_argument("folder", help="Folder to scan")
    check.add_argument("--baseline", default=DEFAULT_BASELINE, help="Baseline file to read")
    return parser


def run_baseline(folder: str, output: str) -> int:
    try:
        data = scan_directory(folder)
    except NotADirectoryError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    save_baseline(data, output)
    print(f"Baseline saved: {len(data)} files")
    return 0


def run_check(folder: str, baseline_path: str) -> int:
    try:
        old = load_baseline(baseline_path)
        new = scan_directory(folder)
    except (FileNotFoundError, NotADirectoryError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    changes = compare(old, new)
    for path in changes["modified"]:
        print(f"Modified: {path}")
    for path in changes["added"]:
        print(f"Added:    {path}")
    for path in changes["deleted"]:
        print(f"Deleted:  {path}")

    if not any(changes.values()):
        print("No changes detected")
        return 0
    return 1


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "baseline":
        return run_baseline(args.folder, args.output)
    return run_check(args.folder, args.baseline)
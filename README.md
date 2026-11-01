# File Integrity Monitor

A Python command-line tool that detects added, modified, and deleted files in a folder by comparing SHA-256 hashes against a saved baseline.

## Features

- Scans a folder and all of its subfolders
- Saves a baseline of `{relative path: SHA-256 hash}` as JSON
- Reports added, modified, and deleted files compared to the baseline
- Hashes files in chunks, so large files don't use much memory
- Stores relative paths, so a baseline still works if the folder moves
- Returns exit codes that scripts can use: `0` no changes, `1` changes found, `2` error

## Installation

```bash
git clone https://github.com/[your-username]/file-integrity-monitor.git
cd file-integrity-monitor
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Requires Python 3.10 or newer.

## Usage

Create a baseline of a folder:

```bash
python -m integrity_monitor.main baseline scan_me
```

```
Baseline saved: 2 files
```

Check the folder against the baseline later:

```bash
python -m integrity_monitor.main check scan_me
```

If nothing changed:

```
No changes detected
```

If files changed:

```
Modified: a.txt
Added:    new.txt
Deleted:  sub/b.txt
```

By default the baseline is saved to and read from `baseline.json` in the current directory. Use `--output` (with `baseline`) or `--baseline` (with `check`) to choose a different file:

```bash
python -m integrity_monitor.main baseline scan_me --output ~/baselines/scan_me.json
python -m integrity_monitor.main check scan_me --baseline ~/baselines/scan_me.json
```

> **Note:** Store the baseline file outside the folder you are monitoring. Otherwise the baseline file itself will show up as a change.

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success, or no changes detected |
| 1 | Changes detected |
| 2 | Error (missing folder, missing or corrupted baseline) |

## Running the tests

```bash
python -m pytest
```

The suite has [number] tests covering hashing, scanning, baseline storage, change detection, and the CLI. Tests use pytest's `tmp_path` fixture, so they build temporary folders and leave nothing behind.

## Project structure

```
file-integrity-monitor/
├── integrity_monitor/
│   ├── hasher.py       # SHA-256 of one file, read in chunks
│   ├── scanner.py      # Walk a folder, build {path: hash}
│   ├── baseline.py     # Save and load the baseline as JSON
│   ├── comparer.py     # Find added, modified, and deleted files
│   ├── cli.py          # argparse commands: baseline and check
│   └── main.py         # Entry point
├── test/               # pytest test suite
├── requirements.txt
└── README.md
```

## Design decisions

**Chunked hashing.** Files are read 8 KB at a time and fed to the hasher incrementally, so memory use stays small regardless of file size. A test compares the chunked result against hashing a 100,000-byte file in one call, to catch any dropped or repeated chunk.

**Relative paths with forward slashes.** The baseline stores paths relative to the scanned folder, using `as_posix()`. That keeps baselines portable if the folder moves or is checked on another operating system.

**`compare` is a pure function.** It takes two dictionaries and returns what changed, with no file access or printing. Set operations find added and deleted paths, and a hash comparison finds modified ones. This made the core logic simple to test.

**Fail loudly on bad input.** A missing folder raises an error instead of returning an empty result, because an empty scan would look like every file was deleted. A missing or corrupted baseline stops the check with a clear message instead of being treated as an empty baseline.

**Separation of concerns.** Hashing, scanning, storage, comparison, and the CLI each live in their own module, so each can be tested on its own.

## Threat model and limitations

**What it detects:** changes to file contents, and files added or removed, since the baseline was created.

**What it does not detect:**

- **Tampering with the baseline.** Anyone who can edit `baseline.json` can hide changes. In real use, the baseline should be stored somewhere protected, such as read-only or on a separate system.
- **Changes between scans.** A file that is modified and then restored before the next check goes unnoticed.
- **Metadata-only changes.** Permissions, ownership, and timestamps are not tracked, only contents.
- **Unreadable files.** Files the tool lacks permission to read are skipped with a message, which means they are not monitored.
- **A compromised tool.** If the tool or Python itself is modified, its results cannot be trusted.

## Future work

- Report skipped files in the `check` summary
- Optional ignore patterns, such as `.git/` or `*.log`
- Sign or encrypt the baseline to detect tampering
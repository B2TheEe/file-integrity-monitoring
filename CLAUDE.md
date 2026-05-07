# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the tool

```bash
python fim.py
```

Prompts for a directory path at runtime. No build step or package manager required — stdlib only.

## Architecture

A Python file integrity monitor (FIM) that detects unauthorized changes to files by comparing SHA-256 hashes against a saved baseline.

**Data flow:**

1. `FileScanner.scan_directory` walks the target directory via `os.walk` and returns a list of full file paths, excluding `.git/`, `baseline.json`, and `fim.log`.
2. `Monitor.build_scan` hashes each path with `FileHasher` to produce a `{filepath: hash}` dict.
3. `BaselineManager.load_baseline` loads `baseline.json`. If none exists, the current scan is saved as the initial baseline and the run ends.
4. `BaselineManager.compare` diffs the baseline against the current scan, returning `added`, `removed`, and `modified` buckets.
5. `AlertManager.process_changes` prints timestamped alerts to stdout and appends them to `fim.log`.
6. `BaselineManager.save_baseline` writes the current scan as the new baseline.

**Module responsibilities:**

- `fim.py` — `Monitor`: orchestrates the full scan/compare/alert/save cycle. Entry point.
- `filescanner.py` — `FileScanner`: directory walker; exclusions defined in `EXCLUDE_DIRS` and `EXCLUDE_FILES` class attributes.
- `filehasher.py` — `FileHasher`: SHA-256 hashing; `load_file` returns raw `bytes`, passed directly to `hashlib.sha256()`.
- `baselinemanager.py` — `BaselineManager`: persists baseline as `baseline.json` (path configurable via constructor); `compare` returns a dict with `added`, `removed`, `modified` keys.
- `alertmanager.py` — `AlertManager`: `send_alert` formats and logs a single change; `process_changes` iterates the full diff dict. Log path configurable via constructor.

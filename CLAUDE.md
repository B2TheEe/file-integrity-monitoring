# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the tool

```bash
python fim.py
```

The entry point prompts for a file path at runtime. There is no build step, package manager, or test suite yet.

## Architecture

This is a Python file integrity monitor (FIM) — a security tool that detects unauthorized changes to files by comparing SHA-256 hashes against a saved baseline.

**Module responsibilities:**

- `fim.py` — `Monitor` class: orchestrates a scan-then-hash loop. Entry point.
- `filescanner.py` — `FileScanner`: walks a directory tree with `os.walk` and lists files.
- `filehasher.py` — `FileHasher`: computes and verifies SHA-256 hashes of individual files.
- `baselinemanager.py` — `BaselineManager`: saves, loads, and diffs baseline snapshots (stubbed).
- `alertmanager.py` — `AlertManager`: emits alerts on detected changes (stubbed).

**Intended data flow:**

1. `FileScanner` enumerates all files under a watched directory.
2. `FileHasher` hashes each file.
3. `BaselineManager` stores the initial hash map and later diffs it against a fresh scan.
4. `AlertManager` fires on any addition, deletion, or modification detected by the diff.

**Current state:** `BaselineManager` and `AlertManager` are empty stubs. `FileHasher.load_file` reads bytes but then calls `.encode()` on the result (which is already `bytes`), causing the hash to always fail silently — this is a known bug to fix.

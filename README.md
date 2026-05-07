# File Integrity Monitor

A Python tool that detects unauthorized changes to files by comparing SHA-256 hashes against a saved baseline.

## Usage

```bash
python fim.py
```

Enter a directory path when prompted. On the first run, the tool saves the current state as a baseline. On subsequent runs, it compares the current state against the baseline and reports any added, removed, or modified files.

Alerts are printed to the console and appended to `fim.log`.

## How it works

1. **Scan** — walks the target directory and collects all file paths
2. **Hash** — computes a SHA-256 hash for each file
3. **Compare** — diffs the current hashes against the saved baseline
4. **Alert** — reports changes and updates the baseline

## Project structure

| File | Description |
|---|---|
| `fim.py` | Entry point; orchestrates the scan/compare/alert flow |
| `filescanner.py` | Walks a directory tree and returns file paths |
| `filehasher.py` | Computes and verifies SHA-256 hashes |
| `baselinemanager.py` | Saves, loads, and diffs baseline snapshots (JSON) |
| `alertmanager.py` | Prints alerts and writes to `fim.log` |

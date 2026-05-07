import json
import os

class BaselineManager():
    def __init__(self, baseline_path='baseline.json'):
        self.baseline_path = baseline_path

    def save_baseline(self, baseline):
        with open(self.baseline_path, 'w') as f:
            json.dump(baseline, f, indent=2)

    def load_baseline(self):
        if not os.path.exists(self.baseline_path):
            return None
        with open(self.baseline_path, 'r') as f:
            return json.load(f)

    def compare(self, baseline, current_scan):
        baseline_files = set(baseline.keys())
        current_files = set(current_scan.keys())

        added = {f: current_scan[f] for f in current_files - baseline_files}
        removed = {f: baseline[f] for f in baseline_files - current_files}
        modified = {
            f: {'baseline': baseline[f], 'current': current_scan[f]}
            for f in baseline_files & current_files
            if baseline[f] != current_scan[f]
        }

        return {'added': added, 'removed': removed, 'modified': modified}

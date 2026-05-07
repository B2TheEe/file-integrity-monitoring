from filescanner import FileScanner
from filehasher import FileHasher
from baselinemanager import BaselineManager
from alertmanager import AlertManager


class Monitor():
    def __init__(self, filepath):
        self.filepath = filepath
        self.baseline_manager = BaselineManager()
        self.alert_manager = AlertManager(log_path='fim.log')
        self.file_hasher = FileHasher()

    def build_scan(self):
        scanner = FileScanner()
        filepaths = scanner.scan_directory(self.filepath)
        return {fp: self.file_hasher.calculate_hash(fp) for fp in filepaths}

    def run(self):
        current_scan = self.build_scan()
        baseline = self.baseline_manager.load_baseline()

        if baseline is None:
            print("No baseline found. Saving current state as baseline.")
            self.baseline_manager.save_baseline(current_scan)
            return

        changes = self.baseline_manager.compare(baseline, current_scan)
        if any(changes.values()):
            self.alert_manager.process_changes(changes)
        else:
            print("No changes detected.")

        self.baseline_manager.save_baseline(current_scan)


def main(filepath):
    monitor = Monitor(filepath)
    monitor.run()

if __name__ == '__main__':
    filepath = input("Enter directory path to monitor: ")
    main(filepath)

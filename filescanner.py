import os


class FileScanner():
    def __init__(self):
        pass

    EXCLUDE_DIRS = {'.git'}
    EXCLUDE_FILES = {'baseline.json'}

    def scan_directory(self, path):
        filepaths = []
        for folder, subs, files in os.walk(path):
            subs[:] = [s for s in subs if s not in self.EXCLUDE_DIRS]
            for filename in files:
                if filename not in self.EXCLUDE_FILES:
                    filepaths.append(os.path.join(folder, filename))
        return filepaths

    def get_all_files(self, path):
        pass

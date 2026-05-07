import os


class FileScanner():
    def __init__(self):
        pass

    def scan_directory(self, path):
        filepaths = []
        for folder, subs, files in os.walk(path):
            for filename in files:
                filepaths.append(os.path.join(folder, filename))
        return filepaths

    def get_all_files(self, path):
        pass

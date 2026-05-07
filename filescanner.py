import os
import sys
from sys import path


class FileScanner():
    def __init__(self):
        pass

    def scan_directory(self, path):
        for folder, subs, files in os.walk(path):
            #with open(os.path.join(folder, 'python-outfile.txt'), 'w') as dest:
                for filename in files:
                    with open(os.path.join(folder, filename), 'r') as src:
                        print(filename)
                        #dest.write(src.read())
                return files

    def get_all_files(self, path):
        pass








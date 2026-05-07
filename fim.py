import os
from filescanner import FileScanner
from filehasher import FileHasher

class Monitor():
    def __init__(self,filepath):
        self.filepath = filepath

    def run(self):
        file_scanner = FileScanner()
        dirscan = file_scanner.scan_directory(self.filepath)
        while dirscan:

            file_hash = FileHasher()
            hash = file_hash.calculate_hash(self.filepath)
            isHash = file_hash.verify_hash(self.filepath,hash)
            print(isHash)





def main(filepath):
    monitor = Monitor(filepath)
    monitor.run()
if __name__ == '__main__':
    filepath = input("Enter file path: ")
    main(filepath)
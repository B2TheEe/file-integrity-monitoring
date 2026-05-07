import hashlib

class FileHasher():
    def __init__(self):
        pass
    def calculate_hash(self, filepath):
        content = self.load_file(filepath)
        if content is None:
            return None
        hex_dig = hashlib.sha256(content).hexdigest()
        print(f"Hashed String: {hex_dig}")
        return hex_dig

    def verify_hash(self, filepath, hash):
        content = self.load_file(filepath)
        if content is None:
            return False
        hex_dig = hashlib.sha256(content).hexdigest()
        return hash == hex_dig

    def load_file(self, filepath):
        try:
            with open(filepath, 'rb') as file:
                return file.read()
        except IsADirectoryError:
            print("The specified path is a directory.")
            return None

    def compare(self,baseline, current_scan):
        pass


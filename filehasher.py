import hashlib

class FileHasher():
    def __init__(self):
        pass
    def  calculate_hash(self,filepath):
        try:
            content = self.load_file(filepath)
            hash_object = hashlib.sha256(content.encode())
            hex_dig = hash_object.hexdigest()

            print(f"Hashed String: {hex_dig}")
            return hex_dig
        except AttributeError:
            print("The specified path is a directory.")

    def verify_hash(self,filepath,hash):

        try:
            content = self.load_file(filepath)
            hash_object = hashlib.sha256(content.encode())
            hex_dig = hash_object.hexdigest()
            print(f"Hashed String: {hex_dig}")
            if (hash == hex_dig):
                return True
            else:
                return False
        except AttributeError:
            print("The specified path is a directory.")


        return False

    def load_file(self,filepath):
        try:
            with open(filepath, 'rb') as file:
                content = file.read()
        except IsADirectoryError:
               print("The specified path is a directory.")

    def compare(self,baseline, current_scan):
        pass


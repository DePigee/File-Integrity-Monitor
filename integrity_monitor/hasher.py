import hashlib

CHUNK_SIZE = 8192

def hash_file(path: str)-> str:
    sha256 = hashlib.sha256()

    with open (path, "rb") as file:
        chunk = file.read(CHUNK_SIZE) 

        while chunk:
            sha256.update(chunk)
            chunk = file.read(CHUNK_SIZE) 
    return sha256.hexdigest()
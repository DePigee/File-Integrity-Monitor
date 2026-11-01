from .hasher import hash_file

def main():
     hashed_file = hash_file("test.txt")
     print(hashed_file)

main()
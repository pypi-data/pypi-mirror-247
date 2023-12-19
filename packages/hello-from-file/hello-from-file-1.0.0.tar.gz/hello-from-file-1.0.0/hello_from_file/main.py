import os

def read_hello_file():
    file_path = os.path.join(os.path.dirname(__file__), '../../hello.txt')

    # Read the content from hello.txt
    with open(file_path, 'r') as file:
        content = file.read()

    return content
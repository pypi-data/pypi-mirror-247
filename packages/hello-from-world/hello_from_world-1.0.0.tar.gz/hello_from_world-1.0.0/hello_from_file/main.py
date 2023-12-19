import os

def read_hello_file():
    # Read the content from hello.txt
    with open('../hello.txt', 'r') as file:
        content = file.read()

    return content
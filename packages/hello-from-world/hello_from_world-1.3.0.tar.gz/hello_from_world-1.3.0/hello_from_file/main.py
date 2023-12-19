import os
from json import load
from pkg_resources import resource_stream

def read_hello_file():
    # Construct the absolute path to hello.txt using os.path
    package_directory = os.path.dirname(__file__)
    file_path = os.path.join(package_directory, '..', 'hello.txt')

    # Load the content of hello.txt
    with open(file_path, 'r') as file:
        schema = load(file)

    return schema
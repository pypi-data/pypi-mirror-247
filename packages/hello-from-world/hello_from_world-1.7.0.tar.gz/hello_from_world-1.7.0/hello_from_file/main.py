# import os
# from json import load

# def read_hello_file():
#     # Construct the relative path to hello.txt based on the current working directory
#     package_directory = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(package_directory, '..', 'hello.txt')

#     # Load the content of hello.txt
#     with open(file_path, 'r') as file:
#         schema = load(file)

#     return schema

from json import load
from pkg_resources import resource_stream

def read_hello_file():
    # Read the content from hello.txt
    schema = load(resource_stream('hello_from_file', 'yo.txt'))

    return schema
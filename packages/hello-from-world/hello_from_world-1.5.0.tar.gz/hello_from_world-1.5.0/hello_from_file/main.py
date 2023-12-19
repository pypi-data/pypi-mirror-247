from json import load
from pkg_resources import resource_stream

def read_hello_file():
    # Read the content from hello.txt
    schema = load(resource_stream('hello_from_file', 'yo.txt'))

    return schema
import os

def read_hello_file():
    script_path = os.path.abspath(__file__)

    # Construct the path to hello.txt using os.path
    file_path = os.path.join(os.path.dirname(script_path), '..', 'hello.txt')

    # Read the content of hello.txt
    with open(file_path, 'r') as file:
        content = file.read()

    return content


# from pkg_resources import resource_string

# def read_hello_file():
#     # Read the content from hello.txt
#     content = resource_string('hello_from_file', 'yo.txt').decode('utf-8')

#     return content
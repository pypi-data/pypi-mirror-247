import os

def read_hello_file():
    # Construct the relative path to hello.txt based on the current working directory
    package_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(package_directory, '..', 'hello.txt')

    # Load the content of hello.txt
    with open(file_path, 'r') as file:
        content = file.read()

    return content


# from pkg_resources import resource_string

# def read_hello_file():
#     # Read the content from hello.txt
#     content = resource_string('hello_from_file', 'yo.txt').decode('utf-8')

#     return content
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="hello_from_world",
    version="1.5.0",
    description="Just a random package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    # package_data={'hello_from_file': ['hello_from_file/hello.txt']},
    license="MIT",
)
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="hello_from_world",
    version="1.0.0",
    description="Just a random package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
)
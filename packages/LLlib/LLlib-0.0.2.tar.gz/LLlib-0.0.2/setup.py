from setuptools import setup, find_packages
import json

# Readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Sensitive data
creds = json.load(open("src/credentials.json", "r"))

setup(
    name="LLlib",
    version="0.0.2",
    packages=find_packages(),
    description="A simple Python library for creating linked lists and performing operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hnshlr",
    author_email=creds["author_email"],
    keywords="linkedlist, listnode, linked list, list node, singly linked list",
    url="https://github.com/Hnshlr/LinkedListLibrary",
    license="MIT",
    include_package_data=True
)

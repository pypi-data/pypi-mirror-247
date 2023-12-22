# snake_me_please/setup.py
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="snake_me_please",
    url="https://github.com/AdityaJ7/snake_me_please",
    description="Snake Me Please is a Python package and command-line tool designed to convert user-defined variable names to snake_case in Python files while excluding imported variables and keywords from Python libraries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.7",
    author="Aditya Jetely",
    author_email="ajetely@gmail.com",
    license="public",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "snake-me-please = snake_me_please.converter:main",
        ],
    },
)

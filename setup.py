import codecs
import os

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.in") as f:
    requirements = f.read().splitlines()

# Solution from https://packaging.python.org/guides/single-sourcing-package-version/
def read(rel_path: str) -> str:
    """Read file."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    """Parse version from file content."""
    for line in read(rel_path).splitlines():
        if line.startswith("VERSION"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="audiobook-tags",
    version=get_version("src/audiobook_tags/version.py"),
    author="Andrey Sorokin",
    author_email="andrey@sorokin.engineer",
    description="Fix mp3 tags to use in iTunes/iPhone audiobooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "audiobook-tags=audiobook_tags.main:main",
        ],
    },
    url="https://andgineer.github.io/audiobook-tags/",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=requirements,
    python_requires=">=3.7",
    keywords="audiobook mp3-tags",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

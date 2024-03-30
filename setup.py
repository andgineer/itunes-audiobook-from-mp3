import codecs
import os

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.in") as f:
    requirements = f.read().splitlines()


def get_version() -> str:
    """Parse version from file content."""
    with open("src/audiobook_tags/version.py") as f:
        version_lines = f.read().splitlines()
        for line in version_lines:
            if line.startswith("VERSION"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="audiobook-tags",
    version=get_version(),
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

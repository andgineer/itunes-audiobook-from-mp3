import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("requirements.dev.txt") as f:
    tests_requirements = f.read().splitlines()

from src.audiobook_tags import version

setuptools.setup(
    name="audiobook-tags",
    version=version.VERSION,
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
    tests_require=tests_requirements,
    python_requires=">=3.7",
    keywords="audiobook mp3-tags",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

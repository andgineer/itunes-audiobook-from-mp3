#!/usr/bin/env bash
#
# Pin current dependencies versions.
#
unset CONDA_PREFIX  # if conda is installed, it will mess with the virtual env

START_TIME=$(date +%s)

uv pip compile requirements.in --output-file=requirements.txt --upgrade
REQS_TIME=$(date +%s)

uv pip compile requirements.dev.in --output-file=requirements.dev.txt --upgrade

# Preserve environment markers from .in file that uv strips during compilation
# Add Python version marker to types-eyed3 to support Python 3.10, 3.11, 3.12
if grep -q "^types-eyed3==" requirements.dev.txt; then
    sed -i.bak 's/^types-eyed3==\([0-9.]*\)$/types-eyed3==\1 ; python_version >= "3.12"/' requirements.dev.txt
    rm -f requirements.dev.txt.bak
fi

END_TIME=$(date +%s)

echo "Req‘s compilation time: $((REQS_TIME - $START_TIME)) seconds"
echo "Req‘s dev compilation time: $((END_TIME - REQS_TIME)) seconds"
echo "Total execution time: $((END_TIME - $START_TIME)) seconds"

# do not pin dependencies in the package
scripts/include_pyproject_requirements.py requirements.in

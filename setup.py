#!/usr/bin/env python

import os
from distutils.command.upload import upload as upload_orig
from setuptools import find_packages, setup
from typing import List

VERSION = "0.1.2"


def generate_install_requires() -> List[str]:
    # Path agnostic way to open requirements
    abspath = os.path.abspath(__file__)
    project_root = os.path.dirname(abspath)
    req_path = os.path.join(project_root, "requirements.txt")

    with open(req_path) as f:
        required = f.read().splitlines()

    # Remove comments
    return list(filter(lambda x: not x.startswith("#"), required))


setup(
    name="mkdocs-git-snippet",
    version=VERSION,
    description="An MkDocs plugin that reads snippets from Github Repositories.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mercari",
    url="https://github.com/mercari/mkdocs-git-snippet",
    python_requires=">=3.5",
    install_requires=generate_install_requires(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    entry_points={
        "mkdocs.plugins": ["git-snippet = mkdocs_git_snippet.plugin:GitSnippetPlugin"]
    },
)

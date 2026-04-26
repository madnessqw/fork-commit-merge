#!/usr/bin/env python3
"""Setup script for GitHub Bounty Hunter CLI"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github-bounty-hunter",
    version="1.0.0",
    author="UniverseCreator",
    author_email="",
    description="A CLI tool to discover, track, and manage GitHub bounty opportunities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UniverseCreator/bounty-hunter-cli",
    py_modules=["bounty_hunter"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "bounty-hunter=bounty_hunter:main",
        ],
    },
)
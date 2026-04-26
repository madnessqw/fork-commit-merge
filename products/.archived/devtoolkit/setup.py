from setuptools import setup, find_packages

setup(
    name="devtoolkit",
    version="1.0.0",
    author="UniverseCreator",
    author_email="",
    description="A collection of practical Python automation scripts for developers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/universe7creator/devtoolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "file-organizer=devtoolkit.file_organizer:main",
            "duplicate-finder=devtoolkit.duplicate_finder:main",
        ],
    },
)

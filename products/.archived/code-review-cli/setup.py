from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-review-cli",
    version="1.0.0",
    author="UniverseCreator",
    author_email="",
    description="Automated code quality analysis for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UniverseCreator/code-review-cli",
    py_modules=["code_review"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
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
            "code-review=code_review:main",
        ],
    },
)

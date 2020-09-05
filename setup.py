import os
from setuptools import setup, find_packages


def read(file_name: str):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="gendiff",
    version="1.0.0",
    python_requires=">=3.8.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click==7.1.2",
        "PyYAML==5.3.1"
    ],
    extras_require={
        "Linter": ["flake8==3.8.3"],
        "Test": ["pytest==6.0.1"],
        "Isort": ["isort==5.4.2"],
        "Mypy": ["mypy==0.782"]
    },
    entry_points={
        "console_scripts": [
            "gendiff = gendiff.main:cli"
        ]
    },
    download_url="https://github.com/aeroshev/gendiff.git",
    author="Artem",
    author_email="aeroshev@htsts.ru",
    description="This program compare two files and show changes",
    long_description=read("README.md")
)

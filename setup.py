import os
from setuptools import setup, find_packages


def read(file_name: str):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='gendiff',
    version='1.0.0',
    python_requires='>=3.8.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click==7.1.2',
        'PyYAML==5.3.1',
        'Colorama==0.4.3'
    ],
    entry_points={
        'console_scripts': [
            'gendiff = gendiff.main:cli'
        ]
    },
    download_url='https://github.com/aeroshev/gendiff.git',
    author='Artem',
    author_email='aeroshev@hsts.ru',
    description='This program compare two files and show changes',
    long_description=read('README.md')
)



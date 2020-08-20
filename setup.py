from setuptools import setup, find_packages


setup(
    name='gendiff',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'gendiff = gendiff.main:cli'
        ]
    },
    author='Artem',
    author_email='aeroshev@hsts.ru',
    description='This program compare two files and show changes'
)



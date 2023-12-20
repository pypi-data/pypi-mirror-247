from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    desc = f.read()

setup(
    name='readabform',
    version='0.1',
    long_description=desc,
    long_description_content_type='text/markdown',
    requires=[
        'bestErrors',
    ],
    author='Torrez'
)
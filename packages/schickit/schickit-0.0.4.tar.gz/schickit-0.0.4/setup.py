from setuptools import setup, find_packages

setup(
    name="schickit",
    version="0.0.4",
    description="a toolkit for processing single cell Hi-C data",
    author="ABC",
    packages=find_packages(),
    entry_points={
        'schickit': [
            'run = schickit.run:main',
            'index = schickit.index:main',
        ]}
)
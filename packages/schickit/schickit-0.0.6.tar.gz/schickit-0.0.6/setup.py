from setuptools import setup, find_packages

setup(
    name="schickit",
    version="0.0.6",
    description="a toolkit for processing single cell Hi-C data",
    author="ABC",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'schickit run = schickit.run:main',
            'schickit index = schickit.index:main',
        ]}
)
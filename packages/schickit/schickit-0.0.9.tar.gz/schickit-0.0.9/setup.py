from setuptools import setup, find_packages

setup(
    name="schickit",
    version="0.0.9",
    description="a toolkit for processing single cell Hi-C data",
    author="ABC",
    packages=['src', 'src.utils'],
    entry_points={
        'console_scripts': [
            'schickit = src.main:main',
        ]}
)
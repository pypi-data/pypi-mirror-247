from setuptools import setup, find_packages

setup(
    name="schickit",
    version="0.0.10",
    description="a toolkit for processing single cell Hi-C data",
    author="ABC",
    packages=['schickit', 'schickit.utils'],
    entry_points={
        'console_scripts': [
            'schickit = schickit.main:main',
        ]}
)
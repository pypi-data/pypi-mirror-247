from setuptools import setup, find_packages

setup(
    name='py-jutil',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[],
    author='Noah Wilhoite',
    author_email='notnoah349@gmail.com',
    description='JUtil is a collection of useful functions, values, and classes for Python.',
    long_description="""
# JUtil

## Description:
JUtil is a collection of useful functions, values, and classes for Python.

## Dependencies:
- None yet

## Note:
- This module is a work in progress.

## Recent Changes:
- Added `jutil.styling`, for styling text in the console.
- Added `jutil.inp`, for quick and easy input functions.
- Added `jutil.logs`, for quick and easy logging functions.


___
v0.0.3, developed by Noah Wilhoite
Last updated: Dec 21th, 2023
"""
,
    long_description_content_type='text/markdown',
)
from setuptools import setup, find_packages

setup(
    name='py_mrm',
    version='1.2.0',
    author='E.A.J.F. Peters',
    author_email='e.a.j.f.peters@tue.nl',
    description='Functions for multiphase reactor modeling',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
)

from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

setup(
    name = 'verysimplemodule_liedson',
    version = VERSION,
    author = 'liedson',
    author_email = 'fabricoliedson@gamil.com',
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_require = '',

    keywords = ['python', 'math'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ]
 
)
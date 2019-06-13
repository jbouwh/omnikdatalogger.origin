import os
import re
from setuptools import setup, find_packages

def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    path = os.path.join(os.path.dirname(__file__), package, '__init__.py')
    with open(path, 'rb') as f:
        init_py = f.read().decode('utf-8')
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="omnik-data-logger",
    packages = ['omnik-data-logger'],
    version=get_version('omnik'),
    license="gpl-3.0",
    author="Pascal Prins",
    author_email="pascal.prins@foobar-it.com",
    description="Omnik Data Logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paprins/omnik-data-logger",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Home Automation',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
        "Operating System :: OS Independent",
    ],
    install_requires = required,
    scripts=['bin/omnik-logger'],
)
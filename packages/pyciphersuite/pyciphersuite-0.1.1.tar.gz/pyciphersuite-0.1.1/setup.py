from setuptools import setup

from pyciphersuite import __version__
from pyciphersuite import __license__
from pyciphersuite import __author__

with open("README.md", "r") as f:
    long_description = f.read()

install_requires = [
    "requests"
]

setup(
    name="pyciphersuite",
    version=__version__,
    license=__license__,
    author=__author__,
    description="Python API wrapper for ciphersuiteinfo",
    packages=["pyciphersuite"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jxdv/pyciphersuite",
    keywords=["python3", "api", "rest api", "ciphersuite"],
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

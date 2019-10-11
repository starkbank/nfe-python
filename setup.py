from os import path
from setuptools import setup, find_packages


with open(path.join(path.dirname(__file__), "README.md")) as readme:
    README = readme.read()


setup(
    name="starkbank-nfe",
    packages=find_packages(),
    include_package_data=True,
    description="Python xml signer and webservice requester",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/starkbank/nfe",
    author="Stark Bank",
    author_email="developers@starkbank.com",
    keywords=["nfe", "nfse", "xml", "xml signer", "stark bank", "starkbank"],
    version="0.1.0",
)

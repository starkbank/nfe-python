import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name="nfse-library",
        version="1.0",
        scripts=['nfe-library'],
        author="Vitor Sgobbi",
        author_email="vitor.gabriel@starkbank.com",
        description="Python xml signer and webservice requester",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/vsgobbi/nfe-library",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )

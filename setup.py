import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name='nfse-python',
        version='0.1',
        scripts=[''],
        author="Vitor Sgobbi",
        author_email="vitor.gabriel@starkbank.com",
        description="Python xml signer and webservice requester",
        long_description=long_description,
        long_description_content_type="text/xml",
        url="https://github.com/vsgobbi/nfse-python",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 27",
            "License :: OSI Approved :: GPL License",
            "Operating System :: OS Independent",
        ],
    )

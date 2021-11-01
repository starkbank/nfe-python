from os import path
from setuptools import setup, find_packages


with open(path.join(path.dirname(__file__), "README.md")) as readme:
    README = readme.read()


setup(
    name="bnsouza-nfe",
    packages=find_packages(),
    include_package_data=True,
    description="Python xml signer and webservice requester",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/bnsouza/nfe-python",
    author="Stark Bank / Bruno Souza",
    author_email="bruno@komu.com.br",
    keywords=["nfe", "nfse", "xml", "xml signer", "stark bank", "starkbank"],
    install_requires=[
        "lxml==4.4.1",
        "pycryptodome==3.11.0",
        "requests==2.22.0",
        "rsa==4.0",
        "urllib3==1.25.3",
    ],
    version="0.2",
)

### Create a source distribution:

#Run ```python setup.py sdist``` inside the project directory.

### Install twine:

#```pip install twine```

### Upload package to pypi:

#```twine upload dist/*```

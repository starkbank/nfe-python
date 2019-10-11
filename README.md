## Description
Lib created in order to sign XML content for SOAP Envelops when a signature is required. 
This library is intended to be used within WebServices that require certificate signature values inside the XML body.
Pure Python coded. Its features consist in extracting .CERT or .PEM files and PrivateKeys to add values 
on Signatures elements as ***SignatureValue*** and ***X509Certificate*** with ***rsa-sha1*** encryption type,
compliant with http://www.w3.org/2000/09/xmldsig. 
Sign a XML file or buffered string using A1 or A3 certificate, PKCS1_v1_5 supported by RFC3447. 
It serializes the data to request SOAP RPC services. Creates POST requests on WebServices as NFe and NFSe.

## Table of Contents


- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)




<!-- [![FVCproductions](https://avatars1.githubusercontent.com/u/4284691?v=3&s=200)](http://fvcproductions.com) -->
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)
[![Coverage Status](http://img.shields.io/coveralls/badges/badgerbadgerbadger.svg?style=flat-square)](https://coveralls.io/r/badges/badgerbadgerbadger) 
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)

---


## Installation

### Pip install 
- Firstly, install library with pip:

```shell
pip install starkbank-nfe
```
---
- Or clone this repo and install library:

```shell   
git clone https://github.com/starkbank/nfe
python setup.py install
``` 

## Features
> Using the following libs: 
- lxml, pyCrypto, requests, ssl, rsa


---
## Usage

### Using this lib:
##### We can create a new Rps, Consult Nfes and Cancel Nfes
```python
# coding: utf-8
from gateways.saopaulo import SaopauloGateway

certificateContent=open("../static/certificate.crt", "rb").read()
privateKeyContent = open("./static/rsaKey.pem").read()

###Create Nfe:

nota = {
    "senderTaxId": "01234567890123",
    "subscription": "01234567",
    "rpsSeries": "TESTE",
    "rpsNumber": "9117092019",
    "rpsType": "RPS",
    "issueDate": "2019-07-09",
    "statusRps": "N",
    "rpsTax": "T",
    "issRetain": "false",
    "serviceAmount": "1",
    "deductionAmount": "0",
    "pisAmount": "0",
    "irAmount": "0",
    "csllAmount": "0",
    "cofinsAmount": "0",
    "inssAmount": "0",
    "serviceCode": "05895",
    "aliquot": "2",
    "receiverTaxId": "32109876543210",
    "receiverName": "SOME COMPANY NAME",
    "receiverStreetLine1": "Null",
    "receiverStreetNumber": "123",
    "receiverStreetLine2": "Null",
    "receiverDistrict": "Null",
    "receiverCity": "3550308",
    "receiverState": "SP",
    "receiverZipCode": "00000000",
    "receiverEmail": "none@none",
    "description": "Teste de emissao de NFS-e de boletos prestados",
}

print(SaopauloGateway.sendRps(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **nota
    ))

###How to delete a Nfe:

nota = {
    "senderTaxId": "01234567890123",
    "subscription": "01234567",
    "nfeNumber": "001"
}

print(SaopauloGateway.cancelRps(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **nota
    ))

###Consult sent Nfes

parameters = {
    "senderTaxId": "01234567890123",
    "subscription": "01234567",
    "dtInicio": "2019-09-15",
    "dtFim": "2019-09-18",
}

print(SaopauloGateway.consultNfes(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **parameters
))

```

---

## Contributing

#### Get started

- **Step 1**
    - 🍴 Fork this repo!

- **Step 2**
    - 🔨🔨 Clone this repo to your local machine using `https://github.com/starkbank/nfe`

- **Step 3**
    - 🔃 Create a new pull request using <a href="https://github.com/starkbank/nfe/compare/" target="_blank">`https://github.com/starkbank/nfe/compare/`</a>

---

## Support

Reach out to me at one of the following places!

- E-mail at <a href="mailto:" target="_blank">`developers@starkbank.com`</a>
- Github at <a href="https://www.github.com/starkbank" target="_blank">`@starkbank`</a>

---

## License

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
- Copyright 2019 © <a href="https://github.com/starkbank" target="_blank">STARK BANK S.A.</a>

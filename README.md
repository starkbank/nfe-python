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



<a href="https://gnu.org"><img src="https://www.gnu.org/graphics/gplv3-127x51.png" title="FVCproductions" alt="GPL"></a>

<!-- [![FVCproductions](https://avatars1.githubusercontent.com/u/4284691?v=3&s=200)](http://fvcproductions.com) -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)
[![Coverage Status](http://img.shields.io/coveralls/badges/badgerbadgerbadger.svg?style=flat-square)](https://coveralls.io/r/badges/badgerbadgerbadger) 

---


## Installation

### Clone

### CLONE PROJECT
- Firstly, clone this repo to your local machine

```shell
git clone https://github.com/starkbank/nfe.git
```
---
### INSTALL PACKAGE
```shell     
python setup.py install
``` 

### INSTALL REQUIRED LIBS

- Install main libs
```shell     
pip install -r requirements.txt
``` 

## Features
> Using the following libs: 
- lxml, pyCrypto, requests, ssl, rsa

---


## Setup

### CREATE VENV

- Create virtualenv using Python2.7
```shell     
virtualenv -p python2.7 venv
```
- Activate the virtualenv
```shell     
source venv/bin/activate
```
- Verify if version is correct
```shell     
python --version #expected return: Python2.7
pip --version
```

---
## Usage

### Using this lib:
##### We can create a new RPS, Consult Nfes and Cancel Nfes
```python
# coding: utf-8
from gateways.saopaulo import SaopauloGateway

certificateContent=open("../static/certificate.crt", "rb").read()
privateKeyContent = open("./static/rsaKey.pem").read()

###Create Nfe:

nfe = {
    "senderTaxId": "63841121000180",
    "inscricaoPrestador":  "98412100",
    "serieRps": "TESTE",
    "numeroRps": "9117092019",
    "tipoRps": "RPS",
    "dataEmissao": "2019-07-09",
    "statusRps": "N",
    "tributacaoRps": "T",
    "issRetido": "false",
    "valorServicos": "1",
    "valorDeducoes": "0",
    "valorPis": "0",
    "valorIr": "0",
    "valorCsll": "0",
    "valorCofins": "0",
    "valorInss": "0",
    "codigoServico": "05895",
    "aliquotaServicos": "2",
    "receiverTaxId": "30134945000167",
    "receiverName": "HUMMINGBIRD HEALTH PRODUCTS",
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
    **nfe
    ))

###How to delete a Nfe:

nota = {
    "senderTaxId": "20018183000180",
    "inscricaoPrestador": "57038597",
    "nfeNumber": "296"
}

print(SaopauloGateway.cancelRps(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **nota
    ))

###Consult sent Nfes

parameters = {
    "senderTaxId": "20018183000180",
    "inscricaoPrestador": "57038597",
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

- E-mail at <a href="mailto:" target="_blank">`vitor.gabriel@starkbank.com`</a>
- Github at <a href="https://www.github.com/vsgobbi" target="_blank">`@vsgobbi`</a>

---

## License

 [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
- **[GPL license](https://www.gnu.org/licenses/gpl-3.0)**
- Copyright 2019 © <a href="https://github.com/vsgobbi" target="_blank">Vitor Gabriel Sgobbi</a>.

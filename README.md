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

certificateContent = open("./certificate.crt", "rb").read()
privateKeyContent = open("./rsaKey.pem").read()

###Create Nfe:

nota = {
    "CPFCNPJRemetente": "01234567890987",
    "InscricaoPrestador":  "01234567",
    "SerieRPS": "TESTE",
    "NumeroRPS": "9117092019",
    "TipoRPS": "RPS",
    "DataEmissao": "2019-07-09",
    "StatusRPS": "N",
    "TributacaoRPS": "T",
    "ValorServicos": "1",
    "ValorDeducoes": "0",
    "ValorPIS": "0",
    "ValorIR": "0",
    "ValorCSLL": "0",
    "ValorCOFINS": "0",
    "ValorINSS": "0",
    "CodigoServico": "05895",
    "AliquotaServicos": "2",
    "ISSRetido": "false",
    "CPFCNPJTomador": "01234567654321",
    "RazaoSocialTomador": "SOME COMPANY NAME",
    "Logradouro": "Rua Um",
    "NumeroEndereco": "123",
    "ComplementoEndereco": "Centro",
    "Bairro": "Vila Unica",
    "Cidade": "3550308",
    "UF": "SP",
    "CEP": "00000000",
    "EmailTomador": "none@none.com",
    "Discriminacao": "Teste de emissao de NFS-e de boletos prestados",
}

print(SaopauloGateway.sendRps(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **nota
))

###How to delete a Nfe:

nota = {
    "CPFCNPJRemetente": "01234567890123",
    "InscricaoPrestador": "01234567",
    "NumeroNFe": "001"
}

print(SaopauloGateway.cancelRps(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **nota
))

###Consult sent Nfes

parameters = {
    "CPFCNPJRemetente": "01234567890123",
    "InscricaoPrestador": "01234567",
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

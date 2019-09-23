## Description
Lib created in order to sign XML content for SOAP Envelops when a signed XML is required. 
This library is intended to use with WebServices that requires certificate signatures values amongst the xml body.
Pure Python coded. It's features are extracting .CERT or .PEM files and PrivateKeys to add values 
on Signatures elements as ***SignatureValue*** and ***X509Certificate*** with ***rsa-sha1*** encryption type,
compliance with http://www.w3.org/2000/09/xmldsig. 
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

### Using this lib to sign a xml file:

#### How to extract certificate files:
```python
from xmlsigner.signerXml import SignCert

certificateFile = "./certfiles/converted.crt"
privateKeyRSA = "./certfiles/privRSAkey.pem"
privateKeyFile = "./certfiles/RSAPrivateKey.pem"

objSignCert = SignCert(
    privateKeyContent=open(privateKeyRSA).read(),
    certificateContent=open(certificateFile).read(),
    rsaKeyContent=open(privateKeyRSA).read()
)

objSignCert.loadPem()
certContent = objSignCert.loadCert()
print(certContent)
keyContent = objSignCert.loadPem()
print(keyContent)
```

#### How to sign a new xml:
```python
xmlEnvelope = "file.xml"
with open(xmlEnvelope, 'rb') as xmlEnvelope:
    xmlData = xmlEnvelope.read()

# Simply sign with extended A1 certificate
xmlEnvelope = etree.fromstring(xmlData)
signedRoot = objSignCert.signA1Cert(xmlEnvelope)
print signedRoot
```


#### How to verify the signed xml file
```python
objSignCert.verifySignature(signedRoot)
```

#### How to perform POST method using a signed xml:
```python
# Sign and post a xml example:
objServ = Services(
    privateKeyContent=open(privateKeyRSA).read(),
    certificateContent=open(certificateFile).read(),
    rsaKeyContent=open(privateKeyRSA).read()
)
taxId = "12345678000198"
taxPayerId = "12345678000198"
result = objServ.consultTaxIdSubscription(taxId=taxId, taxPayerId=taxPayerId)
print(result)
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

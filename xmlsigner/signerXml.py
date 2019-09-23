# -*- coding: utf-8 -*-
from xmlsigner.certMethods import Certificate


class SignCert:

    def __init__(self, privateKeyContent, certificateContent, rsaKeyContent):
        self.privateKeyContent = privateKeyContent
        self.certificateContent = certificateContent
        self.rsaKeyContent = rsaKeyContent

    def loadCert(self):
        return Certificate.extractCertContent(self.certificateContent)

    def loadPem(self):
        return Certificate.valdidatePrivateKey(self.rsaKeyContent)

    def signWithA1Cert(self, bufferXml):
        return Certificate.signWithA1Cert(
            xml=bufferXml,
            certContent=self.certificateContent,
            rsaKeyContent=self.rsaKeyContent
        )

    def signRps(self, bufferXml):
        return Certificate.signRpsWithRsa(
            bufferXml=bufferXml,
            certContent=self.certificateContent,
            rsaKeyContent=self.rsaKeyContent
        )

    def signCancel(self, bufferXml):
        return Certificate.signCancelWithRsa(
            bufferXml=bufferXml,
            certContent=self.certificateContent,
            rsaKeyContent=self.rsaKeyContent
        )

    def signLoteRps(self, stringXml):
        return Certificate.signLoteRps(
            stringXml=stringXml,
            certContent=self.certificateContent,
            rsaKeyContent=self.rsaKeyContent
        )

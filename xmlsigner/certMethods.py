# -*- coding: utf-8 -*-
from Integer import b64e
from lxml import etree
from xmlsigner import xmlDigSign as signer
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


class Certificate(object):

    @classmethod
    def valdidatePrivateKey(cls, privateKeyContent):
        try:
            if "-----BEGIN RSA PRIVATE KEY-----" in privateKeyContent:
                if "-----END RSA PRIVATE KEY-----" in privateKeyContent:
                    key = RSA.importKey(privateKeyContent)
                    return key.keydata
        except Exception as e:
            return "Invalid RSA Private Key {:s}".format(e)

    @classmethod
    def extractCertContent(cls, certContent):
        certBuffer = certContent.replace("\n", "")
        certData = certBuffer.split("-----BEGIN CERTIFICATE-----")
        certBuffer = str((certData[1].replace("-----END CERTIFICATE-----", "")))
        return certBuffer

    @classmethod
    def signWithA1Cert(cls, xml, certContent, rsaKeyContent, returnString=True):
        certContent = cls.extractCertContent(certContent)

        xml = etree.tostring(xml, encoding="utf-8")
        signedXml = signer.sign(xml=xml, certContent=certContent, rsaKeyContent=rsaKeyContent)

        if returnString:
            return signedXml
        else:
            signedXml = etree.fromstring(signedXml)
            return signedXml

    @classmethod
    def verifySignature(cls, rsaPrivateKeyContent, digest, sign):
        try:

            verifier = PKCS1_v1_5.new(rsaPrivateKeyContent.publickey())
            verified = verifier.verify(digest, sign)
            assert verified
        except Exception as e:
            raise e

    @classmethod
    def signRpsWithRsa(cls, bufferXml, rsaKeyContent, certContent):
        ns = {}

        signInscricaoPrestador = bufferXml.find('.//InscricaoPrestador', namespaces=ns).text
        signSerieRPS = bufferXml.find('.//SerieRPS', namespaces=ns).text
        signNumeroRPS = bufferXml.find('.//NumeroRPS', namespaces=ns).text
        signDataEmissao = bufferXml.find('.//DataEmissao', namespaces=ns).text
        signStatusRPS = bufferXml.find('.//StatusRPS', namespaces=ns).text
        signValorServicos = bufferXml.find('.//ValorServicos', namespaces=ns).text
        signValorDeducoes = bufferXml.find('.//ValorDeducoes', namespaces=ns).text
        signCodigoServico = bufferXml.find('.//CodigoServico', namespaces=ns).text
        signISSRetido = bufferXml.find('.//ISSRetido', namespaces=ns).text
        signCPFCNPJTomador = bufferXml.find('.//CPFCNPJTomador/CNPJ', namespaces=ns).text

        if signISSRetido == "false":
            signISSRetido = "N"
        else:
            signISSRetido = "S"
        stringConcat = '%s%s%s%sT%s%s%015d%015d%05d%s%s' % (
            str(signInscricaoPrestador).zfill(8),
            str(signSerieRPS.ljust(5)).upper(),
            str(signNumeroRPS).zfill(12),
            str(signDataEmissao.replace("-", "")),
            str(signStatusRPS),
            str(signISSRetido),
            int(float(signValorServicos) * 100),
            int(float(signValorDeducoes) * 100),
            int(signCodigoServico),
            str(2),
            str(signCPFCNPJTomador).zfill(14))

        digest = SHA.new(stringConcat)
        rsaKey = RSA.importKey(rsaKeyContent)
        signer = PKCS1_v1_5.new(rsaKey)
        sign = signer.sign(digest)
        b64Signed = b64e(sign)

        cls.verifySignature(rsaKey, digest, sign)

        bufferXml.find(".//Assinatura", namespaces=ns).text = b64Signed
        return cls.signWithA1Cert(bufferXml, certContent=certContent, rsaKeyContent=rsaKeyContent)

    @classmethod
    def signCancelWithRsa(cls, bufferXml, rsaKeyContent, certContent):
        ns = {}

        signInscricaoPrestador = bufferXml.find('.//InscricaoPrestador', namespaces=ns).text
        signNumeroNFe = bufferXml.find('.//NumeroNFe', namespaces=ns).text
        stringConcat = signInscricaoPrestador + signNumeroNFe.zfill(12)

        digest = SHA.new(stringConcat)

        rsaKey = RSA.importKey(rsaKeyContent)
        signer = PKCS1_v1_5.new(rsaKey)
        sign = signer.sign(digest)
        b64Signed = b64e(sign)

        cls.verifySignature(rsaKey, digest, sign)

        tagCancelSignatureX509Data = bufferXml.find('.//Detalhe', namespaces=ns)
        etree.SubElement(tagCancelSignatureX509Data, 'AssinaturaCancelamento').text = b64Signed
        return cls.signWithA1Cert(bufferXml, certContent=certContent, rsaKeyContent=rsaKeyContent)

    @classmethod
    def signLoteRps(cls, stringXml, certContent, rsaKeyContent):
        ns = {}

        bufferXml = etree.fromstring(stringXml)
        signInscricaoPrestador = bufferXml.find('.//InscricaoPrestador', namespaces=ns).text
        signSerieRPS = bufferXml.find('.//SerieRPS', namespaces=ns).text
        signNumeroRPS = bufferXml.find('.//NumeroRPS', namespaces=ns).text
        signDataEmissao = bufferXml.find('.//DataEmissao', namespaces=ns).text
        signStatusRPS = bufferXml.find('.//StatusRPS', namespaces=ns).text
        signTributacaoRPS = bufferXml.find('.//TributacaoRPS', namespaces=ns).text
        signValorServicos = bufferXml.find('.//ValorServicos', namespaces=ns).text
        signValorDeducoes = bufferXml.find('.//ValorDeducoes', namespaces=ns).text
        signCodigoServico = bufferXml.find('.//CodigoServico', namespaces=ns).text
        signISSRetido = bufferXml.find('.//ISSRetido', namespaces=ns).text
        signCPFCNPJTomador = bufferXml.find('.//CPFCNPJTomador/CNPJ', namespaces=ns).text

        if "false" in signISSRetido:
            signISSRetido = "N"
        else:
            signISSRetido = "S"
        signNumeroRPS = signNumeroRPS.rjust(12, "0")
        signDataEmissao = signDataEmissao.replace("-", "")
        signValorServicos = signValorServicos.replace("R$", "")
        signValorServicos = signValorServicos.rjust(15, "0")
        signValorDeducoes = signValorDeducoes.replace("R$", "")
        signValorDeducoes = signValorDeducoes.rjust(15, "0")
        signCodigoServico + signCodigoServico.rjust(5, "0")

        signCPFCNPJIntermediario = bufferXml.find(".//CPFCNPJIntermediario", namespaces=ns).text

        if signCPFCNPJIntermediario != None:
            signISSRetidoIntermediario = bufferXml.find(".//ISSRetidoIntermediario", namespaces=ns).text
            signInscricaoMunicipalIntermediario = bufferXml.find(".//InscricaoMunicipalIntermediario", namespaces=ns).text
            if "false" in signISSRetidoIntermediario:
                stringConcat = str(signInscricaoPrestador + signSerieRPS + " " + signNumeroRPS + signDataEmissao
                                   + signTributacaoRPS + signStatusRPS + signValorServicos + signValorDeducoes + "0"
                                   + signCodigoServico + signISSRetido + signCPFCNPJTomador)
            else:
                signISSRetidoIntermediario = "S"
                signCPFCNPJIntermediario = "2" + signCPFCNPJIntermediario
                stringConcat = str(signInscricaoPrestador + signSerieRPS + " " + signNumeroRPS + signDataEmissao
                                   + signTributacaoRPS + signStatusRPS + signValorServicos + signValorDeducoes + "0"
                                   + signCodigoServico + signISSRetido + signCPFCNPJTomador + signCPFCNPJIntermediario
                                   + signInscricaoMunicipalIntermediario + signISSRetidoIntermediario)

        message = str(stringConcat).encode("ascii")

        digest = SHA.new(message)

        RSAKey = RSA.importKey(rsaKeyContent)
        signer = PKCS1_v1_5.new(RSAKey)
        sign = signer.sign(digest)
        b64Signed = b64e(sign)

        cls.verifySignature(rsaKeyContent, digest, sign)

        ns = {}
        bufferXml = etree.fromstring(stringXml)
        bufferXml.find(".//Assinatura", namespaces=ns).text = b64Signed

        return cls.signWithA1Cert(bufferXml, certContent=certContent, rsaKeyContent=rsaKeyContent)

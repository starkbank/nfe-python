from re import search, sub
from .rsa import Rsa
from .currency import Currency
from .certificate import Certificate


class Rps:

    @classmethod
    def xmlCreateRps(cls, xml, inscricaoPrestador, serieRps, numeroRps, dataEmissao, statusRps, valorServicos,
         valorDeducoes, codigoServico, issRetido, receiverTaxId, senderTaxId, tipoRps, tributacaoRps, valorPis,
         valorCofins, valorInss, valorIr, valorCsll, aliquotaServicos, receiverName, receiverStreetLine1,
         receiverStreetNumber, receiverStreetLine2, receiverDistrict, receiverCity, receiverState,
         receiverZipCode, receiverEmail, description, privateKeyContent, certificateContent):

        rpsToSign = "{inscricaoPrestador}{serieRps}{numeroRps}{dataEmissao}T{statusRps}" \
                    "{issRetido}{valorServicos}{valorDeducoes}{codigoServico}2{receiverTaxId}".format(
            inscricaoPrestador=inscricaoPrestador.zfill(8),
            serieRps=serieRps.ljust(5).upper(),
            numeroRps=numeroRps.zfill(12),
            dataEmissao=dataEmissao.replace("-", ""),
            statusRps=statusRps,
            issRetido={"false": "N", "true": "S"}.get(issRetido),
            valorServicos=str(valorServicos).zfill(15),
            valorDeducoes=str(valorDeducoes).zfill(15),
            codigoServico=codigoServico.zfill(5),
            receiverTaxId=receiverTaxId.zfill(14),
        )

        rpsSignature = Rsa.sign(text=rpsToSign, privateKeyContent=privateKeyContent)

        parameters = {
            "rpsSignature": rpsSignature,
            "inscricaoPrestador": inscricaoPrestador,
            "serieRps": serieRps,
            "tipoRps": tipoRps,
            "tributacaoRps": tributacaoRps,
            "valorPis": Currency.formatted(valorPis),
            "valorCofins": Currency.formatted(valorCofins),
            "valorInss": Currency.formatted(valorInss),
            "valorIr": Currency.formatted(valorIr),
            "valorCsll": Currency.formatted(valorCsll),
            "valorServicos": Currency.formatted(valorServicos),
            "valorDeducoes": Currency.formatted(valorDeducoes),
            "aliquotaServicos": Currency.formatted(aliquotaServicos),
            "numeroRps": numeroRps,
            "dataEmissao": dataEmissao,
            "statusRps": statusRps,
            "codigoServico": codigoServico,
            "issRetido": issRetido,
            "senderTaxId": senderTaxId,
            "receiverTaxId": receiverTaxId,
            "receiverName": receiverName,
            "receiverStreetLine1": receiverStreetLine1.decode("utf-8"),
            "receiverStreetNumber": receiverStreetNumber,
            "receiverStreetLine2": receiverStreetLine2.decode("utf-8"),
            "receiverDistrict": receiverDistrict.decode("utf-8"),
            "receiverCity": receiverCity,
            "receiverState": receiverState,
            "receiverZipCode": receiverZipCode,
            "receiverEmail": receiverEmail,
            "description": description.decode("utf-8")
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def cancelRps(cls, xml, senderTaxId, inscricaoPrestador, nfeNumber, certificateContent, privateKeyContent):
        cancelToSign = "{inscricaoPrestador}{nfeNumber}".format(
            inscricaoPrestador=inscricaoPrestador.zfill(8),
            nfeNumber=nfeNumber.zfill(12)
        )

        cancelSignature = Rsa.sign(text=cancelToSign, privateKeyContent=privateKeyContent)

        parameters = {
            "senderTaxId": senderTaxId,
            "inscricaoPrestador": inscricaoPrestador,
            "nfeNumber": nfeNumber,
            "cancelSignature": cancelSignature,
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def consultNfes(cls, xml, senderTaxId, inscricaoPrestador, dtInicio, dtFim, certificateContent, privateKeyContent):
        parameters = {
            "senderTaxId": senderTaxId,
            "inscricaoPrestador": inscricaoPrestador,
            "dtInicio": dtInicio,
            "dtFim": dtFim,
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def signXml(cls, xml, privateKeyContent, certificateContent, **kwargs):
        xmlWithoutBreakLine = sub("\n*", "", xml)
        xmlWithoutSpaces = sub("\s{2,}", "", xmlWithoutBreakLine)

        p1WithSignature = search("<!\[CDATA\[(.*)\]\]>", xmlWithoutSpaces).group(1)
        p1WithoutSignature = sub("<Signature .*</Signature>", "", p1WithSignature)

        p1 = p1WithoutSignature.format(**kwargs)

        digestValue = Rsa.digest(p1)
        namespace = search("<[^> ]+ ?([^>]*)>", p1WithoutSignature).group(1)
        signInfo = search("(<SignedInfo>.*</SignedInfo>)", xmlWithoutSpaces).group(1)
        signInfoWithNamespace = sub("<SignedInfo>", "<SignedInfo xmlns=\"http://www.w3.org/2000/09/xmldsig#\" {namespace}>".format(namespace=namespace), signInfo)
        message = signInfoWithNamespace.format(digestValue=digestValue)
        signatureValue = Rsa.sign(text=message, privateKeyContent=privateKeyContent)

        sigendXml = xmlWithoutSpaces.format(
            digestValue=digestValue,
            signatureValue=signatureValue,
            certificate=Certificate.getContent(certificateContent),
            **kwargs
        )

        return sigendXml

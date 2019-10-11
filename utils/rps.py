from re import search, sub
from .rsa import Rsa
from .currency import Currency
from .certificate import Certificate


class Rps:

    @classmethod
    def xmlCreateRps(cls, xml, subscription, rpsSeries, rpsNumber, issueDate, statusRps, serviceAmount,
                     deductionAmount, serviceCode, issRetain, receiverTaxId, senderTaxId, rpsType, rpsTax, pisAmount,
                     cofinsAmount, inssAmount, irAmount, csllAmount, aliquot, receiverName, receiverStreetLine1,
                     receiverStreetNumber, receiverStreetLine2, receiverDistrict, receiverCity, receiverState,
                     receiverZipCode, receiverEmail, description, privateKeyContent, certificateContent):

        rpsToSign = "{InscricaoPrestador}{SerieRPS}{NumeroRPS}{DataEmissao}T{StatusRPS}" \
                    "{ISSRetido}{ValorServicos}{ValorDeducoes}{CodigoServico}2{RazaoSocialTomador}".format(
            InscricaoPrestador=subscription.zfill(8),
            SerieRPS=rpsSeries.ljust(5).upper(),
            NumeroRPS=rpsNumber.zfill(12),
            DataEmissao=issueDate.replace("-", ""),
            StatusRPS=statusRps,
            ISSRetido={"false": "N", "true": "S"}.get(issRetain),
            ValorServicos=str(serviceAmount).zfill(15),
            ValorDeducoes=str(deductionAmount).zfill(15),
            CodigoServico=serviceCode.zfill(5),
            RazaoSocialTomador=receiverTaxId.zfill(14),
        )

        rpsSignature = Rsa.sign(text=rpsToSign, privateKeyContent=privateKeyContent)

        parameters = {
            "CPFCNPJRemetente": senderTaxId,
            "Assinatura": rpsSignature,
            "InscricaoPrestador": subscription,
            "SerieRPS": rpsSeries,
            "NumeroRPS": rpsNumber,
            "TipoRPS": rpsType,
            "DataEmissao": issueDate,
            "StatusRPS": statusRps,
            "TributacaoRPS": rpsTax,
            "ValorServicos": Currency.formatted(serviceAmount),
            "ValorDeducoes": Currency.formatted(deductionAmount),
            "ValorPIS": Currency.formatted(pisAmount),
            "ValorCOFINS": Currency.formatted(cofinsAmount),
            "ValorINSS": Currency.formatted(inssAmount),
            "ValorIR": Currency.formatted(irAmount),
            "ValorCSLL": Currency.formatted(csllAmount),
            "CodigoServico": serviceCode,
            "AliquotaServicos": Currency.formatted(aliquot),
            "ISSRetido": issRetain,
            "CPFCNPJTomador": receiverTaxId,
            "RazaoSocialTomador": receiverName,
            "Logradouro": receiverStreetLine1.decode("utf-8"),
            "NumeroEndereco": receiverStreetNumber,
            "ComplementoEndereco": receiverStreetLine2.decode("utf-8"),
            "Bairro": receiverDistrict.decode("utf-8"),
            "Cidade": receiverCity,
            "UF": receiverState,
            "CEP": receiverZipCode,
            "EmailTomador": receiverEmail,
            "Discriminacao": description.decode("utf-8")
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def cancelRps(cls, xml, senderTaxId, subscription, nfeNumber, certificateContent, privateKeyContent):
        cancelToSign = "{InscricaoPrestador}{NumeroNFe}".format(
            InscricaoPrestador=subscription.zfill(8),
            NumeroNFe=nfeNumber.zfill(12)
        )
        print(cancelToSign)
        cancelSignature = Rsa.sign(text=cancelToSign, privateKeyContent=privateKeyContent)

        parameters = {
            "CPFCNPJRemetente": senderTaxId,
            "InscricaoPrestador": subscription,
            "NumeroNFe": nfeNumber,
            "AssinaturaCancelamento": cancelSignature,
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def consultNfes(cls, xml, senderTaxId, subscription, dtInicio, dtFim, certificateContent, privateKeyContent):
        parameters = {
            "CPFCNPJRemetente": senderTaxId,
            "Inscricao": subscription,
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
        message = signInfoWithNamespace.format(DigestValue=digestValue)
        signatureValue = Rsa.sign(text=message, privateKeyContent=privateKeyContent)

        sigendXml = xmlWithoutSpaces.format(
            DigestValue=digestValue,
            SignatureValue=signatureValue,
            X509Certificate=Certificate.getContent(certificateContent),
            **kwargs
        )

        return sigendXml

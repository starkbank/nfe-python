from re import search, sub
from .rsa import Rsa
from .currency import Currency
from .certificate import Certificate
from ..utils.compatibility import stringDecode


class Rps:

    @classmethod
    def xmlCreateRps(cls, xml, InscricaoPrestador, SerieRPS, NumeroRPS, TipoRPS, DataEmissao, StatusRPS, ValorServicos,
                     ValorDeducoes, CodigoServico, ISSRetido, CPFCNPJTomador, CPFCNPJRemetente, TributacaoRPS, ValorPIS,
                     ValorCOFINS, ValorINSS, ValorIR, ValorCSLL, AliquotaServicos, RazaoSocialTomador, Logradouro,
                     NumeroEndereco, ComplementoEndereco, Bairro, Cidade, UF, CEP, EmailTomador, Discriminacao,
                     privateKeyContent, certificateContent):

        CPFCNPJTomadorTag = "CPF"
        if len(CPFCNPJTomador) > 11:
            CPFCNPJTomadorTag = "CNPJ"

        rpsToSign = "{InscricaoPrestador}{SerieRPS}{NumeroRPS}{DataEmissao}{TributacaoRPS}{StatusRPS}" \
                    "{ISSRetido}{ValorServicos}{ValorDeducoes}{CodigoServico}{CPFCNPJ}{RazaoSocialTomador}".format(
            InscricaoPrestador=InscricaoPrestador.zfill(8),
            SerieRPS=SerieRPS.ljust(5).upper(),
            NumeroRPS=NumeroRPS.zfill(12),
            DataEmissao=DataEmissao.replace("-", ""),
            TributacaoRPS=TributacaoRPS.upper(),
            StatusRPS=StatusRPS,
            ISSRetido={"false": "N", "true": "S"}.get(ISSRetido),
            ValorServicos=str(ValorServicos).zfill(15),
            ValorDeducoes=str(ValorDeducoes).zfill(15),
            CodigoServico=CodigoServico.zfill(5),
            CPFCNPJ=("1" if CPFCNPJTomadorTag == "CPF" else "2"),
            RazaoSocialTomador=CPFCNPJTomador.zfill(14),
        )

        rpsSignature = Rsa.sign(text=rpsToSign, privateKeyContent=privateKeyContent)

        parameters = {
            "CPFCNPJRemetente": CPFCNPJRemetente,
            "Assinatura": stringDecode(rpsSignature),
            "InscricaoPrestador": InscricaoPrestador,
            "SerieRPS": SerieRPS,
            "NumeroRPS": NumeroRPS,
            "TipoRPS": TipoRPS,
            "DataEmissao": DataEmissao,
            "StatusRPS": StatusRPS,
            "TributacaoRPS": TributacaoRPS,
            "ValorServicos": Currency.formatted(ValorServicos),
            "ValorDeducoes": Currency.formatted(ValorDeducoes),
            "ValorPIS": Currency.formatted(ValorPIS),
            "ValorCOFINS": Currency.formatted(ValorCOFINS),
            "ValorINSS": Currency.formatted(ValorINSS),
            "ValorIR": Currency.formatted(ValorIR),
            "ValorCSLL": Currency.formatted(ValorCSLL),
            "CodigoServico": CodigoServico,
            "AliquotaServicos": Currency.formatted(AliquotaServicos),
            "ISSRetido": ISSRetido,
            "CPFCNPJTomador": CPFCNPJTomador,
            "CPFCNPJTomadorTag": CPFCNPJTomadorTag,
            "RazaoSocialTomador": RazaoSocialTomador,
            "Logradouro": Logradouro,
            "NumeroEndereco": NumeroEndereco,
            "ComplementoEndereco": ComplementoEndereco,
            "Bairro": Bairro,
            "Cidade": Cidade,
            "UF": UF,
            "CEP": CEP,
            "EmailTomador": EmailTomador,
            "Discriminacao": Discriminacao,
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def cancelRps(cls, xml, CPFCNPJRemetente, InscricaoPrestador, NumeroNFe, certificateContent, privateKeyContent):
        cancelToSign = "{InscricaoPrestador}{NumeroNFe}".format(
            InscricaoPrestador=InscricaoPrestador.zfill(8),
            NumeroNFe=NumeroNFe.zfill(12)
        )

        cancelSignature = Rsa.sign(text=cancelToSign, privateKeyContent=privateKeyContent)

        parameters = {
            "CPFCNPJRemetente": CPFCNPJRemetente,
            "InscricaoPrestador": InscricaoPrestador,
            "NumeroNFe": NumeroNFe,
            "AssinaturaCancelamento": stringDecode(cancelSignature),
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def consultNfes(cls, xml, CPFCNPJRemetente, Inscricao, dtInicio, dtFim, certificateContent, privateKeyContent):
        parameters = {
            "CPFCNPJRemetente": CPFCNPJRemetente,
            "Inscricao": Inscricao,
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

        digestValue = stringDecode(Rsa.digest(p1))

        namespace = search("<[^> ]+ ?([^>]*)>", p1WithoutSignature).group(1)
        signInfo = search("(<SignedInfo>.*</SignedInfo>)", xmlWithoutSpaces).group(1)
        signInfoWithNamespace = sub("<SignedInfo>", "<SignedInfo xmlns=\"http://www.w3.org/2000/09/xmldsig#\" {namespace}>".format(namespace=namespace), signInfo)
        message = signInfoWithNamespace.format(DigestValue=digestValue)
        signatureValue = stringDecode(Rsa.sign(text=message, privateKeyContent=privateKeyContent))

        sigendXml = xmlWithoutSpaces.format(
            DigestValue=digestValue,
            SignatureValue=signatureValue,
            X509Certificate=Certificate.getContent(certificateContent),
            **kwargs
        )

        return sigendXml

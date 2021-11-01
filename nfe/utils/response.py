from lxml import etree
from re import search
from .compatibility import xmlFromString, getXmlText


class Response:

    @classmethod
    def resultDict(cls, strResult):
        responseGroup = search("\<RetornoXML>(.*)\</Retorno", strResult).group(1)
        res = {}
        root = xmlFromString(responseGroup)
        for element in root.iter():
            text = getXmlText(element)
            if text:
                res.setdefault("{tag}".format(tag=element.tag), "{text}".format(text=str(text)))
        return res

    @classmethod
    def getTail(cls, strResult):
        responseGroup = search("\<RetornoXML>(.*)\</Retorno", strResult).group(1)
        responseGroup = search("\</Cabecalho>(.*)\</Retorno", responseGroup).group(1)
        try:
            root = "<root>" + responseGroup + "</root>"
            tree = etree.fromstring(root)
            nfeData = []
            res = {}
            for i in tree:
                res.update({
                    "SerieRPS": i.find('.//SerieRPS', namespaces={}).text,
                    "NumeroRPS": i.find('.//NumeroRPS', namespaces={}).text,
                    "DataEmissaoNFe": i.find('.//DataEmissaoNFe', namespaces={}).text,
                    "CPFCNPJTomador": i.find('.//CPFCNPJTomador', namespaces={})[0].text,
                    "CodigoVerificacao": i.find('.//CodigoVerificacao', namespaces={}).text,
                    "NumeroNFe": i.find('.//NumeroNFe', namespaces={}).text
                })
                nfeData.append(res.copy())
            return nfeData
        except Exception as error:
            return error

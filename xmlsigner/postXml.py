import requests
import ssl
import re
import socket
from lxml import etree
from xmlsigner.certMethods import Certificate
from xmlsigner.customHttpConnection import NewAdapter


NAMESPACE_NFE = "http://www.portalfiscal.inf.br/nfe"
NAMESPACE_NFE_PRODAM = "http://www.prefeitura.sp.gov.br/nfe"
NAMESPACE_SOAP = "http://www.w3.org/2003/05/soap-envelope"
NAMESPACE_XSI = "http://www.w3.org/2001/XMLSchema-instance"
NAMESPACE_XSD = "http://www.w3.org/2001/XMLSchema"
NAMESPACE_METODO_SEFAZ = "http://www.portalfiscal.inf.br/nfe/wsdl/"
NAMESPACE_METODO_PRODAM = "http://www.prefeitura.sp.gov.br/nfe"

NFE = {
        'SP': {
        'STATUS': 'nfe.fazenda.sp.gov.br/ws/nfestatusservico4.asmx',
        'AUTORIZACAO': 'nfe.fazenda.sp.gov.br/ws/nfeautorizacao4.asmx',
        'RECIBO': 'nfe.fazenda.sp.gov.br/ws/nferetautorizacao4.asmx',
        'CHAVE': 'nfe.fazenda.sp.gov.br/ws/nfeconsultaprotocolo4.asmx',
        'INUTILIZACAO': 'nfe.fazenda.sp.gov.br/ws/nfeinutilizacao4.asmx',
        'EVENTOS': 'nfe.fazenda.sp.gov.br/ws/nferecepcaoevento4.asmx',
        'CADASTRO': 'nfe.fazenda.sp.gov.br/ws/cadconsultacadastro4.asmx',
        'HTTPS': 'https://',
        'HOMOLOGACAO': 'https://homologacao.'
        },
        'PREFEITURA': {
        'STATUS': 'nfe.fazenda.sp.gov.br/ws/nfestatusservico4.asmx',
        'CADASTRO': 'nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx',
        'AUTORIZACAO': 'nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx',
        'CANCELAMENTO': 'nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx',
        'CONSULTA': 'nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx',
        'TESTEENVIOLOTERPS': 'nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx',
        'ENVIOLOTERPS': 'nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx',
        'HTTPS': 'https://',
        }
    }


class PostXML:

    def __init__(self, cert, key, uf="PREFEITURA"):
        self.environment = 2 if uf == "SP" else 1
        self.cert = cert
        self.key = key
        self.uf = uf
        self.entityType = ["SP", "PREFEITURA"]

    def _getUrl(self, type):
        lista = ["SP", 'PREFEITURA']
        if self.uf.upper() in lista:
            if self.environment == 1:
                environment = 'HTTPS'
                self.url = NFE[self.uf.upper()][environment] + NFE[self.uf.upper()][type]
            else:
                environment = 'HOMOLOGACAO'
                self.url = NFE[self.uf.upper()][environment] + NFE[self.uf.upper()][type]
        return self.url

    def _postHeaders(self):
        response = {
            'content-type': 'application/soap+xml; charset=utf-8;',
            'Accept': 'application/soap+xml; charset=utf-8;',
            'Cache-Control': "no-cache",
            'Host': "nfe.prefeitura.sp.gov.br",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
        }
        return response

    def _post(self, url, xml):
        try:
            xmlDef = '<?xml version="1.0" encoding="UTF-8"?>'
            xml = re.sub('<>(.*?)</>',
                         lambda x: x.group(0).replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', ''),
                         etree.tostring(xml, encoding='unicode').replace('\n', '')
                         )
            xml = xmlDef + xml

            certFile = "../certfiles/converted.crt"
            keyFile = "../certfiles/privateKey.key"
            caCertFile = "../certfiles/cacert.pem"

            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.settimeout(20)
            socks = ssl.wrap_socket(sock=clientSocket,
                                    keyfile=keyFile,
                                    certfile=certFile,
                                    cert_reqs=ssl.CERT_REQUIRED,
                                    ssl_version=ssl.PROTOCOL_TLSv1,
                                    ca_certs=caCertFile,
                                    )

            s = requests.Session()

            s.mount('http://', NewAdapter(soqt=socks))
            s.mount('https://', NewAdapter(soqt=socks))

            result = s.post(url, xml, headers=self._postHeaders(), verify=True)

            self.requestStatus = result.status_code
            print "Request Status: {}".format(self.requestStatus)
            result.encoding = "utf-8"
            xmlResult = str(result.content)
            xmlResult = xmlResult.replace("&lt;", "<")
            xmlResult = xmlResult.replace("&gt;", ">")
            if self.requestStatus == 200:
                return self._resultDissector(xmlResult)
            return xmlResult
        except requests.exceptions.RequestException as e:
            raise e

    def _resultDissector(self, xmlResult):
        if "ConsultaNFeEmitidasResponse xmlns=" in xmlResult and "<Sucesso>true</Sucesso>" in xmlResult:
            splitResult = xmlResult.split("</Cabecalho>")
            strResult = splitResult[1].split("</Retorno")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return self._getTail(strResult)
        if "ConsultaNFeRecebidasResponse xmlns=" in xmlResult and "<Sucesso>true</Sucesso>" in xmlResult:
            splitResult = xmlResult.split("</Cabecalho>")
            strResult = splitResult[1].split("</Retorno")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return self._getTail(strResult)
        if "ConsultaCNPJResponse xmlns=" in xmlResult and "<Sucesso>true</Sucesso>" in xmlResult:
            splitResult = xmlResult.split("</Cabecalho>")
            strResult = splitResult[1].split("</Retorno")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return self._resultDict(strResult)
        if "EnvioRPSResponse xmlns=" in xmlResult and "<Sucesso>true</Sucesso>" in xmlResult:
            splitResult = xmlResult.split("""<Alerta xmlns="">""")
            strResult = splitResult[1].split("</Alerta>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return self._resultDict(strResult)
        if "EnvioRPSResponse xmlns=" in xmlResult and "<Sucesso>false</Sucesso>" in xmlResult:
            splitResult = xmlResult.split("</Cabecalho>")
            strResult = splitResult[1].split("</RetornoEnvioRPS>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return self._resultDict(strResult)
        if "CancelamentoNFeResponse xmlns=" in xmlResult and "<Sucesso>true</Sucesso>" in xmlResult:
            splitResult = xmlResult.split("</Cabecalho>")
            strResult = splitResult[1].split("</RetornoCancelamentoNFe>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return self._resultDict(strResult)
        if "ConsultaNFeResponse xmlns=" in xmlResult and "<Sucesso>true</Sucesso>" in xmlResult:
            splitResult = xmlResult.split("<ChaveNFe>")
            splitResult = splitResult[1].replace("</ChaveNFe>", "")
            strResult = splitResult.split("</NFe>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return self._resultDict(strResult)
        if "Erro xmlns" in xmlResult:
            splitResult = xmlResult.split("""<Erro xmlns="">""")
            strResult = splitResult[1].split("</Erro>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return self._resultDict(strResult)
        else:
            try:
                xmlResult = xmlResult[38:]
                splitResult = xmlResult.split("<soap:Body>")
                strResult = splitResult[1].split("</soap:Body>")
                strResult = str(strResult[0])
                strResult = "<root>" + strResult + "</root>"
                return self._resultDict(strResult)
            except Exception as error:
                raise error

    def _resultDict(self, strResult):
        res = {}
        root = etree.fromstring(strResult)
        for i in root.iter():
            text = i.text
            text = text.encode("utf-8", "replace") if text else None
            if text:
                res.setdefault("{tag}".format(tag=i.tag), "{text}".format(text=text))
        return res

    def _getTail(self, strResult):
        tree = etree.fromstring(strResult)
        nfeData = []
        res = {}
        for i in tree:
            res.update({
                "SerieRPS": i.find('.//SerieRPS', namespaces={}).text,
                "NumeroRPS": i.find('.//NumeroRPS', namespaces={}).text,
                "DataEmissaoNFe": i.find('.//DataEmissaoNFe', namespaces={}).text,
                "CPFCNPJTomador": i.find('.//CPFCNPJTomador/CNPJ', namespaces={}).text,
                "CodigoVerificacao": i.find('.//CodigoVerificacao', namespaces={}).text,
                "NumeroNFe": i.find('.//NumeroNFe', namespaces={}).text
            })
            nfeData.append(res.copy())
        return nfeData

    def _constructXmlSoap(self, method, data, publicEntity):
        self.entityType = publicEntity
        if publicEntity == "SEFAZ":
            root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
              "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
            body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
            a = etree.SubElement(body, "nfeDadosMsg", xmlns=NAMESPACE_METODO_SEFAZ + method)
            a.append(data)
            return root
        if self.entityType == "PRODAM":
            root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
                "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
            body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
            a = etree.SubElement(body, "ConsultaCNPJRequest", xmlns=NAMESPACE_METODO_PRODAM)
            etree.SubElement(a, "VersaoSchema").text = "1"
            a.append(data)
            return root

    def consultSubscription(self, signedXml):
        root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
            "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
        body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
        a = etree.SubElement(body, "ConsultaCNPJRequest", xmlns=NAMESPACE_METODO_PRODAM)
        etree.SubElement(a, "VersaoSchema").text = "1"
        msgXml = etree.SubElement(a, "MensagemXML")
        msgXml.text = signedXml
        url = self._getUrl(type="CADASTRO")
        return self._post(url, root)

    def consultNfe(self, signedXml):
        root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
            "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
        body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
        a = etree.SubElement(body, "ConsultaNFeRequest", xmlns=NAMESPACE_METODO_PRODAM)
        etree.SubElement(a, "VersaoSchema").text = "1"
        msgXml = etree.SubElement(a, "MensagemXML")
        msgXml.text = signedXml
        url = self._getUrl(type="CONSULTA")
        return self._post(url, root)

    def cancelNfe(self, signedXml):
        root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
            "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
        body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
        a = etree.SubElement(body, "CancelamentoNFeRequest", xmlns=NAMESPACE_METODO_PRODAM)
        etree.SubElement(a, "VersaoSchema").text = "1"
        msgXml = etree.SubElement(a, "MensagemXML")
        msgXml.text = signedXml
        url = self._getUrl(type="CANCELAMENTO")
        return self._post(url, root)

    def bulkingRPSTests(self, signedXml):
        root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
            "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
        body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
        a = etree.SubElement(body, "TesteEnvioLoteRPSRequest", xmlns=NAMESPACE_METODO_PRODAM)
        etree.SubElement(a, "VersaoSchema").text = "1"
        msgXml = etree.SubElement(a, "MensagemXML")
        msgXml.text = signedXml
        url = self._getUrl(type="TESTEENVIOLOTERPS")
        return self._post(url, root)

    def bulkRPS(self, signedXml):
        root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
            "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
        body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
        a = etree.SubElement(body, "EnvioLoteRPSRequest", xmlns=NAMESPACE_METODO_PRODAM)
        etree.SubElement(a, "VersaoSchema").text = "1"
        msgXml = etree.SubElement(a, "MensagemXML")
        msgXml.text = signedXml
        url = self._getUrl(type="ENVIOLOTERPS")
        return self._post(url, root)

    def sendRPS(self, signedXml):
        root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
            "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
        body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
        a = etree.SubElement(body, "EnvioRPSRequest", xmlns=NAMESPACE_METODO_PRODAM)
        etree.SubElement(a, "VersaoSchema").text = "1"
        msgXml = etree.SubElement(a, "MensagemXML")
        msgXml.text = signedXml
        url = self._getUrl(type="AUTORIZACAO")
        return self._post(url, root)

    def consultReceivedNfe(self, signedXml):
        root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
            "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
        body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
        a = etree.SubElement(body, "ConsultaNFeRecebidasRequest", xmlns=NAMESPACE_METODO_PRODAM)
        etree.SubElement(a, "VersaoSchema").text = "1"
        msgXml = etree.SubElement(a, "MensagemXML")
        msgXml.text = signedXml
        url = self._getUrl(type="CONSULTA")
        return self._post(url, root)

    def consultSentNfe(self, signedXml):
        root = etree.Element("{%s}Envelope" % NAMESPACE_SOAP, nsmap={
            "xsi": NAMESPACE_XSI, "xsd": NAMESPACE_XSD, "soap": NAMESPACE_SOAP})
        body = etree.SubElement(root, "{%s}Body" % NAMESPACE_SOAP)
        a = etree.SubElement(body, "ConsultaNFeEmitidasRequest", xmlns=NAMESPACE_METODO_PRODAM)
        etree.SubElement(a, "VersaoSchema").text = "1"
        msgXml = etree.SubElement(a, "MensagemXML")
        msgXml.text = signedXml
        url = self._getUrl(type="CONSULTA")
        return self._post(url, root)

    def sefazSubscription(self, cnpj):
        if self.uf.upper() == "SEFAZ":
            root = etree.Element("ConsCad", versao="2.00", xmlns=NAMESPACE_NFE)
            info = etree.SubElement(root, "infCons")
            etree.SubElement(info, "xServ").text = "CONS-CAD"
            etree.SubElement(info, "UF").text = self.uf.upper()
            etree.SubElement(info, "CNPJ").text = cnpj
            xml = self._constructXmlSoap("CadConsultaCadastro4", root, self.uf)
            url = self._getUrl(type="CADASTRO")
            return self._post(url, xml)

        elif self.uf.upper() == "PRODAM":
            root = etree.Element("MensagemXML")
            cabecalho = etree.SubElement(root, "Cabecalho", Versao="1")
            remetente = etree.SubElement(cabecalho, "CNPJRemetente")
            etree.SubElement(remetente, "CNPJ").text = cnpj
            contribuinte = etree.SubElement(root, "CNPJContribuinte")
            etree.SubElement(contribuinte, "CNPJ").text = cnpj
            xmlToSign = etree.tostring(root)
            xmlSigned = Certificate.signWithA1Cert(xmlToSign, certContent=self.cert, rsaKeyContent=self.key)
            xmlSigned = (etree.fromstring(xmlSigned))
            xmlSigned = self._constructXmlSoap("ConsultaCNPJRequest", xmlSigned, self.uf)
            url = self._getUrl(type="CADASTRO")
            return self._post(url, xmlSigned)

        else:
            url = self._getUrl(type="CADASTRO")
            root = etree.Element("ConsCad", versao="2.00", xmlns=NAMESPACE_NFE)
            info = etree.SubElement(root, "infCons")
            etree.SubElement(info, "xServ").text = "CONS-CAD"
            etree.SubElement(info, "UF").text = self.uf.upper()
            etree.SubElement(info, "CNPJ").text = cnpj
            xml = self._constructXmlSoap("ConsultaCNPJ", root, self.uf)
            return self._post(url, xml)

    def serviceStatus(self):
        url = self._getUrl("STATUS")
        root = etree.Element("consStatServ", versao="4.00", xmlns=NAMESPACE_NFE)
        etree.SubElement(root, "tpAmb").text = str(self.environment)
        etree.SubElement(root, "cUF").text = "35"
        etree.SubElement(root, "xServ").text = "STATUS"
        xml = self._constructXmlSoap("NFeStatusServico4", root, self.uf)
        print(etree.tostring(xml))
        return self._post(url, xml)

    def receiptConsult(self, number):
        url = self._getUrl(type="RECIBO")
        root = etree.Element("consReciNFe", versao="4.00", xmlns=NAMESPACE_NFE)
        etree.SubElement(root, "tpAmb").text = str(self.environment)
        etree.SubElement(root, "nRec").text = number
        xml = self._constructXmlSoap("NFeRetAutorizacao4", root, self.uf)
        return self._post(url, xml)

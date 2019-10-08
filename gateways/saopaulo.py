from utils.connection import NewAdapter
from utils.rps import Rps
from utils.response import Response
from utils.schemas import schemaCreateRps, schemaCancelRps, schemaConsultNfes
from ssl import wrap_socket, CERT_REQUIRED, PROTOCOL_TLSv1
import requests
import socket


class SaopauloGateway:

    @classmethod
    def sendRps(cls, privateKeyContent, certificateContent, **kwargs):
        xml = Rps.xmlCreateRps(
            xml=schemaCreateRps,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **kwargs
        )

        return cls.postRequest(xml=xml, method="rps")

    @classmethod
    def cancelRps(cls, privateKeyContent, certificateContent, **kwargs):
        xml = Rps.cancelRps(
            xml=schemaCancelRps,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **kwargs
        )
        return cls.postRequest(xml=xml, method="rps")

    @classmethod
    def consultNfes(cls, privateKeyContent, certificateContent, **kwargs):
        xml = Rps.consultNfes(
            xml=schemaConsultNfes,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **kwargs
        )
        return cls.postRequest(xml=xml, method="consult")

    @classmethod
    def postRequest(cls, xml, method):
        certFile = "../static/certificate.crt"
        keyFile = "../static/rsaKey.pem"
        caCertFile = "../static/cacert.pem"

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.settimeout(20)
        socks = wrap_socket(
            sock=clientSocket,
            keyfile=keyFile,
            certfile=certFile,
            cert_reqs=CERT_REQUIRED,
            ssl_version=PROTOCOL_TLSv1,
            ca_certs=caCertFile,
        )

        session = requests.Session()

        session.mount('http://', NewAdapter(soqt=socks))
        session.mount('https://', NewAdapter(soqt=socks))

        headers = {
            'content-type': 'application/soap+xml; charset=utf-8;',
            'Accept': 'application/soap+xml; charset=utf-8;',
            'Cache-Control': "no-cache",
            'Host': "nfe.prefeitura.sp.gov.br",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
        }

        response = session.post(
            "https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx",
            xml,
            headers=headers,
            verify=True)

        status = response.status_code
        if status != 200:
            return "Error"

        if method == "consult":
            return Response.getTail(cls.clearedResponse(response))

        if method == "rps":
            return Response.resultDict(cls.clearedResponse(response))


    @classmethod
    def clearedResponse(cls, response):
        response.encoding = "utf-8"
        xmlResponse = str(response.content)
        xmlResponse = xmlResponse.replace("&lt;", "<")
        xmlResponse = xmlResponse.replace("&gt;", ">")
        return xmlResponse
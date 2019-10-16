from ..utils.rps import Rps
from ..utils.response import Response
from ..utils.schemas import schemaCreateRps, schemaCancelRps, schemaConsultNfes
from ..utils.compatibility import stringEncode, stringDecode
from requests import post


class SaopauloGateway:

    @classmethod
    def sendRps(cls, privateKey, certificate, **kwargs):
        xml = Rps.xmlCreateRps(
            xml=schemaCreateRps,
            privateKeyContent=privateKey,
            certificateContent=certificate,
            **kwargs
        )

        return cls.sendRequest(
            xml=xml,
            privateKey=privateKey,
            certificate=certificate,
            method="rps",
        )

    @classmethod
    def cancelRps(cls, privateKey, certificate, **kwargs):
        xml = Rps.cancelRps(
            xml=schemaCancelRps,
            privateKeyContent=privateKey,
            certificateContent=certificate,
            **kwargs
        )

        return cls.sendRequest(
            xml=xml,
            privateKey=privateKey,
            certificate=certificate,
            method="rps",
        )

    @classmethod
    def consultNfes(cls, privateKey, certificate, **kwargs):
        xml = Rps.consultNfes(
            xml=schemaConsultNfes,
            privateKeyContent=privateKey,
            certificateContent=certificate,
            **kwargs
        )

        return cls.sendRequest(
            xml=xml,
            privateKey=privateKey,
            certificate=certificate,
            method="consult",
        )

    @classmethod
    def clearedResponse(cls, response):
        xmlResponse = response.replace("&lt;", "<")
        xmlResponse = xmlResponse.replace("&gt;", ">")
        return xmlResponse

    @classmethod
    def sendRequest(cls, privateKey, certificate, xml, method):
        certPath = "/tmp/cert.crt"
        keyPath = "/tmp/rsaKey.pem"

        headers = {
            "Content-Type": "application/soap+xml; charset=utf-8;",
            "Accept": "application/soap+xml; charset=utf-8;",
            "Cache-Control": "no-cache",
            "Host": "nfe.prefeitura.sp.gov.br",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        with open(certPath, "w") as tempCert:
            tempCert.write(certificate)
        tempCert.close()

        with open(keyPath, "w") as tempKey:
            tempKey.write(privateKey)
        tempKey.close()

        response = post(
            url="https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx",
            data=stringEncode(xml),
            headers=headers,
            cert=(certPath, keyPath),
            verify=True
        )

        status = response.status_code
        content = stringDecode(response.content)

        if status != 200:
            return {}, status

        if method == "consult":
            return Response.getTail(cls.clearedResponse(content)), status

        if method == "rps":
            return Response.resultDict(cls.clearedResponse(content)), status

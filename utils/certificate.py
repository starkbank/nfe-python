

class Certificate:

    @classmethod
    def getContent(cls, text):
        certBuffer = text.replace("\n", "")
        certData = certBuffer.split("-----BEGIN CERTIFICATE-----")
        certBuffer = str((certData[1].replace("-----END CERTIFICATE-----", "")))
        return certBuffer

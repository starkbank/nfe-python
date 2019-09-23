from xmlsigner.signerXml import SignCert
from services.Services import Services
from lxml import etree


certificateFile = "./certfiles/converted.crt"
privateKeyRSA = "./certfiles/privRSAkey.pem"
privateKeyFile = "./certfiles/RSAPrivateKey.pem"

objSignCert = SignCert(
    privateKeyContent=open(privateKeyRSA).read(),
    certificateContent=open(certificateFile).read(),
    rsaKeyContent=open(privateKeyRSA).read()
)


certContent = objSignCert.loadCert()
# print(certContent)
print(objSignCert.loadPem())
exit()
xmlEnvelope = "file.xml"
with open(xmlEnvelope, 'rb') as xmlEnvelope:
    xmlData = xmlEnvelope.read()

# Simply sign with extended A1 certificate
xmlEnvelope = etree.fromstring(xmlData)
signedRoot = objSignCert.signWithA1Cert(xmlEnvelope)
print("Signed root: %s" % signedRoot)

# Sign and post a xml example:
objServ = Services(
    certificateContent=open("./certfiles/converted.crt", "rb").read(),
    rsaKeyContent=open("./certfiles/privRSAkey.pem", "rb").read(),
    privateKeyContent=open("./certfiles/privateKey.key", "rb").read()
)

taxId = "00623904000173"
taxPayerId = "00623904000173"
result = objServ.consultTaxIdSubscription(taxId=taxId, taxPayerId=taxPayerId)
print(result)


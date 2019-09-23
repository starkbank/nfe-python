import hashlib
import re
from lxml import etree
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Integer import b64e, b64d


def sign(xml, certContent, rsaKeyContent, signIdValue=None):
    """Return xmldsig XML string from xml_string of XML.
    Args:
      xml: str of bytestring xml to sign
      certContent: str content of certificate file
      rsaKeyContent: RSA key private content
      signIdValue: str of signature id value
    Returns:
      str: signed bytestring xml
    """
    keyInfoXml = """<KeyInfo><X509Data/></KeyInfo>"""

    constSignatureXml = \
        """<Signature %(signatureId)sxmlns="http://www.w3.org/2000/09/xmldsig#">%(signedInfoXml)s<SignatureValue>%(signatureValue)s</SignatureValue>%(keyInfoXml)s</Signature>"""

    signedInfoXml = _signedInfo(xml)
    signatureValue = signedWithRSA(signedInfoXml, rsaKeyContent)

    if signIdValue is None:
        signatureId = ""
    else:
        signatureId = "Id='%s' " % signIdValue

    signatureXml = constSignatureXml % {
        "signedInfoXml": signedInfoXml,
        "signatureValue": b64e(signatureValue),
        "keyInfoXml": keyInfoXml,
        "signatureId": signatureId,
    }

    prefix = "</p1:"
    foo = xml.split(prefix)
    after = prefix+foo[1]
    signedXml = foo[0] + signatureXml + after

    ns = {"ns": "http://www.w3.org/2000/09/xmldsig#"}

    signedXml = etree.fromstring(signedXml)
    tagX509Data = signedXml.find(".//ns:X509Data", namespaces=ns)

    etree.SubElement(tagX509Data, "X509Certificate").text = certContent
    xmlEnvelope = etree.tostring(signedXml)

    return xmlEnvelope


def verify(xml, rsaKeyContent):
    """Return if <Signature> is valid for "xml"
    Args:
      xml: str of XML with xmldsig <Signature> element
      rsaKeyContent: RSA key private content
    Returns:
      bool: signature for "xml" is valid
    """
    rxSignature = re.compile("<Signature.*?</Signature>")
    signatureXml = rxSignature.search(xml).group(0)
    unsignedXml = xml.replace(signatureXml, "")
    reSignatureValue = re.compile("<SignatureValue[^>]*>([^>]+)</SignatureValue>")
    signatureValue = reSignatureValue.search(signatureXml).group(1)
    expected = b64d(signatureValue)
    signedInfoXml = _signedInfo(unsignedXml)
    actual = signedWithRSA(signedInfoXml, rsaKeyContent=rsaKeyContent)
    isVerified = (expected == actual)

    return isVerified


def _digest(data):
    """SHA1 hash digest of message data.

    Implements RFC2437, 9.2.1 EMSA-PKCS1-v1_5, Step 1. for "Hash = SHA1"

    Args:
      data: str of bytes to digest
    Returns:
      str: of bytes of digest from "data"
    """
    hasher = hashlib.sha1()
    hasher.update(data)

    return hasher.digest()


def getXmlnsPrefixes(xml):
    """Return string of root namespace prefix attributes in given order.
    Args:
      xml: str of bytestring xml
    Returns:
      str: [xmlns:prefix="uri"] list ordered as in "xml"
    """
    rxRoot = re.compile("<[^> ]+ ?([^>]*)>")
    rxNs = re.compile("xmlns:[^> ]+")

    if rxRoot.match(xml):
        rootAttr = rxRoot.match(xml).group(1)
        nsAttrs = [a for a in rootAttr.split(" ") if rxNs.match(a)]
        return " ".join(nsAttrs)
    return None


def _signedInfo(xml):
    """Return <SignedInfo> for bytestring xml.
    Args:
      xml: str of bytestring
    Returns:
      str: xml bytestring of <SignedInfo> computed from "xml"
    """
    signedInfoXml = \
        """<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#"%(xmlnsAttr)s><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod><SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform><Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></DigestMethod><DigestValue>%(digestValue)s</DigestValue></Reference></SignedInfo>"""

    xmlnsAttr = getXmlnsPrefixes(xml)
    if xmlnsAttr:
        xmlnsAttr = " %s" % xmlnsAttr

    signedInfoXml = signedInfoXml % {
        "digestValue": b64e(_digest(xml)),
        "xmlnsAttr": xmlnsAttr
    }

    return signedInfoXml


def signedWithRSA(data, rsaKeyContent):
    """SHA1 hash digest of message data.
    Args:
      data: str of bytestring
      rsaKeyContent: str extracted content of RSA Private Key
    Returns:
      str: xml bytestring of <SignedInfo> computed from "xml"
    """
    digest = SHA.new(data)
    privateKey = RSA.importKey(rsaKeyContent)
    signer = PKCS1_v1_5.new(privateKey)
    signed = signer.sign(digest)

    return signed

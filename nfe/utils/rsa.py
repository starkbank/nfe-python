from base64 import b64encode
from hashlib import sha1
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from ..utils.compatibility import stringEncode


class Rsa:

    @classmethod
    def sign(cls, text, privateKeyContent):
        digest = SHA.new(stringEncode(text))
        rsaKey = RSA.importKey(privateKeyContent)
        signer = PKCS1_v1_5.new(rsaKey)
        signature = signer.sign(digest)
        return b64encode(signature)

    @classmethod
    def digest(cls, text):
        hasher = sha1()
        hasher.update(stringEncode(text))
        digest = hasher.digest()
        return b64encode(digest)

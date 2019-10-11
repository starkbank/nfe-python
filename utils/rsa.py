from base64 import b64encode
from hashlib import sha1
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


class Rsa:

    @classmethod
    def sign(cls, text, privateKeyContent):
        digest = SHA.new(text.encode("utf8"))
        rsaKey = RSA.importKey(privateKeyContent)
        signer = PKCS1_v1_5.new(rsaKey)
        signature = signer.sign(digest)
        return b64encode(signature)

    @classmethod
    def digest(cls, text):
        hasher = sha1()
        hasher.update(text)
        digest = hasher.digest()
        return b64encode(digest)

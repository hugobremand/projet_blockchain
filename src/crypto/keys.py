from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import hashlib


class WalletKeys:
    def __init__(self):
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),  
            default_backend()
        )
        self.public_key = self.private_key.public_key()

    def get_private_key_bytes(self):
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

    def get_public_key_bytes(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def get_address(self):
        public_bytes = self.get_public_key_bytes()
        sha = hashlib.sha256(public_bytes).hexdigest()
        return sha
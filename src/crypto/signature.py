from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature


def sign_message(private_key, message: bytes) -> bytes:
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )
    return signature


def verify_signature(public_key, message: bytes, signature: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False
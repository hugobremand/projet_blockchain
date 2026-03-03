from src.crypto.keys import WalletKeys
from src.crypto.signature import sign_message, verify_signature


def test_signature_valid():
    wallet = WalletKeys()
    message = b"hello"

    signature = sign_message(wallet.private_key, message)

    assert verify_signature(wallet.public_key, message, signature) is True


def test_signature_invalid_if_message_modified():
    wallet = WalletKeys()
    message = b"hello"

    signature = sign_message(wallet.private_key, message)

    modified_message = b"hello modified"

    assert verify_signature(wallet.public_key, modified_message, signature) is False
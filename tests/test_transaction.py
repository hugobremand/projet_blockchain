from src.crypto.keys import WalletKeys
from src.core.transaction import Transaction


def test_transaction_valid():
    wallet = WalletKeys()

    tx = Transaction(
        sender=wallet.get_address(),
        receiver="receiver",
        amount=10,
        nonce=1
    )

    tx.sign(wallet.private_key)

    assert tx.is_valid(wallet.public_key) is True


def test_transaction_invalid_if_modified():
    wallet = WalletKeys()

    tx = Transaction(
        sender=wallet.get_address(),
        receiver="receiver",
        amount=10,
        nonce=1
    )

    tx.sign(wallet.private_key)

    
    tx.amount = 999

    assert tx.is_valid(wallet.public_key) is False
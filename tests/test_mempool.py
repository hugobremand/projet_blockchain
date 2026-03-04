import pytest
from src.crypto.keys import WalletKeys
from src.core.transaction import Transaction
from src.core.mempool import Mempool


def create_signed_transaction():
    wallet = WalletKeys()

    tx = Transaction(
        sender=wallet.get_address(),
        receiver="receiver",
        amount=10,
        nonce=1
    )

    tx.sign(wallet.private_key)

    return tx, wallet


def test_add_valid_transaction():
    mempool = Mempool()
    tx, wallet = create_signed_transaction()

    mempool.add_transaction(tx, wallet.public_key)

    assert len(mempool.transactions) == 1


def test_reject_invalid_transaction():
    mempool = Mempool()
    tx, wallet = create_signed_transaction()

    tx.amount = 999  # modification après signature

    with pytest.raises(ValueError):
        mempool.add_transaction(tx, wallet.public_key)


def test_remove_transactions():
    mempool = Mempool()
    tx, wallet = create_signed_transaction()

    mempool.add_transaction(tx, wallet.public_key)

    mempool.remove_transactions([tx])

    assert len(mempool.transactions) == 0
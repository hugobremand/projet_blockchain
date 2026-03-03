from src.crypto.keys import WalletKeys
from src.core.transaction import Transaction
from src.core.block import Block


def create_sample_transaction():
    wallet = WalletKeys()

    tx = Transaction(
        sender=wallet.get_address(),
        receiver="receiver",
        amount=10,
        nonce=1
    )

    tx.sign(wallet.private_key)
    return tx


def test_block_creation():
    tx = create_sample_transaction()

    block = Block(
        previous_hash="abc123",
        transactions=[tx]
    )

    assert block.header.previous_hash == "abc123"
    assert block.header.merkle_root is not None


def test_block_hash_changes_if_nonce_changes():
    tx = create_sample_transaction()

    block = Block(
        previous_hash="abc123",
        transactions=[tx]
    )

    original_hash = block.compute_hash()

    block.header.nonce += 1

    new_hash = block.compute_hash()

    assert original_hash != new_hash
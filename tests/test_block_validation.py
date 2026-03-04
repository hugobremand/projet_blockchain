import pytest
from src.crypto.keys import WalletKeys
from src.core.transaction import Transaction
from src.core.block import Block
from src.core.chain import Blockchain


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


def test_reject_block_without_mining():
    blockchain = Blockchain()
    tx, wallet = create_signed_transaction()

    block = Block(
        previous_hash=blockchain.get_latest_block().hash,
        transactions=[tx]
    )

    # On n'appelle PAS block.mine()
    with pytest.raises(ValueError):
        blockchain.add_block(block)


def test_reject_block_with_unsigned_transaction():
    blockchain = Blockchain()
    wallet = WalletKeys()

    tx = Transaction(
        sender=wallet.get_address(),
        receiver="receiver",
        amount=10,
        nonce=1
    )
    # Pas de signature

    block = Block(
        previous_hash=blockchain.get_latest_block().hash,
        transactions=[tx]
    )

    block.mine(blockchain.difficulty)

    with pytest.raises(ValueError):
        blockchain.add_block(block)
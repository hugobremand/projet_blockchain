from src.crypto.keys import WalletKeys
from src.core.transaction import Transaction
from src.core.chain import Blockchain
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


def test_mining_creates_new_block():
    blockchain = Blockchain()
    mempool = Mempool()

    tx, wallet = create_signed_transaction()

    mempool.add_transaction(tx, wallet.public_key)

    blockchain.mine_pending_transactions(mempool)

    assert len(blockchain.chain) == 2


def test_mined_block_respects_difficulty():
    blockchain = Blockchain()
    mempool = Mempool()

    tx, wallet = create_signed_transaction()
    mempool.add_transaction(tx, wallet.public_key)

    blockchain.mine_pending_transactions(mempool)

    mined_block = blockchain.chain[1]

    assert mined_block.hash.startswith("0" * blockchain.difficulty)
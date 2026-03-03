# from src.crypto.keys import WalletKeys
# from src.core.transaction import Transaction
# from src.core.block import Block
# from src.core.chain import Blockchain


# def create_signed_transaction():
#     wallet = WalletKeys()

#     tx = Transaction(
#         sender=wallet.get_address(),
#         receiver="receiver",
#         amount=10,
#         nonce=1
#     )

#     tx.sign(wallet.private_key)
#     return tx


# def test_genesis_block_exists():
#     blockchain = Blockchain()

#     assert len(blockchain.chain) == 1
#     assert blockchain.chain[0].header.previous_hash == "0"


# def test_add_block():
#     blockchain = Blockchain()

#     tx = create_signed_transaction()

#     new_block = Block(
#         previous_hash=blockchain.get_latest_block().compute_hash(),
#         transactions=[tx]
#     )

#     blockchain.add_block(new_block)

#     assert len(blockchain.chain) == 2


# def test_chain_invalid_if_tampered():
#     blockchain = Blockchain()

#     tx = create_signed_transaction()

#     new_block = Block(
#         previous_hash=blockchain.get_latest_block().compute_hash(),
#         transactions=[tx]
#     )

#     blockchain.add_block(new_block)

#     blockchain.chain[1].header.nonce += 1

#     assert blockchain.is_chain_valid() is False
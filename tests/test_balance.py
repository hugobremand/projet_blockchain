# import pytest
# from src.crypto.keys import WalletKeys
# from src.core.transaction import Transaction
# from src.core.chain import Blockchain
# from src.core.block import Block


# def test_balance_updates_correctly():
#     blockchain = Blockchain()

#     sender_wallet = WalletKeys()
#     receiver_wallet = WalletKeys()

#     # On simule un "mint" initial en donnant 100 au sender
#     genesis_reward = Transaction(
#         sender="SYSTEM",
#         receiver=sender_wallet.get_address(),
#         amount=100,
#         nonce=0
#     )
#     genesis_reward.signature = "system"  # bypass signature for system

#     block = Block(
#         previous_hash=blockchain.get_latest_block().hash,
#         transactions=[genesis_reward]
#     )

#     block.mine(blockchain.difficulty)
#     blockchain.add_block(block)

#     assert blockchain.get_balance(sender_wallet.get_address()) == 100


# def test_reject_transaction_if_insufficient_balance():
#     blockchain = Blockchain()

#     wallet = WalletKeys()

#     tx = Transaction(
#         sender=wallet.get_address(),
#         receiver="receiver",
#         amount=50,
#         nonce=1
#     )
#     tx.sign(wallet.private_key)

#     block = Block(
#         previous_hash=blockchain.get_latest_block().hash,
#         transactions=[tx]
#     )

#     block.mine(blockchain.difficulty)

#     with pytest.raises(ValueError):
#         blockchain.add_block(block)
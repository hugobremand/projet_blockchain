from src.crypto.keys import WalletKeys


def test_wallet_generates_keys():
    wallet = WalletKeys()

    assert wallet.private_key is not None
    assert wallet.public_key is not None


def test_wallet_generates_address():
    wallet = WalletKeys()
    address = wallet.get_address()

    assert isinstance(address, str)
    assert len(address) == 64  
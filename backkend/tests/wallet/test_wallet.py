from backkend.wallet.wallet import Wallet


def test_verify_a_signature_is_valid():
    data = {'test': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert Wallet.verify(wallet.public_key, data, signature)


def test_verify_a_signature_is_not_valid():
    data = {'test': 'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert not Wallet.verify(Wallet().public_key, data, signature)

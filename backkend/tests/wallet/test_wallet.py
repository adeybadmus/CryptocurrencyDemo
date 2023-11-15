from backkend.wallet.wallet import Wallet


def test_verify_a_signature_is_valid():
    """Test the verification of a valid signature.

    Checks:
    1. Creates a Wallet instance.
    2. Signs a piece of data with the wallet.
    3. Verifies that the signature is valid using the wallet's public key.
    """

    wallet = Wallet()
    data = {'test': 'test_data'}
    signature = wallet.sign(data)
    assert Wallet.verify(wallet.public_key, data, signature)


def test_verify_a_signature_is_not_valid():
    """Test the verification of an invalid signature.

    Checks:
    1. Creates a Wallet instance.
    2. Signs a piece of data with the wallet.
    3. Verifies that the signature is not valid using a different wallet's public key.
    """

    wallet = Wallet()
    data = {'test': 'test_data'}
    signature = wallet.sign(data)
    assert not Wallet.verify(Wallet().public_key, data, signature)


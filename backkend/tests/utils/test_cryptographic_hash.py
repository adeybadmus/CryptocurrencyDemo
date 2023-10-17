from backkend.utils.cryptographic_hash import cryptographic_hash


def test_cryptographic_hash():
    assert cryptographic_hash(
        [2], 'three', 1) == cryptographic_hash('three', [2], 1)

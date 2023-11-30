from backkend.utils.cryptographic_hash import cryptographic_hash


def test_cryptographic_hash():
    """Test the cryptographic_hash function.

    This test verifies that the cryptographic_hash function produces the same hash
    regardless of the order of the input arguments.

    Checks:
    1. Verifies that the cryptographic_hash function produces the same hash
       regardless of the order of the input arguments.
    """

    # Create hash results with different order of input arguments
    hash_result_1 = cryptographic_hash([2], 'three', 1)
    hash_result_2 = cryptographic_hash('three', [2], 1)

    # Verify that the hash results are equal
    assert hash_result_1 == hash_result_2

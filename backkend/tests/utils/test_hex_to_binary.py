from backkend.utils.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    original_number = 500
    hex_number = hex(original_number)[2:]
    new_binary_number = hex_to_binary(hex_number)

    assert int(new_binary_number, 2) == original_number

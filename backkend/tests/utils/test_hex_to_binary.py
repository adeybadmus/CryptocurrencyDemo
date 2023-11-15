from backkend.utils.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    """Test the hex_to_binary function.

    Checks:
    1. Converts a decimal number to hexadecimal.
    2. Uses hex_to_binary to convert the hexadecimal number to binary.
    3. Converts the binary number back to decimal.
    4. Asserts that the final decimal number matches the original number.
    """

    original_number = 500
    hex_number = hex(original_number)[2:]
    new_binary_number = hex_to_binary(hex_number)
    converted_decimal_number = int(new_binary_number, 2)
    assert converted_decimal_number == original_number


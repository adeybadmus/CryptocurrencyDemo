from backkend.utils.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    """Test the hex_to_binary function.

    This test checks:
    1. Converts a decimal number (500) to hexadecimal.
    2. Uses hex_to_binary to convert the hexadecimal number to binary.
    3. Converts the binary number back to decimal.
    4. Asserts that the final decimal number matches the original number (500).
    """

    # Step 1: Convert decimal to hexadecimal
    original_number = 500
    hex_number = hex(original_number)[2:]

    # Step 2: Convert hexadecimal to binary using hex_to_binary function
    new_binary_number = hex_to_binary(hex_number)

    # Step 3: Convert binary back to decimal
    converted_decimal_number = int(new_binary_number, 2)

    # Step 4: Assert that the final decimal number matches the original number
    assert converted_decimal_number == original_number



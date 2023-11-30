from backkend.utils.cryptographic_hash import cryptographic_hash

HEX_TO_BINARY_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}


def hex_to_binary(hex_string):
    """Converts a hexadecimal string to its binary representation.

    Args:
        hex_string (str): The input hexadecimal string.

    Returns:
        str: The binary representation of the input hexadecimal string.
    """
    binary_string = ''
    for character in hex_string:
        binary_string += HEX_TO_BINARY_TABLE[character]
    return binary_string


def main():
    """Example usage of hex_to_binary function.

    Example 1:
        Demonstrates converting a decimal number to hexadecimal and then to binary.

    Example 2:
        Demonstrates converting a cryptographic hash to binary.
    """
    # Example 1
    number = 451
    hex_number = hex(number)[2:]
    print(f'hex_number: {hex_number}')

    binary_number = hex_to_binary(hex_number)
    print(f'binary_number: {binary_number}')

    # Example 2
    hex_to_binary_cryptographic_hash = hex_to_binary(
        cryptographic_hash('lunch'))
    print(f'hex_to_binary_cryptographic_hash: {hex_to_binary_cryptographic_hash}')


if __name__ == '__main__':
    main()

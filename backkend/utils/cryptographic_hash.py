import hashlib
import json


def cryptographic_hash(*args):
    """Generates a SHA-256 hash of the provided data.

    Args:
        *args: Variable number of arguments to be hashed.

    Returns:
        str: Hexadecimal representation of the computed hash.
    """
    # Convert each argument to a JSON string and sort them
    stringify_sorted_data = sorted(map(lambda data: json.dumps(data), args))

    # Concatenate the sorted JSON strings
    joined_data = "".join(stringify_sorted_data)

    # Compute the SHA-256 hash and return the hexadecimal representation
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    """Example usage of the cryptographic_hash function."""
    # Example 1
    result1 = cryptographic_hash('Ade', 'Yinka', 200)
    print(f"cryptographic_hash('Ade', 'Yinka', 200): {result1}")

    # Example 2
    result2 = cryptographic_hash(200, 'Yinka', 'Ade')
    print(f"cryptographic_hash(200, 'Yinka', 'Ade'): {result2}")


if __name__ == '__main__':
    main()

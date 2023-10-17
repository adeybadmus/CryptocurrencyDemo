import hashlib
import json


# def stringify_data(data):
# return json.dumps(data)


def cryptographic_hash(*args):
    """this method returns a sha-256 hash of the data supplied
    """
    # stringify_data = json.dumps(data)   # converts a number  to string, allow us use a hash a number as well as string
    # joined_data = stringify_data(args)
    stringify_sorted_data = sorted(map(lambda data: json.dumps(data), args))
    joined_data = "".join(stringify_sorted_data)
    # lambda function called data, takes sorted and mapped argument and converts it into json
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()
    # encode the data to octet digits (utf-8 standard- os and 1s), to ensure Data integrity and security during transmission


def main():
    print(
        f"cryptographic-hash('Ade', 'Yinka', 200): {cryptographic_hash('Ade', 'Yinka', 200)}")
    print(
        f"cryptographic-hash('Ade', 'Yinka', 200): {cryptographic_hash(200, 'Yinka', 'Ade')}")


if __name__ == '__main__':
    main()

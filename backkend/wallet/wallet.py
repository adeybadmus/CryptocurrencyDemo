"""
This is a representation of a miners wallet.
It holds information of the miners crypto balance
And it allows the miner to authorize transactions
"""
import uuid
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from backkend.config import STARTING_BALANCE
import json


class Wallet:
    address = str(uuid.uuid4())[0:8]
    balance = STARTING_BALANCE

    def __init__(self):
        # self.address = str(uuid.uuid4())[0:8]
        # self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1,
            default_backend()
        )
        self.public_key = self.private_key.public_key()

    def sign(self, data):
        """
        This will help generate a signature using the data provided
        and the local private key
        """
        return self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )

    @staticmethod
    def verify(public_key, data, signature):
        """
        This will verify the signature that is referencing the data and the original public key
        """
        try:
            public_key.verify(
                signature,
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )

            return True
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')

    data = {'test_info': 'test_data_two'}
    transaction_signature = wallet.sign(data)
    print(f'signature: {transaction_signature}')

    transaction_should_be_valid = Wallet.verify(
        wallet.public_key, data, transaction_signature)
    print(f'transaction_should_be_valid: {transaction_should_be_valid}')

    transaction_should_be_invalid = Wallet.verify(
        Wallet().public_key, data, transaction_signature
    )
    print(f'transaction_should_be_invalid: {transaction_should_be_invalid}')


if __name__ == '__main__':
    main()

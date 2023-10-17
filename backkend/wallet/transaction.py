import uuid
import time

from backkend.wallet.wallet import Wallet
#from backkend.config import MINING_REWARD
#from backkend.config import MINING_REWARD_INPUT

class Transaction:
    """
    logs the exchange of currency from a sender to one or more recipients
    """

    def __init__(self, sender_wallet, recipient, amount):
        self.id = str(uuid.uuid4())[0:8]
        self.output = self.create_transaction_output(
            sender_wallet,
            recipient,
            amount
        )

        self.input = self.create_transaction_input(sender_wallet, self.output)

    def create_transaction_output(self, sender_wallet, recipient, amount, output=None):
        """
        build the output data for the specific transaction
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance. Amount must be <= balance')
        output = {recipient: amount, sender_wallet.address: sender_wallet.balance - amount}
        return output

    def create_transaction_input(self, sender_wallet, output):
        """

        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    def update_transaction(self, sender_wallet, recipient, amount):
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance. Amount must be <=balance')
        if recipient in self.output:
            self.output[recipient] == self.output[recipient] + amount
        else:
            self.output[recipient] = amount

        self.output[sender_wallet.address] = \
            self.output[sender_wallet.address] - amount
        self.input = self.create_transaction_input(sender_wallet, self.output)


    def serialize_to_json(self):
        """
         serialises blockchain into a representation of a dictionary
        """
        return self.__dict__

    def deserilize_from_json(transaction_json):
        """
         serialises blockchain into a representation of a dictionary
        """
        return Transaction(**transaction_json)


    @staticmethod
    def is_a_valid_transaction(transaction):
        """
        This validates the transaction and
        raises an exception where the transaction is not valid
        """
        output_total = sum(transaction.output.values())
        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction output values')

        if not Wallet.verify(
                transaction.input['public_key'],
                transaction.output,
                transaction.input['signature']
        ):
            raise Exception('Invalid signature')


def main():
    transaction = Transaction(Wallet(), 'recipient', 10)
    print(f'transaction.__dict__: {transaction.__dict__}')


if __name__ == '__main__':
    main()

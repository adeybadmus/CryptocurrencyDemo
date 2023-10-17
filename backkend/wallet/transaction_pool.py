class TransactionPool:

    def __init__(self):
        self.transaction_map = {}

    def set_transaction(self, transaction):
        """
        this method will set a transaction in the transaction pool
        """
        self.transaction_map[transaction.id] = transaction

    def existing_transaction(self, address):
        """

        """
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == address:
                return transaction

    def transaction_data(self):
        """
        returns the transaction of the transaction pool in json serialised form
        """
        return list(map(
            lambda transaction: transaction.serialize_to_json(),
            self.transaction_map.values()
        ))

    def clear_chain_transactions(self, blockchain):
        """
        Removed all blockchain recorded transactions from the pool of transaction
        finds all transactions in relation to the transaction by ita ID and then deletes all
        The try except statement ensures that the application does not crash an continues if no transaction is found
        """
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass

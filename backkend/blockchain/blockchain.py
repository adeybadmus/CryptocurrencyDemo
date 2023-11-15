from backkend.blockchain.block import Block


"""
This code defines a Blockchain class that represents a basic blockchain. 

The class includes methods for
 
 1) Adding blocks
 2) Replacing the chain
 3) Serializing and deserializing from JSON
 4) Validating the chain. 
 
 The example usage at the end demonstrates the creation of a blockchain, adding four blocks, 
 and printing the blockchain's representation.
"""


class Blockchain:
    def __init__(self) -> None:
        """
        Constructor for the Blockchain class.

        Initializes the blockchain with the genesis block.
        """
        self.chain = [Block.genesis()]

    def add_a_block(self, data):
        """
        Adds a new block to the blockchain.

        Args:
            data (any): The data to be included in the new block.
        """
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self) -> str:
        """
        String representation of the Blockchain object.

        Returns:
            str: A formatted string representation.
        """
        return f'Blockchain-chain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replaces the current chain with a new one under certain conditions.

        Args:
            chain (list): The new blockchain to replace the current one.

        Raises:
            Exception: If the incoming chain is not longer or is not valid.
        """
        if len(chain) <= len(self.chain):
            raise Exception('The incoming chain must be longer than the current chain')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is not valid: {e}')
        self.chain = chain

    def to_json(self):
        """
        Serializes the blockchain into a list of blocks.

        Returns:
            list: A list of serialized blocks.
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def deserialise_from_json(blockchain_json):
        """
        Creates a Blockchain object from a serialized JSON representation.

        Args:
            blockchain_json (list): The serialized blockchain data.

        Returns:
            Blockchain: A Blockchain object.
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(
            lambda block_json: Block.deserialise_from_json(block_json),
            blockchain_json
        ))
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Verifies if an incoming chain is valid.

        The rules for validation are:
        1. The chain must start with the genesis block.
        2. The blocks must be validated correctly.

        Args:
            chain (list): The chain to be validated.

        Raises:
            Exception: If the chain is not valid.
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be the valid one')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_a_valid_block(last_block, block)


# Example usage
blockchain = Blockchain()
blockchain.add_a_block('one')
blockchain.add_a_block('two')
blockchain.add_a_block('three')
blockchain.add_a_block('four')

print(blockchain)

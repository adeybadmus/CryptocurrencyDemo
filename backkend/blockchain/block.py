import time
from backkend.config import MINE_RATE
from backkend.utils.cryptographic_hash import cryptographic_hash

"""
This code defines a Block class for the blockchain, including 

1) Methods for mining new blocks
2) Creating the genesis block
3) Adjusting difficulty
4) Validating blocks. 

The main function demonstrates the creation of a blockchain with a genesis block and the mining of a new block, 
with an attempt to validate it. 

The comments provide explanations for each section of the code. 
"""

# Initial data for the genesis block
GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'last_hash',
    'hash': 'origin_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """Class representing a block in the blockchain."""

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        """
        Constructor for the Block class.

        Args:
            timestamp (int): The timestamp of the block.
            last_hash (str): The hash of the previous block.
            hash (str): The hash of the current block.
            data (any): The data contained in the block.
            difficulty (int): The difficulty level for mining.
            nonce (int): A random number used in mining.
        """
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self) -> str:
        """
        String representation of the Block object.

        Returns:
            str: A formatted string representation.
        """
        return (
            'Block('
            f'timestamp: {self.timestamp},'
            f'last_hash: {self.last_hash},'
            f'hash: {self.hash},'
            f'data: {self.data},'
            f'difficulty: {self.difficulty},'
            f'nonce: {self.nonce})'
        )

    def __eq__(self, other):
        """
        Compare two Block objects for equality.

        Returns:
            bool: True if equal, False otherwise.
        """
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary.

        Returns:
            dict: A dictionary representation of the block.
        """
        return self.__dict__

    @staticmethod
    def deserialise_from_json(block_json):
        """
        Create a Block object from a serialized JSON representation.

        Args:
            block_json (dict): The serialized block data.

        Returns:
            Block: A Block object.
        """
        return Block(**block_json)

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on a given last block and data.

        Args:
            last_block (Block): The last block in the blockchain.
            data (any): The data to be included in the new block.

        Returns:
            Block: The mined block.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_mine_block_difficulty(last_block, timestamp)
        nonce = 0
        from backend.utils.cryptographic_hash import cryptographic_hash
        hash = cryptographic_hash(
            timestamp, last_hash, data, difficulty, nonce)
        while hash[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            hash = cryptographic_hash(
                timestamp, last_hash, data, difficulty, nonce)
        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Create the genesis block.

        Returns:
            Block: The genesis block.
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_mine_block_difficulty(last_block, new_timestamp):
        """
        Adjust the difficulty level for mining a new block.

        Args:
            last_block (Block): The last block in the blockchain.
            new_timestamp (int): The timestamp of the new block.

        Returns:
            int: The adjusted difficulty level.
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1
        return 1

    @staticmethod
    def is_a_valid_block(last_block, block):
        """
        Validate a new block against certain criteria.

        Args:
            last_block (Block): The last block in the blockchain.
            block (Block): The block to be validated.

        Raises:
            Exception: If the block is not valid.
        """
        if block.last_hash != last_block.hash:
            raise Exception('The last_hash of the block must be correct')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty adjustment must only be by 1')

        if block.hash[:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof of work requirement has not been met')

        currently_constructed_block_hash = cryptographic_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )
        if block.hash != currently_constructed_block_hash:
            raise Exception('The new block hash must be correct')


def main():
    # Example usage in the main function
    genesis_block = Block.genesis()
    new_block = Block.mine_block(genesis_block, 'foo')
    print(new_block)

    genesis_block = Block.genesis()
    new_block = Block.mine_block(genesis_block, 'foo')
    new_block.last_hash = 'incorrect hash'
    try:
        Block.is_a_valid_block(genesis_block, new_block)
    except Exception as e:
        print(f'is_valid_block: {e}')


if __name__ == '__main__':
    main()

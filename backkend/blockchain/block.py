import time
from backkend.config import MINE_RATE
from backkend.utils.cryptographic_hash import cryptographic_hash


"""Caps because its outside the class"""
# GENESIS_DATA = {
#     'timestamp': 'timestamp',
#     'last_hash': 'last_hash',
#     'hash': 'origin_hash',
#     'data': 'data'
# }

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'last_hash',
    'hash': 'origin_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'

}


class Block:
    """
    """

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self) -> str:
        return (
            'Block('
            f'timestamp: {self.timestamp},'
            f'last_hash: {self.last_hash},'
            f'hash: {self.hash},'
            f'data: {self.data},'
            f'data: {self.difficulty},'
            f'data: {self.nonce})'

        )

    def __eq__(self, other):
        """
        This method makes teh dictionary object readable for comparison
         """
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        serialises blockchain into a representation of a dictionary
        """
        return self.__dict__

    @staticmethod
    def deserialise_from_json(block_json):
        return Block(**block_json)

    @staticmethod
    def mine_block(last_block, data):
        """
        mines a block based on a given last block and data, until a block hash is found
        that meets the leading 0's proof of work requirement
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_mine_block_difficulty(last_block,timestamp )
        nonce = 0
        from backkend.utils.cryptographic_hash import cryptographic_hash
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
        # return Block(1, 'genesis_last_hash', 'genesis_hash', [])
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_mine_block_difficulty(last_block, new_timestamp):
        """adjust the difficulty depending on the mine rate in time value
        """
        if(new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        if(last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_a_valid_block(last_block, block):
        """block validation must follow this rules:
        1. the new block must reference  the valid last hash
        2. the new block must meet the proof of work requirement
        3. the hash must be a valid combination of the block's fields
        4. the difficulty adjustment must adjust by 1
        """

        if block.last_hash != last_block.hash:
            raise Exception('the last_hash of the block must be correct')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty adjustment must only be by 1')

        if block.hash[:block.difficulty] != '0'*block.difficulty:
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

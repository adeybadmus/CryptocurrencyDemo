from backkend.blockchain.block import Block


class Blockchain:
    def __init__(self) -> None:  # value set to none
        self.chain = [Block.genesis()]

    def add_a_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self) -> str:  # represent object in blockchain in human readable form
        return f'Blockchain-chain: {self.chain}'

    def replace_chain(self, chain):
        """
        1. Incoming chain must be longer that the current chain
        2. Incoming chain must have a valid format
        """
        if len(chain) >= len(self.chain):
            raise Exception('The incoming chain must be longer than the current chain')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'cannot replace. The incoming chain is not valid: {e}')
        self.chain = chain

    def to_json(self):
        """
        serialises blockchain into a list of blocks
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def deserialise_from_json(blockchain_json):
        blockchain = Blockchain()
        blockchain.chain=list(map(
            lambda block_json: Block.deserialise_from_json()
        ))

        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """this method verifies an incoming chain is valid.
        the rules for validation are the following:
        1. the chain must start with the genesis block.
        2. the blocks must be validated correctly
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be the valid one')
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            block.is_a_valid_block((last_block, block))


blockchain = Blockchain()
blockchain.add_a_block('one')
blockchain.add_a_block('two')

print(blockchain)

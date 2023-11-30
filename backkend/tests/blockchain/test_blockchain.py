import pytest
from backkend.blockchain.block import GENESIS_DATA
from backkend.blockchain.blockchain import Blockchain


def test_the_blockchain_instance():
    """Test the creation of a blockchain instance.

    Checks:
    1. Verifies that the first block in the blockchain is the genesis block.
    """
    blockchain = Blockchain()
    assert blockchain.chain[0].timestamp == GENESIS_DATA['timestamp']


def test_add_a_block():
    """Test the addition of a block to the blockchain.

    Checks:
    1. Verifies that this function adds a block to the blockchain.
    """
    blockchain = Blockchain()
    data1 = 'second block'
    blockchain.add_a_block(data1)
    assert blockchain.chain[-1].data == data1


def test_length_of_blockchain():
    """Test the length of the blockchain.

    Checks:
    1. Verifies that this function adds two blocks to the blockchain.
    2. Verifies the length of the blockchain is 3.
    """
    blockchain = Blockchain()
    data1 = 'second block'
    data2 = 'third block'
    blockchain.add_a_block(data1)
    blockchain.add_a_block(data2)
    assert len(blockchain.chain) == 3


@pytest.fixture
def blockchain_three_blocks():
    """Fixture for a blockchain with three blocks."""
    blockchain = Blockchain()
    for i in range(1, 3):
        blockchain.add_a_block(i)
    return blockchain


def test_is_a_valid_chain(blockchain_three_blocks):
    """Test if a chain is valid.

    Checks:
    1. The function is_valid_chain should not raise any exceptions for a valid chain.
    """
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_is_a_valid_chain_with_bad_genesis_block(blockchain_three_blocks):
    """Test if a chain has a bad genesis block.

    Checks:
    1. The function should raise an exception with a message indicating the genesis block must be valid.
    """
    blockchain_three_blocks.chain[0].hash = 'bad hash'

    with pytest.raises(Exception, match='The genesis block must be the valid one'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_replace_the_chain(blockchain_three_blocks):
    """Test replacing the chain with another chain.

    Checks:
    1. Verifies that the chain is replaced successfully.
    """
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_blocks.chain)
    assert blockchain.chain == blockchain_three_blocks.chain


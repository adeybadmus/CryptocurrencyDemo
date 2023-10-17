import pytest
from backkend.blockchain.block import GENESIS_DATA
from backkend.blockchain.blockchain import Blockchain


def test_the_blockchain_instance():
    # verify first block
    # in the blockchain is the genesis block
    blockchain = Blockchain()
    assert blockchain.chain[0].timestamp == GENESIS_DATA['timestamp']


def test_add_a_block():
    # verify that this function add
    # a block to the block chain
    blockchain = Blockchain()
    data1 = 'second block'
    blockchain.add_a_block(data1)
    assert blockchain.chain[-1].data == data1


def test_length_of_blockchain():
    # verify that this function add
    # a block to the block chain
    blockchain = Blockchain()
    data1 = 'second block'
    data2 = 'third block'
    blockchain.add_a_block(data1)
    blockchain.add_a_block(data2)
    assert len(blockchain.chain) == 3


@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_a_block(i)
    return blockchain


def test_is_a_valid_chain(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks)


def test_is_a_valid_chain_with_bad_genesis_block(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash = 'bad hash'

    with pytest.raises(Exception, match='The genesis block must be the valid one'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)


def test_replace_the_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_blocks.chain)
    assert blockchain.chain == blockchain_three_blocks.chain

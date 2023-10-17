import time

import pytest as pytest

from backkend.blockchain.block import Block, GENESIS_DATA
from backkend.config import MINE_RATE, SECONDS


def test_genesis():
    """ 1. tests the genesis method
        2. checks the created genesis instance is an instance of the Block class
    """
    genesis = Block.genesis()
    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value


def test_mine_block():
    """ 1. tests the mine_block method
        2. checks the created block instance is an instance of the Block class
        3. checking the data
        4. checking the last_hash in new block is that of the genesis block
    """
    last_block = Block.genesis()
    data: str = 'this is a test to verify instance'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash


def test_block_difficulty():
    """ 1. tests the mine_block method
         2. checks the created block instance is an instance of the Block class
         3. checking the data
         4. checking the difficulty of the hash in new block is equal to the difficulty set for the class
     """
    last_block = Block.genesis()
    data = 'this is a test to verify difficulty'
    block = Block.mine_block(last_block, data)
    assert block.hash[0:block.difficulty] == '0' * block.difficulty


def test_mine_rate():
    """ 1. tests the mine_block method
         2. checks the created block instance is an instance of the Block class
         3. checking the data
         4. checking the difficulty of the hash in new block is equal to the difficulty set for the class
     """
    last_block = Block.genesis()
    data = 'this is a test to that difficulty level vary depending on mine rate'
    block = Block.mine_block(last_block, data)
    block_mine_rate = block.timestamp - last_block.timestamp
    assert block_mine_rate >= MINE_RATE


def test_for_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'test_data')
    mined_new_block = Block.mine_block(last_block, 'test_quick_block')
    assert mined_new_block.difficulty == last_block.difficulty + 1


def test_for_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'food')
    time.sleep(MINE_RATE / SECONDS)
    mined_new_block = Block.mine_block(last_block, 'test_slow_block')
    assert mined_new_block.difficulty == last_block.difficulty - 1


def test_mine_block_difficulty_decrement_is_limited_to_one():
    last_block = Block(
        time.time_ns(),
        'last_hash',
        'current_hash',
        'data',
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)
    new_mined_block = Block.mine_block(last_block, 'some data')
    assert new_mined_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis()


@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'some data')


def test_is_a_valid_block(last_block, block):
    Block.is_a_valid_block(last_block, block)


def test_is_a_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'bad last hash'

    with pytest.raises(Exception, match='the last_hash of the block must be correct'):
        Block.is_a_valid_block(last_block, block)


def test_block_validation_difficulty_was_skipped(last_block, block):
    skipped_difficulty = 5
    block.difficulty = skipped_difficulty
    block.hash = f'{"0" * skipped_difficulty}11abijgjj22'

    with pytest.raises(Exception, match='The block difficulty adjustment must only be by 1'):
        Block.is_a_valid_block(last_block, block)


def test_it_is_a_valid_proof_of_work(last_block, block):
    block.difficulty = 4

    with pytest.raises(Exception, match='The proof of work requirement has not been met'):
        Block.is_a_valid_block(last_block, block)


def test_new_block_hash(last_block, block):
    block.hash = '000incorrecthash'

    with pytest.raises(Exception, match='The new block hash must be correct'):
        Block.is_a_valid_block(last_block, block)

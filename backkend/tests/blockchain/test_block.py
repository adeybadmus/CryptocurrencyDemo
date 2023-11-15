import time
import pytest

from backkend.blockchain.block import Block, GENESIS_DATA
from backkend.config import MINE_RATE, SECONDS


def test_genesis():
    """Test the genesis method.

    Checks:
    1. The created genesis instance is an instance of the Block class.
    2. Verify each key-value pair in GENESIS_DATA.
    """
    genesis = Block.genesis()
    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_mine_block():
    """Test the mine_block method.

    Checks:
    1. The created block instance is an instance of the Block class.
    2. The data in the block is correct.
    3. The last_hash in the new block is that of the genesis block.
    """
    last_block = Block.genesis()
    data = 'this is a test to verify instance'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash


def test_block_difficulty():
    """Test the mine_block method and block difficulty.

    Checks:
    1. The created block instance is an instance of the Block class.
    2. The data in the block is correct.
    3. The difficulty of the hash in the new block is equal to the difficulty set for the class.
    """
    last_block = Block.genesis()
    data = 'this is a test to verify difficulty'
    block = Block.mine_block(last_block, data)
    assert block.hash[0:block.difficulty] == '0' * block.difficulty


def test_mine_rate():
    """Test the mine_block method and mine rate.

    Checks:
    1. The created block instance is an instance of the Block class.
    2. The data in the block is correct.
    3. The difficulty of the hash in the new block is equal to the difficulty set for the class.
    4. The mine rate is greater than or equal to MINE_RATE.
    """
    last_block = Block.genesis()
    data = 'this is a test to that difficulty level vary depending on mine rate'
    block = Block.mine_block(last_block, data)
    block_mine_rate = block.timestamp - last_block.timestamp
    assert block_mine_rate >= MINE_RATE


def test_for_quickly_mined_block():
    """Test for quickly mined block.

    Checks:
    The difficulty of the mined new block is one more than the last block.
    """
    last_block = Block.mine_block(Block.genesis(), 'test_data')
    mined_new_block = Block.mine_block(last_block, 'test_quick_block')
    assert mined_new_block.difficulty == last_block.difficulty + 1


def test_for_slowly_mined_block():
    """Test for slowly mined block.

    Checks:
    The difficulty of the mined new block is one less than the last block after sleeping for MINE_RATE / SECONDS.
    """
    last_block = Block.mine_block(Block.genesis(), 'food')
    time.sleep(MINE_RATE / SECONDS)
    mined_new_block = Block.mine_block(last_block, 'test_slow_block')
    assert mined_new_block.difficulty == last_block.difficulty - 1


def test_mine_block_difficulty_decrement_is_limited_to_one():
    """Test that the difficulty decrement is limited to one.

    Checks:
    The difficulty of the new mined block is set to 1 after sleeping for MINE_RATE / SECONDS.
    """
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
    """Test if a block is valid.

    Checks:
    The function is_a_valid_block should not raise any exceptions for a valid block.
    """
    Block.is_a_valid_block(last_block, block)


def test_is_a_valid_block_bad_last_hash(last_block, block):
    """Test if a block has a bad last hash.

    Checks:
    The function should raise an exception with a message indicating the last_hash must be correct.
    """
    block.last_hash = 'bad last hash'

    with pytest.raises(Exception, match='The last_hash of the block must be correct'):
        Block.is_a_valid_block(last_block, block)


def test_block_validation_difficulty_was_skipped(last_block, block):
    """Test if block difficulty adjustment was skipped.

    Checks:
    The function should raise an exception with a message indicating the difficulty adjustment must only be by 1.
    """
    skipped_difficulty = 5
    block.difficulty = skipped_difficulty
    block.hash = f'{"0" * skipped_difficulty}11abijgjj22'

    with pytest.raises(Exception, match='The block difficulty adjustment must only be by 1'):
        Block.is_a_valid_block(last_block, block)


def test_it_is_a_valid_proof_of_work(last_block, block):
    """Test if it is a valid proof of work.

    Checks:
    The function should raise an exception with a message indicating the proof of work requirement has not been met.
    """
    block.difficulty = 4

    with pytest.raises(Exception, match='The proof of work requirement has not been met'):
        Block.is_a_valid_block(last_block, block)


def test_new_block_hash(last_block, block):
    """Test if the new block hash is correct.

    Checks:
    The function should raise an exception with a message indicating the new block hash must be correct.
    """
    block.hash = '000incorrecthash'

    with pytest.raises(Exception, match='The new block hash must be correct'):
        Block.is_a_valid_block(last_block, block)

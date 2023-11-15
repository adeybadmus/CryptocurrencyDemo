import time
import requests
from backkend.wallet.wallet import Wallet

BASE_URL = 'http://localhost:5000'


def get_blockchain():
    """Retrieve the current state of the blockchain."""
    return requests.get(f'{BASE_URL}/blockchain').json()


def get_blockchain_mine_a_block():
    """Mine a new block in the blockchain."""
    return requests.get(f'{BASE_URL}/blockchain/mine').json()


def post_wallet_transaction(receiver, amount):
    """Initiate a transaction from the wallet to the specified receiver with a given amount."""
    return requests.post(
        f'{BASE_URL}/wallet/transact',
        json={'receiver': receiver, 'amount': amount}
    ).json()


def get_wallet_info():
    """Retrieve information about the wallet."""
    return requests.get(f'{BASE_URL}/wallet/info').json()


# Get the initial state of the blockchain
start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')

# Create a wallet and use its address as the recipient
recipient = Wallet().address

# Make a transactions from the wallet to the recipient
post_wallet_transact_1 = post_wallet_transaction(recipient, 21)
print(f'\n post_wallet_transact_1 : {post_wallet_transact_1}')
time.sleep(1)
post_wallet_transact_2 = post_wallet_transaction(recipient, 13)
print(f'\n post_wallet_transact_2 : {post_wallet_transact_2}')
time.sleep(1)

# Mine a new block in the blockchain
mined_block = get_blockchain_mine_a_block()
print(f'\n mined_block : {mined_block}')

# Get information about the wallet
wallet_info = get_wallet_info()
print(f'\n wallet_info: {wallet_info}')

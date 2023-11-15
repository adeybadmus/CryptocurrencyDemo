import os
import requests
from flask import Flask, jsonify, request

import backkend
from backkend.blockchain.blockchain import Blockchain
from backkend.publish_subscribe import PubSub
from backkend.wallet.transaction_pool import TransactionPool
from backkend.wallet.wallet import Wallet
from backkend.wallet.transaction import Transaction

app = Flask(__name__)
blockchain = Blockchain()
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)


@app.route('/')
def default():
    return 'this is MABYs crypto blockchain'


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    # transaction_data.append(Transaction.reward_miner_for_transaction(backkend.wallet.wallet).serialize_to_json())
    blockchain.add_a_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_a_block(block)
    transaction_pool.clear_chain_transactions(blockchain)
    return jsonify(block.to_json())


@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    from backkend.wallet import wallet
    transaction: Transaction = transaction_pool.existing_transaction(wallet.Wallet.address)
    if transaction:
        transaction.update_transaction(backkend.wallet.wallet,
                                       transaction_data['receiver'],
                                       transaction_data['amount']
                                       )
    else:

        transaction = Transaction(
            backkend.wallet.wallet,
            transaction_data['receiver'],
            transaction_data['amount']
        )

        pubsub.broadcast_a_transaction(transaction)
        return jsonify(transaction.serialize_to_json())


@app.route('/wallet/info')
def route_wallet_info():
    wallet = Wallet()
    """
     this returns a json response that contains the wallet address and its balance.
     It accurately reflects teh amount in the wallet
    """
    return jsonify({'address': wallet.address, 'balance': wallet.balance})


PORT = 5000

if os.environ.get("PER") == "True":
    result = requests.get("http://127.0.0.1:{PORT}/blockchain")
    expected_blockchain_result = Blockchain.deserialise_from_json(result.json())

    try:
        blockchain.replace_chain(expected_blockchain_result)
        print('\n -- The local chain was successfully synchronised')
    except Exception as e:
        print(f'\n There was an error synchronising: {e}')

app.run(port=PORT)

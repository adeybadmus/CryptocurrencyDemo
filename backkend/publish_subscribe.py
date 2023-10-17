from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time
from backkend.blockchain.block import Block
from backkend.wallet.transaction import Transaction
from backkend.wallet.transaction_pool import TransactionPool

pubnubConfig = PNConfiguration()
pubnubConfig.subscribe_key = 'sub-c-597c880d-fdcc-4331-a490-ad845fae3516'
pubnubConfig.publish_key = 'pub-c-ef79c7dd-2005-408a-a877-5461c7f235e6'

CHANNELS = {
    'START': 'START',
    'BLOCK': 'BLOCK',
    'TRANSACTION' : 'TRANSACTION'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.transaction_pool = transaction_pool
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f'n --our incoming message: {message_object}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.deserialise_from_json(message_object.message)
            future_chain = self.blockchain.chain[:]
            future_chain.append(block)

            try:
                self.blockchain.replace_chain(future_chain)
                self.transaction_pool.clear_chain_transactions(
                    self.blockchain
                )
                print('\n -- The local chain was replaced successfully')
            except Exception as e:
                print(f'\n -- The local chain was not replaced: {e}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.deserilize_from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool')


class PubSub():
    """This class enables communication between nodes of upskill blockchain network
    """

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pubnubConfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """Deals with publishing of messages into our channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_a_block(self, block):
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_a_transaction(self, transaction):
        self.publish(CHANNELS['TRANSACTION'], transaction.serialize_to_json())


def main():
    publish_subscribe = PubSub()
    time.sleep(1)
    publish_subscribe.publish(CHANNELS['BLOCK'], {'test': 'test_data'})


if __name__ == '__main__':
    main()

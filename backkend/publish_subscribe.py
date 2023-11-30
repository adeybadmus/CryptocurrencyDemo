from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time
from backkend.blockchain.block import Block
from backkend.blockchain.blockchain import Blockchain
from backkend.wallet.transaction import Transaction
from backkend.wallet.transaction_pool import TransactionPool

# PubNub configuration
pubnubConfig = PNConfiguration()
pubnubConfig.subscribe_key = 'yout subscribe_key'
pubnubConfig.publish_key = ' your publish_key'

# Channels for communication
CHANNELS = {
    'START': 'START',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback):
    """Listener class to handle incoming messages on subscribed channels.
    """

    def __init__(self, blockchain, transaction_pool):
        self.transaction_pool = transaction_pool
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        """Handle incoming messages on subscribed channels.

        Args:
            pubnub: PubNub instance.
            message_object: Message received from the channel.
        """
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


class PubSub:
    """This class enables communication between nodes of upskill blockchain network.
    """

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pubnubConfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """Publish messages into the specified channel.

        Args:
            channel (str): Channel to publish the message.
            message (dict): Message to be published.
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_a_block(self, block):
        """Broadcast a block to the BLOCK channel.

        Args:
            block (Block): Block to be broadcasted.
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_a_transaction(self, transaction):
        """Broadcast a transaction to the TRANSACTION channel.

        Args:
            transaction (Transaction): Transaction to be broadcasted.
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.serialize_to_json())


def main():
    """Example usage of the PubSub class to publish a block message.
    """
    blockchain = Blockchain()
    transaction_pool = TransactionPool()
    pubsub = PubSub(blockchain, transaction_pool)
    channel_to_publish = CHANNELS['BLOCK']
    message_to_publish = {'data': 'test_data'}
    time.sleep(1)
    pubsub.publish(channel_to_publish, message_to_publish)


if __name__ == '__main__':
    main()

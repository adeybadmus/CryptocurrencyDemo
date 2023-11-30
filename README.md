# CryptocurrencyDemo project

## Overview
This project is a simple implementation of a blockchain-based cryptocurrency system. The implementation covers key components such as blockchain blocks, the blockchain itself, cryptographic hash functions, and integration with the PubNub messaging service for communication between nodes in the network.

## Project Structure
The project is organized into several modules:

### Blockchain Components:

blockchain/block.py: Defines the Block class representing individual blocks in the blockchain.

blockchain/blockchain.py: Implements the Blockchain class that manages the chain of blocks.

blockchain/genesis_data.py: Contains data for the genesis block.
### Cryptographic Functions:

backend/utils/cryptographic_hash.py: Provides a cryptographic hash function.

backend/utils/hex_to_binary.py: Implements a function for converting hexadecimal to binary.
### Wallet Components:

backend/wallet/transaction.py: Defines the Transaction class representing transactions.

backend/wallet/transaction_pool.py: Manages the pool of transactions.
### PubSub Integration:

pubsub/pubsub.py: Implements the PubSub class for communication between nodes.
pubsub/listener.py: Defines the Listener class for handling incoming PubNub messages.
### Main Execution:

main.py: Contains the main execution script, initializing the blockchain, transaction pool, and PubSub.
### Testing:

tests/: Directory containing test scripts for various components.


## Getting Started
### Dependencies:

Ensure you have the required dependencies installed. You can install them using the provided requirements.txt file:

pip install -r requirements.txt


### Run the Project:

Execute the main.py script to run the cryptocurrency system:

python -m backkend.app

### Run Tests:

Execute the test scripts in the tests/ directory to ensure the correctness of the implemented components:
pytest tests/


### Test Plan
Refer to the provided test plan in the project documentation (test_artefacts/CryptocurrencyDemo_Test Plan) 
for detailed information on test scenarios and strategies.


### PubNub Configuration
Ensure that you have a valid PubNub account and replace the placeholder keys in the pubnubConfig configuration in 
wallet/publish_subscribe.py with your own PubNub subscribe and publish keys.

'pubnubConfig.subscribe_key = 'your subscribe_key'

pubnubConfig.publish_key = ' your publish_key'


### Contributions
Contributions to the project are welcome. If you encounter any issues or have suggestions for improvements, 
please open an issue or submit a pull request.

### License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the code.
from backkend.blockchain.blockchain import Blockchain
import time
from backkend.config import SECONDS

"""
This code generates a blockchain with 1000 blocks, measuring the time it takes to mine each block and 
printing information about the mined block, including its difficulty level and the time taken. 

The average time to mine blocks is also calculated and printed.
"""

# Create a new instance of the Blockchain
blockchain = Blockchain()

# List to store the time taken to mine each block
times = []

# Generate 1000 blocks and measure the time taken for each
for i in range(1000):
    # Record the start time for mining the block
    start_time = time.time_ns()

    # Add a new block to the blockchain
    blockchain.add_a_block(i)

    # Record the end time after mining the block
    end_time = time.time_ns()

    # Calculate the time taken to mine the block in seconds
    time_to_mine = (end_time - start_time) / SECONDS

    # Append the time taken to the list
    times.append(time_to_mine)

    # Calculate the average time to mine blocks
    average_time_to_mine = sum(times) / len(times)

    # Print information about the mined block and time taken
    print(f'New block difficulty: {blockchain.chain[-1].difficulty}')
    print(f'Time taken to mine block {i}: {time_to_mine}s')
    print(f'Average time to add blocks: {average_time_to_mine}s')

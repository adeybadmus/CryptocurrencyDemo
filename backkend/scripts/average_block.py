from backkend.blockchain.blockchain import Blockchain
import time

from backkend.config import SECONDS

blockchain = Blockchain()
times = []

for i in range(1000):
    start_time = time.time_ns()
    blockchain.add_a_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time)/SECONDS
    times.append(time_to_mine)

    average_time_to_mine = sum(times)/len(times)
    print(f'new block difficulty: {blockchain.chain[-1].difficulty}')
    print(f'Time taken to mine clock: {time_to_mine}s')
    print(f'Average time to add blocks: {average_time_to_mine}s')
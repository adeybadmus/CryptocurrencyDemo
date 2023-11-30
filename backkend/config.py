"""
This module defines constants related to time intervals and blockchain parameters.

NANOSECONDS: Constant representing one nanosecond.
MICROSECONDS: Constant representing one microsecond, equivalent to 1000 nanoseconds.
MILLISECONDS: Constant representing one millisecond, equivalent to 1000 microseconds.
SECONDS: Constant representing one second, equivalent to 1000 milliseconds.

MINE_RATE: The time interval (in seconds) defining the target time to mine a new block.
           In this case, it's set to 4 seconds.

STARTING_BALANCE: The initial balance assigned to a wallet when created.

MINING_REWARD: Placeholder for the mining reward value. Uncomment and assign a value when defined.
MINING_REWARD_INPUT: Placeholder for the mining reward input. Uncomment and assign a value when defined.
"""
NANOSECONDS = 1
MICROSECONDS = 1000 * NANOSECONDS
MILLISECONDS = 1000 * MICROSECONDS
SECONDS = 1000 * MILLISECONDS

MINE_RATE = 4 * SECONDS
STARTING_BALANCE = 1000
# MINING_REWARD =
# MINING_REWARD_INPUT =

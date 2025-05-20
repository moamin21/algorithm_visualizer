import time  # Import the time module to measure execution time
from typing import List, Tuple  # Import type hints for better code documentation

class CoinChange:
    """
    Implementation of the Coin Change problem with greedy and dynamic programming approaches
    """
    
    def __init__(self):
        self.reset()  # Initialize the object by calling the reset method
    
    def reset(self):
        """Reset all metrics and states"""
        self.operations = 0  # Counter for number of operations performed
        self.execution_time = 0  # Tracker for execution time
        self.steps = []  # List to store computation steps for visualization
    
    def greedy_coin_change(self, coins: List[int], amount: int) -> Tuple[int, List[int]]:
        """
        Solves the coin change problem using a greedy approach:
        - Choose the largest denomination coin that fits
        - Repeat until target amount is reached
        
        Returns (num_coins, selected_coins)
        
        Note: This does NOT always give optimal solution, but works for US coin denominations
        """
        self.reset()  # Reset all metrics before starting the algorithm
        result = []  # Initialize list to store selected coins
        
        # Sort coins in descending order
        sorted_coins = sorted(coins, reverse=True)  # Sort coins from largest to smallest
        self.steps.append(("init", sorted_coins.copy(), amount))  # Record initial state
        
        start_time = time.time()  # Record the start time
        
        remaining = amount  # Initialize the remaining amount to calculate
        for coin in sorted_coins:  # Iterate through coins in descending order
            # Take as many of this coin as possible
            count = remaining // coin  # Calculate how many of this coin can be used
            self.operations += 1  # Count each coin type consideration as an operation
            
            if count > 0:  # If we can use at least one of this coin
                # Add these coins to result
                result.extend([coin] * count)  # Add 'count' instances of this coin to the result
                remaining -= coin * count  # Reduce the remaining amount
                self.steps.append(("take", coin, count, remaining))  # Record coin selection
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        if remaining == 0:  # If we were able to make exact change
            return len(result), result  # Return number of coins and the coins list
        else:
            # Cannot make exact change
            return -1, []  # Return -1 to indicate no solution found
    
    def dp_coin_change(self, coins: List[int], amount: int) -> Tuple[int, List[int]]:
        """
        Solves the coin change problem using dynamic programming:
        - Find minimum number of coins to make amount
        - Always finds optimal solution
        
        Returns (num_coins, selected_coins)
        """
        self.reset()  # Reset all metrics before starting the algorithm
        
        # Initialize dp array to store minimum coins needed for each amount
        dp = [float('inf')] * (amount + 1)  # Initialize with infinity (unreachable)
        dp[0] = 0  # Base case: 0 coins needed to make amount 0
        
        # Store the last coin used to reach each amount (for backtracking)
        last_coin = [0] * (amount + 1)  # Track which coin was used for each amount
        
        self.steps.append(("init", dp.copy(), amount))  # Record initial state
        
        start_time = time.time()  # Record the start time
        
        # Fill the dp array
        for i in range(1, amount + 1):  # For each amount from 1 to target
            for coin in coins:  # Try each coin
                self.operations += 1  # Count each coin consideration as an operation
                
                if coin <= i and dp[i - coin] + 1 < dp[i]:  # If coin fits and gives better solution
                    dp[i] = dp[i - coin] + 1  # Update with better solution
                    last_coin[i] = coin  # Record which coin was used
                    self.steps.append(("update", i, coin, dp[i]))  # Record the update
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # No solution exists
        if dp[amount] == float('inf'):  # If we couldn't reach the target amount
            return -1, []  # Return -1 to indicate no solution found
        
        # Backtrack to find the coins used
        result = []  # Initialize list to store selected coins
        remaining = amount  # Start with the full amount
        while remaining > 0:  # Continue until all amount is accounted for
            coin = last_coin[remaining]  # Get the coin used for this amount
            result.append(coin)  # Add the coin to result
            remaining -= coin  # Reduce the remaining amount
            self.steps.append(("backtrack", coin, remaining))  # Record the backtracking step
        
        return dp[amount], result  # Return minimum number of coins and the coins list
    
    def compare_approaches(self, coins: List[int], amount: int) -> dict:
        """Compare greedy and DP approaches for coin change problem"""
        # Run greedy approach
        greedy_count, greedy_coins = self.greedy_coin_change(coins, amount)  # Get results from greedy approach
        greedy_metrics = {  # Store metrics from greedy approach
            "operations": self.operations,
            "execution_time": self.execution_time,
            "steps": self.steps.copy()
        }
        
        # Run DP approach
        dp_count, dp_coins = self.dp_coin_change(coins, amount)  # Get results from DP approach
        dp_metrics = {  # Store metrics from DP approach
            "operations": self.operations,
            "execution_time": self.execution_time,
            "steps": self.steps.copy()
        }
        
        return {  # Return results and metrics from both approaches
            "greedy": {
                "count": greedy_count,
                "coins": greedy_coins,
                "metrics": greedy_metrics
            },
            "dp": {
                "count": dp_count,
                "coins": dp_coins,
                "metrics": dp_metrics
            }
        }
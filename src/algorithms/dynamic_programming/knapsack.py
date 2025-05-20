import time  # Import the time module to measure execution time
from typing import List, Tuple, Dict  # Import type hints for better code documentation

class Knapsack:
    """
    Implementation of the 0/1 Knapsack Problem with visualization support
    """
    
    def __init__(self):
        self.reset()  # Initialize the object by calling the reset method
    
    def reset(self):
        """Reset all metrics and states"""
        self.operations = 0  # Counter for number of operations performed
        self.execution_time = 0  # Tracker for execution time
        self.space_used = 0  # Tracker for memory usage
        self.steps = []  # List to store computation steps for visualization
    
    def solve_knapsack(self, weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
        """
        Solve the 0/1 knapsack problem using dynamic programming (tabulation)
        Returns the maximum value and the list of items selected
        """
        self.reset()  # Reset all metrics before starting the algorithm
        n = len(weights)  # Get the number of items
        
        # Initialize the DP table
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]  # Create a (n+1) x (capacity+1) table filled with zeros
        self.space_used = (n + 1) * (capacity + 1)  # Calculate space used by the DP table
        
        # Record initial state
        self.steps.append(("init", dp))  # Save the initial state of the DP table
        
        start_time = time.time()  # Record the start time
        
        # Fill the DP table
        for i in range(1, n + 1):  # For each item (1-indexed)
            for w in range(capacity + 1):  # For each possible capacity
                self.operations += 1  # Count each cell calculation as an operation
                
                # If current item weight is <= current capacity
                if weights[i-1] <= w:  # Check if current item can fit (using 0-indexed weights)
                    # Max of: (1) including the item, (2) excluding the item
                    include_value = values[i-1] + dp[i-1][w - weights[i-1]]  # Value when including the item
                    exclude_value = dp[i-1][w]  # Value when excluding the item
                    
                    # Choose the better option
                    dp[i][w] = max(include_value, exclude_value)  # Take the maximum value
                    
                    # Record the decision
                    decision = "include" if include_value > exclude_value else "exclude"  # Determine if item was included
                    self.steps.append(("fill", i, w, dp, decision, include_value, exclude_value))  # Record step details
                else:
                    # If item is too heavy, we can't include it
                    dp[i][w] = dp[i-1][w]  # Use the value without this item
                    self.steps.append(("fill", i, w, dp, "too_heavy", 0, dp[i-1][w]))  # Record that item was too heavy
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Backtrack to find which items were selected
        selected_items = []  # Initialize list to store selected items
        w = capacity  # Start with full capacity
        
        for i in range(n, 0, -1):  # Iterate through items backwards
            if dp[i][w] != dp[i-1][w]:  # If value changed, this item was included
                selected_items.append(i-1)  # Add item index (0-indexed) to selected items
                w -= weights[i-1]  # Reduce remaining capacity
                self.steps.append(("backtrack", i-1, True))  # Record that item was selected
            else:
                self.steps.append(("backtrack", i-1, False))  # Record that item was not selected
        
        # Reverse to get items in original order
        selected_items.reverse()  # Reverse list to get items in original order
        
        return dp[n][capacity], selected_items  # Return maximum value and selected items
    
    def solve_fractional_knapsack(self, weights: List[int], values: List[int], capacity: int) -> Tuple[float, List[Tuple[int, float]]]:
        """
        Solve the fractional knapsack problem using a greedy approach
        Returns the maximum value and the list of items with fractions
        """
        self.reset()  # Reset all metrics before starting the algorithm
        n = len(weights)  # Get the number of items
        
        # Calculate value/weight ratio for each item
        items = [(i, values[i] / weights[i], values[i], weights[i]) for i in range(n)]  # Create tuples with (index, value/weight ratio, value, weight)
        
        # Sort items by value/weight ratio in descending order
        items.sort(key=lambda x: x[1], reverse=True)  # Sort by value/weight ratio (highest first)
        
        self.steps.append(("init", items))  # Record initial sorted items
        
        start_time = time.time()  # Record the start time
        
        total_value = 0  # Initialize total value
        selected_items = []  # Initialize list to store selected items and their fractions
        remaining_capacity = capacity  # Start with full capacity
        
        for i, ratio, value, weight in items:  # Process items in order of value/weight ratio
            self.operations += 1  # Count each item consideration as an operation
            
            if remaining_capacity >= weight:  # If we can take the whole item
                # Take the whole item
                selected_items.append((i, 1.0))  # Add item index and fraction (100%)
                total_value += value  # Add full item value
                remaining_capacity -= weight  # Reduce remaining capacity
                self.steps.append(("take", i, 1.0, value, remaining_capacity))  # Record taking whole item
            else:
                if remaining_capacity > 0:  # If we have some capacity left
                    # Take a fraction of the item
                    fraction = remaining_capacity / weight  # Calculate the fraction we can take
                    selected_items.append((i, fraction))  # Add item index and fraction
                    total_value += value * fraction  # Add fractional value
                    remaining_capacity = 0  # No capacity left
                    self.steps.append(("take_fraction", i, fraction, value * fraction, remaining_capacity))  # Record taking fraction
                break  # No more capacity left, so stop
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        self.space_used = n  # Space used is proportional to number of items
        
        return total_value, selected_items  # Return maximum value and selected items with fractions
    
    def compare_knapsack_methods(self, weights: List[int], values: List[int], capacity: int) -> Dict:
        """Compare 0/1 and fractional knapsack methods"""
        # 0/1 Knapsack
        zeroone_value, zeroone_items = self.solve_knapsack(weights, values, capacity)  # Solve using 0/1 method
        zeroone_metrics = {  # Store metrics from 0/1 method
            "operations": self.operations,
            "execution_time": self.execution_time,
            "space_used": self.space_used,
            "steps": self.steps.copy()
        }
        
        # Fractional Knapsack
        frac_value, frac_items = self.solve_fractional_knapsack(weights, values, capacity)  # Solve using fractional method
        frac_metrics = {  # Store metrics from fractional method
            "operations": self.operations,
            "execution_time": self.execution_time,
            "space_used": self.space_used,
            "steps": self.steps.copy()
        }
        
        return {  # Return results and metrics from both methods
            "0/1": {
                "value": zeroone_value,
                "items": zeroone_items,
                "metrics": zeroone_metrics
            },
            "fractional": {
                "value": frac_value,
                "items": frac_items,
                "metrics": frac_metrics
            }
        }
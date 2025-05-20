import time  # Import the time module to measure execution time
from typing import Dict, List, Tuple  # Import typing annotations for better code documentation

class Fibonacci:
    """Fibonacci sequence calculation with visualization support"""
    
    def __init__(self):
        self.reset()  # Initialize the object by calling the reset method
    
    def reset(self):
        """Reset all metrics and states"""
        self.operations = 0  # Counter for number of operations performed
        self.execution_time = 0  # Tracker for the execution time
        self.space_used = 0  # Tracker for memory usage
        self.steps = []  # List to store computation steps for visualization
    
    def fibonacci_recursive(self, n: int) -> int:
        """Calculate the nth Fibonacci number using recursion with memoization"""
        self.reset()  # Reset all metrics before calculation
        memo = {}  # Initialize memoization dictionary to store computed values
        self.steps.append(("init", memo.copy()))  # Record initialization step
        
        start_time = time.time()  # Record the start time
        result = self._fibonacci_memo(n, memo)  # Call the helper method to calculate Fibonacci number
        self.execution_time = time.time() - start_time  # Calculate execution time
        
        # Space used is the size of the memoization table
        self.space_used = len(memo)  # Record the space used by counting entries in memo dict
        
        return result  # Return the calculated Fibonacci number
    
    def _fibonacci_memo(self, n: int, memo: Dict[int, int]) -> int:
        """Helper method for memoized Fibonacci calculation"""
        # Base cases
        if n <= 0:
            return 0  # First base case: F(0) = 0
        if n == 1:
            return 1  # Second base case: F(1) = 1
        
        # Check if already computed
        if n in memo:
            self.operations += 1  # Count memo lookup as an operation
            self.steps.append(("memo_hit", n, memo.copy()))  # Record the memoization hit
            return memo[n]  # Return the previously computed value
        
        # Recursive calculation
        self.operations += 1  # Count this calculation as an operation
        memo[n] = self._fibonacci_memo(n-1, memo) + self._fibonacci_memo(n-2, memo)  # Calculate F(n) by recursion with memoization
        self.steps.append(("memo_calc", n, memo.copy()))  # Record the calculation step
        
        return memo[n]  # Return the calculated value
    
    def fibonacci_tabulation(self, n: int) -> int:
        """Calculate the nth Fibonacci number using tabulation (bottom-up DP)"""
        self.reset()  # Reset all metrics before calculation
        
        if n <= 0:
            return 0  # Handle the case for n <= 0
        
        # Initialize table
        table = [0] * (n + 1)  # Create a table of size n+1 initialized with zeros
        if n >= 1:
            table[1] = 1  # Set F(1) = 1 if n is at least 1
        
        self.steps.append(("init_table", table.copy()))  # Record table initialization
        
        start_time = time.time()  # Record the start time
        
        # Fill the table bottom-up
        for i in range(2, n + 1):  # Iterate from 2 to n
            self.operations += 1  # Count each iteration as an operation
            table[i] = table[i-1] + table[i-2]  # Calculate F(i) using F(i-1) and F(i-2)
            self.steps.append(("table_calc", i, table.copy()))  # Record each step
        
        self.execution_time = time.time() - start_time  # Calculate execution time
        
        # Space used is the size of the table
        self.space_used = len(table)  # Record the space used by counting entries in the table
        
        return table[n]  # Return the final Fibonacci number
    
    def compare_methods(self, n: int) -> Tuple[int, Dict]:
        """Compare both methods and return performance metrics"""
        # Run recursive with memoization
        memo_result = self.fibonacci_recursive(n)  # Calculate using memoization
        memo_metrics = {  # Store metrics from memoization method
            "operations": self.operations,
            "execution_time": self.execution_time,
            "space_used": self.space_used,
            "steps": self.steps.copy()
        }
        
        # Run tabulation
        tab_result = self.fibonacci_tabulation(n)  # Calculate using tabulation
        tab_metrics = {  # Store metrics from tabulation method
            "operations": self.operations,
            "execution_time": self.execution_time,
            "space_used": self.space_used,
            "steps": self.steps.copy()
        }
        
        # Verify both methods give same result
        assert memo_result == tab_result, "Different results from the two methods!"  # Check results match
        
        return memo_result, {  # Return the result and performance metrics
            "memoization": memo_metrics,
            "tabulation": tab_metrics
        }
import time  # Import the time module to measure execution time
from typing import List, Any  # Import type hints for better code documentation

class BinarySearch:
    """Binary search implementation with visualization"""

    def __init__(self):
        self.steps = []  # Initialize empty list to store search steps for visualization
        self.comparisons = 0  # Counter for the number of comparisons made
        self.execution_time = 0  # Tracker for execution time

    def search(self, arr: List[Any], target: Any) -> int:
        self.steps = []  # Reset steps list before starting a new search
        self.comparisons = 0  # Reset comparison counter
        start_time = time.time()  # Record the start time
        result = self._binary_search(arr, target, 0, len(arr) - 1)  # Call the recursive binary search function
        self.execution_time = time.time() - start_time  # Calculate total execution time
        return result  # Return the search result (index or -1)

    def _binary_search(self, arr: List[Any], target: Any, left: int, right: int) -> int:
        self.steps.append(("search", left, right, arr.copy()))  # Record current search range
        if left > right:  # Base case: no elements left to search
            return -1  # Target not found in array
        mid = (left + right) // 2  # Calculate middle index
        self.comparisons += 1  # Increment comparison counter
        if arr[mid] == target:  # Check if middle element is the target
            self.steps.append(("found", mid, -1, arr.copy()))  # Record that target was found
            return mid  # Return index where target was found
        elif arr[mid] > target:  # If middle element is greater than target
            self.steps.append(("left", left, mid - 1, arr.copy()))  # Record searching left half
            return self._binary_search(arr, target, left, mid - 1)  # Recursively search left half
        else:  # If middle element is less than target
            self.steps.append(("right", mid + 1, right, arr.copy()))  # Record searching right half
            return self._binary_search(arr, target, mid + 1, right)  # Recursively search right half
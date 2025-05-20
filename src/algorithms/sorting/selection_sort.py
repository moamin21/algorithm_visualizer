from typing import List, Any  # Import type hints for better code documentation
import time  # Import the time module to measure execution time
from .sort_base import SortAlgorithm  # Import the base class for sorting algorithms

class SelectionSort(SortAlgorithm):
    """Implementation of Selection Sort algorithm"""
    
    def __init__(self):
        super().__init__("Selection Sort")  # Initialize the parent class with the name "Selection Sort"
    
    def sort(self, arr: List[Any]) -> List[Any]:
        """
        Sorts an array using Selection Sort algorithm
        Returns a new sorted array without modifying the original
        """
        self.reset_metrics()  # Reset all metrics before starting the algorithm
        n = len(arr)  # Get the length of the input array
        result = arr.copy()  # Create a copy of the input array to avoid modifying the original
        
        # Record initial state
        self.steps.append(("initial", -1, -1, result.copy()))  # Save the initial state of the array
        
        start_time = time.time()  # Record the start time
        
        for i in range(n):  # For each position in the array
            # Find the minimum element in the unsorted portion
            min_idx = i  # Assume the first unsorted element is the minimum
            for j in range(i + 1, n):  # Check all remaining unsorted elements
                if self.compare(result[min_idx], result[j]):  # If current minimum is greater than element at j
                    min_idx = j  # Update minimum index
            
            # Swap the minimum element with the first element of unsorted portion
            if min_idx != i:  # Only swap if minimum is not already at the correct position
                self.swap(result, i, min_idx)  # Swap elements (this method also records the swap)
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final state
        self.steps.append(("final", -1, -1, result.copy()))  # Save the final sorted state of the array
        
        return result  # Return the sorted array
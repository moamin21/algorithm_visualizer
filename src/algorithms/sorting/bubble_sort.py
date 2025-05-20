from typing import List, Any  # Import type hints for better code documentation
import time  # Import the time module to measure execution time
from .sort_base import SortAlgorithm  # Import the base class for sorting algorithms

class BubbleSort(SortAlgorithm):
    """Implementation of Bubble Sort algorithm"""
    
    def __init__(self):
        super().__init__("Bubble Sort")  # Initialize the parent class with the name "Bubble Sort"
    
    def sort(self, arr: List[Any]) -> List[Any]:
        """
        Sorts an array using Bubble Sort algorithm
        Returns a new sorted array without modifying the original
        """
        self.reset_metrics()  # Reset all metrics before starting the algorithm
        n = len(arr)  # Get the length of the input array
        result = arr.copy()  # Create a copy of the input array to avoid modifying the original
        
        # Record initial state
        self.steps.append(("initial", -1, -1, result.copy()))  # Save the initial state of the array
        
        start_time = time.time()  # Record the start time
        
        for i in range(n):  # Outer loop: iterate n times (worst case)
            # Flag to optimize if no swaps occur in a pass
            swapped = False  # Initialize flag to track if any swaps occurred in this pass
            
            for j in range(0, n - i - 1):  # Inner loop: iterate through unsorted portion of array
                # Compare adjacent elements
                if self.compare(result[j], result[j + 1]):  # Compare current element with next element
                    # Swap them if they are in wrong order
                    self.swap(result, j, j + 1)  # Swap the elements (this method also records the swap)
                    swapped = True  # Set flag to indicate a swap occurred
            
            # If no swapping occurred in this pass, array is sorted
            if not swapped:  # Check if any swaps occurred in this pass
                break  # If no swaps, the array is already sorted, so exit early
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final state
        self.steps.append(("final", -1, -1, result.copy()))  # Save the final sorted state of the array
        
        return result  # Return the sorted array
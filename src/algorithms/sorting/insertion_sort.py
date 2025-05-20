from typing import List, Any  # Import type hints for better code documentation
import time  # Import the time module to measure execution time
from .sort_base import SortAlgorithm  # Import the base class for sorting algorithms

class InsertionSort(SortAlgorithm):
    """Implementation of Insertion Sort algorithm"""
    
    def __init__(self):
        super().__init__("Insertion Sort")  # Initialize the parent class with the name "Insertion Sort"
    
    def sort(self, arr: List[Any]) -> List[Any]:
        self.reset_metrics()  # Reset all metrics before starting the algorithm
        n = len(arr)  # Get the length of the input array
        result = arr.copy()  # Create a copy of the input array to avoid modifying the original
        
        # Record initial state
        self.steps.append(("initial", -1, -1, result.copy()))  # Save the initial state of the array
        
        start_time = time.time()  # Record the start time
        
        for i in range(1, n):  # Start from the second element (index 1) and process each element
            key = result[i]  # Store the current element as the key to be inserted
            self.assignments += 1  # Count assignment operation for storing key
            
            # Move elements greater than key one position ahead
            j = i - 1  # Start comparing with the element before the key
            while j >= 0 and self.compare(result[j], key):  # While previous elements are greater than key
                self.assign(result, j + 1, result[j])  # Shift element one position forward
                j -= 1  # Move to the previous element
                
            # Place key in its correct position
            if j + 1 != i:  # Only count if the key was actually moved (not already in place)
                self.assign(result, j + 1, key)  # Insert the key in its correct position
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final state
        self.steps.append(("final", -1, -1, result.copy()))  # Save the final sorted state of the array
        
        return result  # Return the sorted array
from typing import List, Any  # Import type hints for better code documentation
import time  # Import the time module to measure execution time
from .sort_base import SortAlgorithm  # Import the base class for sorting algorithms

class QuickSort(SortAlgorithm):
    """Implementation of Quick Sort algorithm"""
    
    def __init__(self):
        super().__init__("Quick Sort")  # Initialize the parent class with the name "Quick Sort"
    
    def sort(self, arr: List[Any]) -> List[Any]:
        self.reset_metrics()  # Reset all metrics before starting the algorithm
        result = arr.copy()  # Create a copy of the input array to avoid modifying the original
        
        # Record initial state
        self.steps.append(("initial", -1, -1, result.copy()))  # Save the initial state of the array
        
        start_time = time.time()  # Record the start time
        
        self._quick_sort(result, 0, len(result) - 1)  # Call the recursive quick sort function on the entire array
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final state
        self.steps.append(("final", -1, -1, result.copy()))  # Save the final sorted state of the array
        
        return result  # Return the sorted array
    
    def _quick_sort(self, arr: List[Any], low: int, high: int):
        """Recursive quick sort implementation"""
        if low < high:  # Continue only if there are at least 2 elements
            # Partition the array
            pi = self._partition(arr, low, high)  # Get the partition index where pivot is placed in its final position
            
            # Sort elements before and after partition
            self._quick_sort(arr, low, pi - 1)  # Recursively sort elements before pivot
            self._quick_sort(arr, pi + 1, high)  # Recursively sort elements after pivot
    
    def _partition(self, arr: List[Any], low: int, high: int) -> int:
        """Partition the array and return the partition index"""
        # Choose the rightmost element as pivot
        pivot = arr[high]  # Select the last element as pivot
        self.assignments += 1  # Count assignment operation for storing pivot
        
        # Index of smaller element
        i = low - 1  # Initialize index of smaller element
        
        for j in range(low, high):  # Iterate through elements from low to high-1
            # If current element is smaller than or equal to pivot
            if not self.compare(arr[j], pivot):  # If arr[j] <= pivot
                # Increment index of smaller element
                i += 1  # Move to the next position for smaller element
                self.swap(arr, i, j)  # Swap current element with the element at index i
        
        # Place pivot in correct position
        self.swap(arr, i + 1, high)  # Swap pivot (at high) with element at i+1
        
        # Add a step for visualization
        self.steps.append(("partition", low, high, arr.copy()))  # Record the partition operation
        
        return i + 1  # Return the partition index (position of pivot after partitioning)
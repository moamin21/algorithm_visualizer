from typing import List, Any  # Import type hints for better code documentation
import time  # Import the time module to measure execution time
from .sort_base import SortAlgorithm  # Import the base class for sorting algorithms

class MergeSort(SortAlgorithm):
    """Implementation of Merge Sort algorithm"""
    
    def __init__(self):
        super().__init__("Merge Sort")  # Initialize the parent class with the name "Merge Sort"
    
    def sort(self, arr: List[Any]) -> List[Any]:
        self.reset_metrics()  # Reset all metrics before starting the algorithm
        result = arr.copy()  # Create a copy of the input array to avoid modifying the original
        
        # Record initial state
        self.steps.append(("initial", -1, -1, result.copy()))  # Save the initial state of the array
        
        start_time = time.time()  # Record the start time
        
        self._merge_sort(result, 0, len(result) - 1)  # Call the recursive merge sort function on the entire array
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final state
        self.steps.append(("final", -1, -1, result.copy()))  # Save the final sorted state of the array
        
        return result  # Return the sorted array
    
    def _merge_sort(self, arr: List[Any], left: int, right: int):
        """Recursive merge sort implementation"""
        if left < right:  # Continue only if there are at least 2 elements
            # Find middle point
            mid = (left + right) // 2  # Calculate the middle index
            
            # Sort first and second halves
            self._merge_sort(arr, left, mid)  # Recursively sort the left half
            self._merge_sort(arr, mid + 1, right)  # Recursively sort the right half
            
            # Merge the sorted halves
            self._merge(arr, left, mid, right)  # Merge the two sorted halves
    
    def _merge(self, arr: List[Any], left: int, mid: int, right: int):
        """Merge two subarrays of arr[]"""
        # Create temporary arrays
        L = arr[left:mid + 1]  # Create a copy of the left subarray
        R = arr[mid + 1:right + 1]  # Create a copy of the right subarray
        
        # Initial indexes
        i = j = 0  # Initialize indices for the two subarrays
        k = left  # Initialize index for the merged array
        
        # Merge temp arrays back into arr[left..right]
        while i < len(L) and j < len(R):  # Continue until we've processed all elements in one subarray
            if not self.compare(L[i], R[j]):  # If L[i] <= R[j]
                self.assign(arr, k, L[i])  # Place L[i] in the merged array
                i += 1  # Move to next element in left subarray
            else:
                self.assign(arr, k, R[j])  # Place R[j] in the merged array
                j += 1  # Move to next element in right subarray
            k += 1  # Move to next position in merged array
        
        # Copy remaining elements of L[], if any
        while i < len(L):  # If there are remaining elements in left subarray
            self.assign(arr, k, L[i])  # Copy element to merged array
            i += 1  # Move to next element in left subarray
            k += 1  # Move to next position in merged array
        
        # Copy remaining elements of R[], if any
        while j < len(R):  # If there are remaining elements in right subarray
            self.assign(arr, k, R[j])  # Copy element to merged array
            j += 1  # Move to next element in right subarray
            k += 1  # Move to next position in merged array
            
        # Add a step for visualization
        self.steps.append(("merge", left, right, arr.copy()))  # Record the merge operation
from typing import List, Any  # Import type hints for better code documentation
import time  # Import the time module to measure execution time
from .sort_base import SortAlgorithm  # Import the base class for sorting algorithms

class HeapSort(SortAlgorithm):
    """Implementation of Heap Sort algorithm"""
    
    def __init__(self):
        super().__init__("Heap Sort")  # Initialize the parent class with the name "Heap Sort"
    
    def sort(self, arr: List[Any]) -> List[Any]:
        self.reset_metrics()  # Reset all metrics before starting the algorithm
        result = arr.copy()  # Create a copy of the input array to avoid modifying the original
        n = len(result)  # Get the length of the input array
        
        # Record initial state
        self.steps.append(("initial", -1, -1, result.copy()))  # Save the initial state of the array
        
        start_time = time.time()  # Record the start time
        
        # Build a max heap
        for i in range(n // 2 - 1, -1, -1):  # Start from the last non-leaf node and work backwards
            self._heapify(result, n, i)  # Convert the subtree rooted at index i into a max heap
        
        # Extract elements from the heap one by one
        for i in range(n - 1, 0, -1):  # Process each element starting from the end
            # Move current root to end
            self.swap(result, 0, i)  # Swap the root (max element) with the last unsorted element
            
            # Heapify the reduced heap
            self._heapify(result, i, 0)  # Re-heapify the array excluding the sorted elements
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final state
        self.steps.append(("final", -1, -1, result.copy()))  # Save the final sorted state of the array
        
        return result  # Return the sorted array
    
    def _heapify(self, arr: List[Any], n: int, i: int):
        """Heapify a subtree rooted at index i"""
        largest = i  # Initialize largest as root
        left = 2 * i + 1  # Calculate index of left child
        right = 2 * i + 2  # Calculate index of right child
        
        # See if left child exists and is greater than root
        if left < n and self.compare(arr[largest], arr[left]):  # Check if left child is larger than current largest
            largest = left  # Update largest if left child is larger
        
        # See if right child exists and is greater than largest so far
        if right < n and self.compare(arr[largest], arr[right]):  # Check if right child is larger than current largest
            largest = right  # Update largest if right child is larger
        
        # Change root if needed
        if largest != i:  # If largest is not the current root
            self.swap(arr, i, largest)  # Swap current node with the largest child
            
            # Add a step for visualization
            self.steps.append(("heapify", i, largest, arr.copy()))  # Record the heapify operation
            
            # Heapify the affected sub-tree
            self._heapify(arr, n, largest)  # Recursively heapify the affected subtree
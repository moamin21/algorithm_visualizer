import time  # Import the time module to measure execution time
from typing import List, Any  # Import type hints for better code documentation

class SortAlgorithm:
    """Base class for all sorting algorithms"""
    
    def __init__(self, name: str):
        self.name = name  # Store the name of the sorting algorithm
        self.comparisons = 0  # Counter for number of comparisons performed
        self.swaps = 0  # Counter for number of swaps performed
        self.assignments = 0  # Counter for number of assignments performed
        self.execution_time = 0  # Tracker for execution time
        # For visualization - stores state of array at each step
        self.steps = []  # List to store algorithm steps for visualization
    
    def reset_metrics(self):
        """Reset all performance metrics"""
        self.comparisons = 0  # Reset comparisons counter
        self.swaps = 0  # Reset swaps counter
        self.assignments = 0  # Reset assignments counter
        self.execution_time = 0  # Reset execution time
        self.steps = []  # Clear steps list
    
    def compare(self, a: Any, b: Any) -> bool:
        """Compare two elements and increment comparison counter"""
        self.comparisons += 1  # Increment comparison counter
        return a > b  # Return True if a is greater than b
    
    def swap(self, arr: List[Any], i: int, j: int):
        """Swap two elements in an array and increment swap counter"""
        self.swaps += 1  # Increment swap counter
        arr[i], arr[j] = arr[j], arr[i]  # Swap elements at indices i and j
        # Store current state for visualization
        self.steps.append(("swap", i, j, arr.copy()))  # Record the swap operation and current array state
    
    def assign(self, arr: List[Any], i: int, value: Any):
        """Assign a value to an array position and increment assignment counter"""
        self.assignments += 1  # Increment assignment counter
        arr[i] = value  # Assign value to array at index i
        # Store current state for visualization
        self.steps.append(("assign", i, value, arr.copy()))  # Record the assignment operation and current array state
    
    def sort(self, arr: List[Any]) -> List[Any]:
        """Sort method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement sort()")  # Abstract method to be implemented by subclasses
    
    def get_performance_metrics(self) -> dict:
        """Return performance metrics as a dictionary"""
        return {  # Return a dictionary with all performance metrics
            "algorithm": self.name,  # Name of the algorithm
            "comparisons": self.comparisons,  # Number of comparisons
            "swaps": self.swaps,  # Number of swaps
            "assignments": self.assignments,  # Number of assignments
            "execution_time": self.execution_time  # Execution time
        }
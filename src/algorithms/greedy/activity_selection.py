import time  # Import the time module to measure execution time
from typing import List, Tuple, Dict  # Import type hints for better code documentation

class ActivitySelection:
    """
    Implementation of the Activity Selection problem using greedy algorithm
    """
    
    def __init__(self):
        self.reset()  # Initialize the object by calling the reset method
    
    def reset(self):
        """Reset all metrics and states"""
        self.operations = 0  # Counter for number of operations performed
        self.execution_time = 0  # Tracker for execution time
        self.steps = []  # List to store computation steps for visualization
    
    def select_activities(self, start_times: List[int], end_times: List[int]) -> List[int]:
        """
        Select maximum number of non-overlapping activities.
        The greedy approach is to always pick the next activity with the earliest finish time.
        
        Args:
            start_times: List of activity start times
            end_times: List of activity end times
            
        Returns:
            List of indices of selected activities
        """
        self.reset()  # Reset all metrics before starting the algorithm
        
        # Check for valid input
        if len(start_times) != len(end_times):  # Verify input lists have same length
            raise ValueError("Start and end time lists must have the same length")  # Raise error if lengths differ
        
        n = len(start_times)  # Get the number of activities
        if n == 0:  # Handle empty input case
            return []  # Return empty list if no activities
        
        # Create activities as (start, end, index) tuples
        activities = [(start_times[i], end_times[i], i) for i in range(n)]  # Create tuples with (start, end, original index)
        
        # Sort activities by finish time
        activities.sort(key=lambda x: x[1])  # Sort activities based on end time (earliest first)
        
        # Record initial state
        self.steps.append(("init", activities.copy()))  # Save the initial sorted activities
        
        start_time = time.time()  # Record the start time
        
        # First activity is always selected
        selected = [activities[0][2]]  # Select first activity (store original index)
        last_finish_time = activities[0][1]  # Track the finish time of the last selected activity
        
        self.operations += 1  # Count first selection as an operation
        self.steps.append(("select", activities[0], selected.copy(), last_finish_time))  # Record first selection
        
        # Consider all remaining activities
        for i in range(1, n):  # Iterate through remaining activities
            self.operations += 1  # Count each activity consideration as an operation
            current_activity = activities[i]  # Get current activity
            
            # If this activity starts after the last selected activity finishes
            if current_activity[0] >= last_finish_time:  # Check if current activity starts after last selected activity ends
                selected.append(current_activity[2])  # Add original index to selected list
                last_finish_time = current_activity[1]  # Update last finish time
                self.steps.append(("select", current_activity, selected.copy(), last_finish_time))  # Record selection
            else:
                self.steps.append(("skip", current_activity, selected.copy(), last_finish_time))  # Record skipping activity
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final state
        self.steps.append(("final", None, selected.copy(), last_finish_time))  # Save final state
        
        return selected  # Return list of selected activity indices
    
    def dp_select_activities(self, start_times: List[int], end_times: List[int]) -> List[int]:
        """
        Select maximum number of activities using dynamic programming.
        This is for comparison to show that the greedy solution is optimal.
        
        Args:
            start_times: List of activity start times
            end_times: List of activity end times
            
        Returns:
            List of indices of selected activities
        """
        self.reset()  # Reset all metrics before starting the algorithm
        
        # Check for valid input
        if len(start_times) != len(end_times):  # Verify input lists have same length
            raise ValueError("Start and end time lists must have the same length")  # Raise error if lengths differ
        
        n = len(start_times)  # Get the number of activities
        if n == 0:  # Handle empty input case
            return []  # Return empty list if no activities
        
        # Create activities as (start, end, index) tuples and sort by end time
        activities = [(start_times[i], end_times[i], i) for i in range(n)]  # Create tuples with (start, end, original index)
        activities.sort(key=lambda x: x[1])  # Sort activities based on end time (earliest first)
        
        # Record initial state
        self.steps.append(("init", activities.copy()))  # Save the initial sorted activities
        
        start_time = time.time()  # Record the start time
        
        # Initialize DP table
        # dp[i] = max activities we can select from activities[0...i]
        dp = [0] * n  # Create array to store maximum activities up to index i
        dp[0] = 1  # We can always select the first activity
        
        # Initialize array to store the selected activities
        prev = [-1] * n  # prev[i] = previous selected activity before i
        
        # Fill dp table
        for i in range(1, n):  # Iterate through activities starting from index 1
            # Find the latest activity j that doesn't overlap with i
            j = i - 1  # Start from the activity just before current
            while j >= 0 and activities[j][1] > activities[i][0]:  # While activities overlap
                j -= 1  # Move to earlier activity
            
            self.operations += 1  # Count each DP calculation as an operation
            
            # Max activities if we include activity i
            include_i = 1 + (dp[j] if j >= 0 else 0)  # 1 (for current activity) + max activities ending at j
            
            # Max activities if we exclude activity i
            exclude_i = dp[i-1]  # Max activities up to previous position
            
            if include_i > exclude_i:  # If including current activity gives better result
                dp[i] = include_i  # Update DP value
                prev[i] = j  # Set previous activity
                self.steps.append(("dp_include", activities[i], j, dp.copy()))  # Record including activity
            else:
                dp[i] = exclude_i  # Update DP value
                prev[i] = prev[i-1]  # Set previous activity same as for i-1
                self.steps.append(("dp_exclude", activities[i], i-1, dp.copy()))  # Record excluding activity
        
        # Reconstruct solution
        selected = []  # Initialize list for selected activities
        i = n - 1  # Start from the last activity
        while i >= 0:  # Continue until we've considered all activities
            if i == 0 or prev[i] != prev[i-1]:  # If this is first activity or current selection differs from previous
                selected.append(activities[i][2])  # Add original index to selected list
                i = prev[i]  # Jump to previous selected activity
            else:
                i -= 1  # Move to previous activity
        
        # Reverse to get chronological order
        selected.reverse()  # Reverse the list to get activities in original order
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final state
        self.steps.append(("final", None, selected.copy(), -1))  # Save final state
        
        return selected  # Return list of selected activity indices
    
    def compare_approaches(self, start_times: List[int], end_times: List[int]) -> Dict:
        """Compare greedy and DP approaches for activity selection"""
        # Run greedy approach
        greedy_selected = self.select_activities(start_times, end_times)  # Run greedy algorithm
        greedy_metrics = {  # Store metrics from greedy approach
            "operations": self.operations,
            "execution_time": self.execution_time,
            "steps": self.steps.copy()
        }
        
        # Run DP approach
        dp_selected = self.dp_select_activities(start_times, end_times)  # Run DP algorithm
        dp_metrics = {  # Store metrics from DP approach
            "operations": self.operations,
            "execution_time": self.execution_time,
            "steps": self.steps.copy()
        }
        
        return {  # Return results and metrics from both approaches
            "greedy": {
                "selected": greedy_selected,
                "count": len(greedy_selected),
                "metrics": greedy_metrics
            },
            "dp": {
                "selected": dp_selected,
                "count": len(dp_selected),
                "metrics": dp_metrics
            }
        }
    
    def format_activity(self, start: int, end: int, index: int) -> str:
        """Format an activity for display"""
        return f"A{index} ({start}-{end})"  # Create a string representation of an activity
import time  # Import the time module to measure execution time
from typing import List, Tuple, Dict, Optional  # Import type hints for better code documentation
import math  # Import math module for mathematical operations

class FloydWarshall:
    """
    Implementation of the Floyd-Warshall algorithm with visualization support
    """
    
    def __init__(self):
        self.reset()  # Initialize the object by calling the reset method
    
    def reset(self):
        """Reset all metrics and states"""
        self.operations = 0  # Counter for the number of operations performed
        self.execution_time = 0  # Tracker for execution time
        self.space_used = 0  # Tracker for memory usage
        self.steps = []  # List to store computation steps for visualization
    
    def solve(self, graph: List[List[float]]) -> Tuple[List[List[float]], List[List[int]]]:
        """
        Run the Floyd-Warshall algorithm to find shortest paths between all pairs of vertices
        
        Args:
            graph: Adjacency matrix where graph[i][j] is the weight of edge (i,j)
                  Use float('inf') for non-existent edges
                  
        Returns:
            distance matrix, predecessor matrix
        """
        self.reset()  # Reset all metrics before starting the algorithm
        n = len(graph)  # Get the number of vertices in the graph
        
        # Create a copy of the graph for distance matrix
        dist = [row[:] for row in graph]  # Create a deep copy of the input graph matrix
        
        # Initialize predecessor matrix
        # For each edge, if it exists (not inf), set the predecessor to the destination node
        # Otherwise set to -1 (no path)
        pred = [[-1 if dist[i][j] == float('inf') else j for j in range(n)] for i in range(n)]
        for i in range(n):
            pred[i][i] = i  # Set the predecessor of a node to itself for self-loops
        
        self.space_used = n * n * 2  # Calculate space used: n*n for dist matrix + n*n for pred matrix
        
        # Record initial state
        self.steps.append(("init", [row[:] for row in dist], [row[:] for row in pred], -1, -1, -1))  # Save initial matrices state
        
        start_time = time.time()  # Record the start time
        
        # Main Floyd-Warshall algorithm
        for k in range(n):  # For each intermediate vertex k
            for i in range(n):  # For each source vertex i
                for j in range(n):  # For each destination vertex j
                    self.operations += 1  # Count each relaxation attempt as an operation
                    
                    # If vertex k offers a shorter path from i to j, update
                    # Check if path from i to k exists and path from k to j exists
                    # And if using k as intermediate gives shorter path than current direct path
                    if dist[i][k] != float('inf') and dist[k][j] != float('inf') and dist[i][k] + dist[k][j] < dist[i][j]:
                        old_dist = dist[i][j]  # Store old distance for reference
                        old_pred = pred[i][j]  # Store old predecessor for reference
                        
                        dist[i][j] = dist[i][k] + dist[k][j]  # Update distance with the shorter path
                        pred[i][j] = pred[i][k]  # Update predecessor to create the new path
                        
                        self.steps.append(("update", [row[:] for row in dist], [row[:] for row in pred], k, i, j))  # Record the update
                    else:
                        self.steps.append(("no_update", [row[:] for row in dist], [row[:] for row in pred], k, i, j))  # Record no update
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Check for negative cycles
        for i in range(n):  # For each vertex
            if dist[i][i] < 0:  # If distance to itself is negative, there's a negative cycle
                self.steps.append(("negative_cycle", [row[:] for row in dist], [row[:] for row in pred], i, -1, -1))  # Record negative cycle
                return dist, pred  # Return matrices even with negative cycle
        
        # Record final state
        self.steps.append(("final", [row[:] for row in dist], [row[:] for row in pred], -1, -1, -1))  # Save final matrices state
        
        return dist, pred  # Return the distance and predecessor matrices
    
    def get_path(self, pred: List[List[int]], start: int, end: int) -> List[int]:
        """
        Reconstruct the shortest path from start to end using the predecessor matrix
        
        Args:
            pred: Predecessor matrix
            start: Starting vertex
            end: Ending vertex
            
        Returns:
            List of vertices forming the shortest path
        """
        path = []  # Initialize empty path list
        
        # If no path exists
        if pred[start][end] == -1:  # Check if there's no path from start to end
            return path  # Return empty path
        
        # Reconstruct path
        current = start  # Start from the beginning vertex
        while current != end:  # Continue until we reach the end vertex
            path.append(current)  # Add current vertex to path
            current = pred[current][end]  # Move to next vertex using predecessor matrix
            
            # Prevent infinite loops
            if len(path) > len(pred):  # Safety check to prevent infinite loops
                break
        
        path.append(end)  # Add the destination vertex to complete the path
        return path  # Return the reconstructed path
    
    def format_matrix(self, matrix: List[List[float]], vertex_names: Optional[List[str]] = None) -> str:
        """
        Format a matrix for display
        
        Args:
            matrix: The matrix to format
            vertex_names: Optional list of vertex names
            
        Returns:
            Formatted string representation of the matrix
        """
        n = len(matrix)  # Get matrix size
        if vertex_names is None:
            vertex_names = [str(i) for i in range(n)]  # If no names provided, use indices as names
        
        # Calculate column widths
        # For each column, find the maximum width needed between column header and all values in that column
        widths = [max(len(vertex_names[j]), max(len(str(self._format_value(matrix[i][j]))) for i in range(n))) for j in range(n)]
        
        # Create header
        result = "  " + " ".join(vertex_names[j].ljust(widths[j]) for j in range(n)) + "\n"  # Format the header row
        
        # Create rows
        for i in range(n):  # For each row
            row = vertex_names[i] + " " + " ".join(str(self._format_value(matrix[i][j])).ljust(widths[j]) for j in range(n))  # Format each cell
            result += row + "\n"  # Add the formatted row to result
        
        return result  # Return the formatted matrix as a string
    
    def _format_value(self, value: float) -> str:
        """Format a value for display"""
        if value == float('inf'):  # For infinity values
            return "?"  # Display as '?'
        elif value == float('-inf'):  # For negative infinity values
            return "-?"  # Display as '-?'
        elif value == int(value):  # For integer values
            return str(int(value))  # Display as integer without decimal
        else:
            return f"{value:.1f}"  # For floating point values, show one decimal place
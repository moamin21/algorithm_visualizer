import time  # Import the time module to measure execution time
from typing import List, Tuple, Dict, Set  # Import type hints for better code documentation

class DisjointSet:
    """Disjoint Set (Union-Find) data structure for cycle detection"""
    
    def __init__(self, n: int):
        """Initialize a disjoint set with n elements"""
        self.parent = list(range(n))  # Initialize parent array: each element is its own parent initially
        self.rank = [0] * n  # Initialize rank array: all elements have rank 0 initially
    
    def find(self, x: int) -> int:
        """Find the representative (root) of the set containing x with path compression"""
        if self.parent[x] != x:  # If x is not its own parent
            self.parent[x] = self.find(self.parent[x])  # Path compression: update parent to the root
        return self.parent[x]  # Return the root of the set
    
    def union(self, x: int, y: int) -> bool:
        """
        Union the sets containing x and y by rank
        Returns True if x and y were in different sets
        """
        root_x = self.find(x)  # Find the root of x's set
        root_y = self.find(y)  # Find the root of y's set
        
        if root_x == root_y:  # If x and y are already in the same set
            return False  # Already in the same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:  # If rank of x's root is less than y's root
            self.parent[root_x] = root_y  # Make y's root the parent of x's root
        elif self.rank[root_x] > self.rank[root_y]:  # If rank of x's root is greater than y's root
            self.parent[root_y] = root_x  # Make x's root the parent of y's root
        else:  # If ranks are equal
            self.parent[root_y] = root_x  # Make x's root the parent of y's root
            self.rank[root_x] += 1  # Increment the rank of x's root
            
        return True  # Union successful

class Kruskal:
    """
    Implementation of Kruskal's Minimum Spanning Tree algorithm
    """
    
    def __init__(self):
        self.reset()  # Initialize the object by calling the reset method
    
    def reset(self):
        """Reset all metrics and states"""
        self.operations = 0  # Counter for number of operations performed
        self.execution_time = 0  # Tracker for execution time
        self.steps = []  # List to store computation steps for visualization
    
    def find_mst(self, vertices: int, edges: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        """
        Find the Minimum Spanning Tree (MST) using Kruskal's algorithm
        
        Args:
            vertices: Number of vertices in the graph
            edges: List of edges as (u, v, weight) tuples
            
        Returns:
            List of edges in the MST
        """
        self.reset()  # Reset all metrics before starting the algorithm
        
        if vertices <= 0:  # Check for invalid input
            return []  # Return empty list if no vertices
        
        # Record initial state
        self.steps.append(("init", edges.copy(), []))  # Save initial state with all edges
        
        start_time = time.time()  # Record the start time
        
        # Sort edges by weight (increasing order)
        sorted_edges = sorted(edges, key=lambda e: e[2])  # Sort edges by weight (third element of tuple)
        self.steps.append(("sort", sorted_edges.copy(), []))  # Record sorted edges
        
        # Initialize disjoint set for cycle detection
        ds = DisjointSet(vertices)  # Create a disjoint set with 'vertices' number of elements
        
        # Result will store the edges of the MST
        mst = []  # Initialize empty list for MST edges
        
        # Process each edge in order of increasing weight
        for edge in sorted_edges:  # Iterate through sorted edges
            self.operations += 1  # Count each edge consideration as an operation
            u, v, weight = edge  # Unpack the edge: source vertex, destination vertex, and weight
            
            # Check if adding the edge would create a cycle
            if ds.find(u) != ds.find(v):  # If u and v are in different sets (no cycle would be created)
                # Include this edge in the MST
                mst.append(edge)  # Add edge to MST
                ds.union(u, v)  # Union the sets containing u and v
                self.steps.append(("add", edge, mst.copy()))  # Record adding edge to MST
            else:
                # Skip this edge (would create a cycle)
                self.steps.append(("skip", edge, mst.copy()))  # Record skipping edge
            
            # Check if MST is complete (has v-1 edges)
            if len(mst) == vertices - 1:  # If we have v-1 edges, MST is complete
                break  # Exit the loop early
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final MST
        self.steps.append(("final", None, mst.copy()))  # Save final MST
        
        return mst  # Return the MST as a list of edges
    
    def calculate_mst_weight(self, mst: List[Tuple[int, int, int]]) -> int:
        """Calculate the total weight of the MST"""
        return sum(weight for _, _, weight in mst)  # Sum the weights of all edges in the MST
    
    def is_connected(self, vertices: int, edges: List[Tuple[int, int, int]]) -> bool:
        """Check if the graph is connected"""
        if not edges:  # If there are no edges
            return vertices <= 1  # Graph is connected only if it has 0 or 1 vertex
        
        # Build adjacency list
        adj_list = [[] for _ in range(vertices)]  # Create an empty adjacency list for each vertex
        for u, v, _ in edges:  # For each edge in the graph
            adj_list[u].append(v)  # Add v to u's adjacency list
            adj_list[v].append(u)  # Add u to v's adjacency list (for undirected graph)
        
        # DFS to check connectivity
        visited = [False] * vertices  # Initialize visited array to track visited vertices
        
        def dfs(node):  # Define DFS function to traverse the graph
            visited[node] = True  # Mark current node as visited
            for neighbor in adj_list[node]:  # For each neighbor of current node
                if not visited[neighbor]:  # If neighbor hasn't been visited
                    dfs(neighbor)  # Recursively visit the neighbor
        
        # Start DFS from first vertex
        dfs(0)  # Start DFS from vertex 0
        
        # Check if all vertices are visited
        return all(visited)  # Return True if all vertices were visited, False otherwise
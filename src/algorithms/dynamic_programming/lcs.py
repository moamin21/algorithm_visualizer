import time  # Import the time module to measure execution time
from typing import List, Tuple, Dict  # Import type hints for better code documentation

class LCS:
    """
    Implementation of the Longest Common Subsequence problem with visualization support
    """
    
    def __init__(self):
        self.reset()  # Initialize the object by calling the reset method
    
    def reset(self):
        """Reset all metrics and states"""
        self.operations = 0  # Counter for number of operations performed
        self.execution_time = 0  # Tracker for execution time
        self.space_used = 0  # Tracker for memory usage
        self.steps = []  # List to store computation steps for visualization
    
    def find_lcs(self, text1: str, text2: str) -> Tuple[str, List[List[int]]]:
        """
        Find the longest common subsequence of two strings using dynamic programming
        Returns the LCS string and the DP table used to calculate it
        """
        self.reset()  # Reset all metrics before starting the algorithm
        
        m, n = len(text1), len(text2)  # Get the lengths of both input strings
        
        # Initialize the DP table with zeros
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]  # Create a (m+1) x (n+1) table filled with zeros
        self.space_used = (m + 1) * (n + 1)  # Calculate space used by the DP table
        
        # Record initial state
        self.steps.append(("init", dp, "", -1, -1))  # Save the initial state of the DP table
        
        start_time = time.time()  # Record the start time
        
        # Fill the DP table
        for i in range(1, m + 1):  # For each character in text1 (1-indexed)
            for j in range(1, n + 1):  # For each character in text2 (1-indexed)
                self.operations += 1  # Count each cell calculation as an operation
                
                if text1[i-1] == text2[j-1]:  # If characters match (using 0-indexed strings)
                    # Characters match, extend the LCS
                    dp[i][j] = dp[i-1][j-1] + 1  # LCS length increases by 1
                    self.steps.append(("match", dp, text1[i-1], i-1, j-1))  # Record matching characters
                else:
                    # Characters don't match, take the max of the two options
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # Take maximum of left cell or upper cell
                    choice = "left" if dp[i][j-1] > dp[i-1][j] else "up"  # Determine which direction was chosen
                    self.steps.append(("no_match", dp, choice, i-1, j-1))  # Record non-matching characters
        
        # Backtrack to find the actual LCS
        lcs = []  # Initialize list to store LCS characters
        i, j = m, n  # Start from bottom-right cell of DP table
        
        while i > 0 and j > 0:  # Continue until we reach the first row or column
            if text1[i-1] == text2[j-1]:  # If characters match
                # Current characters are part of LCS
                lcs.append(text1[i-1])  # Add character to LCS
                i -= 1  # Move diagonally up-left
                j -= 1
                self.steps.append(("backtrack_match", dp, text1[i], i, j))  # Record matching in backtracking
            elif dp[i-1][j] > dp[i][j-1]:  # If value from above is larger
                # Move up in the table
                i -= 1  # Move up
                self.steps.append(("backtrack_up", dp, "", i, j))  # Record upward move in backtracking
            else:
                # Move left in the table
                j -= 1  # Move left
                self.steps.append(("backtrack_left", dp, "", i, j))  # Record leftward move in backtracking
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Reverse the LCS (we built it backwards)
        lcs.reverse()  # Reverse to get correct order
        lcs_str = ''.join(lcs)  # Convert list of characters to string
        
        # Record final state
        self.steps.append(("final", dp, lcs_str, -1, -1))  # Save final state with LCS result
        
        return lcs_str, dp  # Return the LCS string and DP table
    
    def print_lcs_alignment(self, text1: str, text2: str, lcs: str) -> str:
        """
        Create a visual alignment of the two strings showing the LCS
        Returns a formatted string showing the alignment
        """
        # Map LCS characters to their positions in text1 and text2
        positions1 = self._find_lcs_positions(text1, lcs)  # Find positions of LCS characters in text1
        positions2 = self._find_lcs_positions(text2, lcs)  # Find positions of LCS characters in text2
        
        # Create alignment visualization
        alignment = []  # Initialize list for alignment strings
        alignment.append(f"String 1: {text1}")  # Add the first string to alignment
        
        # Create match line
        match_line = ""  # Initialize match line
        pos1_idx = 0  # Index to track position in the positions1 list
        for i, char in enumerate(text1):  # For each character in text1
            if pos1_idx < len(positions1) and i == positions1[pos1_idx]:  # If current position is part of LCS
                match_line += "|"  # Add a vertical bar to show match
                pos1_idx += 1  # Move to next position
            else:
                match_line += " "  # Add space for non-matching character
        alignment.append(f"Match:    {match_line}")  # Add match line to alignment
        
        alignment.append(f"String 2: {text2}")  # Add the second string to alignment
        
        # Add the LCS
        alignment.append(f"LCS:      {lcs}")  # Add the LCS string to alignment
        
        return "\n".join(alignment)  # Join all lines with newlines and return
    
    def _find_lcs_positions(self, text: str, lcs: str) -> List[int]:
        """Find positions of LCS characters in the original text"""
        positions = []  # Initialize list to store positions
        lcs_idx = 0  # Index to track position in LCS string
        
        for i, char in enumerate(text):  # For each character in the text
            if lcs_idx < len(lcs) and char == lcs[lcs_idx]:  # If current character matches current LCS character
                positions.append(i)  # Record the position
                lcs_idx += 1  # Move to next LCS character
        
        return positions  # Return list of positions
import time  # Import the time module to measure execution time
import heapq  # Import the heapq module for priority queue implementation
from typing import Dict, List, Tuple, Optional  # Import type hints for better code documentation

class HuffmanNode:
    """Node in a Huffman tree"""
    
    def __init__(self, char: str, freq: int):
        self.char = char  # Character stored in this node
        self.freq = freq  # Frequency of the character
        self.left = None  # Reference to left child
        self.right = None  # Reference to right child
    
    def __lt__(self, other):
        # For priority queue ordering
        return self.freq < other.freq  # Compare nodes based on frequency for min-heap
    
    def is_leaf(self) -> bool:
        """Check if the node is a leaf node (has no children)"""
        return self.left is None and self.right is None  # True if node has no children

class HuffmanCoding:
    """
    Implementation of the Huffman Coding algorithm for compression
    """
    
    def __init__(self):
        self.reset()  # Initialize the object by calling the reset method
    
    def reset(self):
        """Reset all metrics and states"""
        self.operations = 0  # Counter for number of operations performed
        self.execution_time = 0  # Tracker for execution time
        self.steps = []  # List to store computation steps for visualization
        self.huffman_tree = None  # Root of the Huffman tree
        self.codes = {}  # Dictionary to store Huffman codes for each character
    
    def build_huffman_tree(self, text: str) -> HuffmanNode:
        """
        Build a Huffman tree for the given text
        
        Args:
            text: Input text to encode
            
        Returns:
            Root node of the Huffman tree
        """
        self.reset()  # Reset all metrics before starting the algorithm
        
        if not text:  # Check if input text is empty
            return None  # Return None for empty input
        
        # Calculate frequency of each character
        freq = {}  # Dictionary to store character frequencies
        for char in text:  # Iterate through each character in the text
            freq[char] = freq.get(char, 0) + 1  # Increment frequency counter for this character
        
        # Record initial frequencies
        self.steps.append(("init", freq.copy()))  # Save character frequencies
        
        start_time = time.time()  # Record the start time
        
        # Create leaf nodes for each character
        nodes = [HuffmanNode(char, freq) for char, freq in freq.items()]  # Create a node for each unique character
        
        # Create a priority queue (min heap)
        heapq.heapify(nodes)  # Convert the list into a min heap priority queue
        
        # Record nodes state
        self.steps.append(("heap", [(node.char, node.freq) for node in nodes]))  # Save initial heap state
        
        # Build the Huffman tree
        while len(nodes) > 1:  # Continue until only one node remains (the root)
            self.operations += 1  # Count each merge operation
            
            # Extract two nodes with lowest frequencies
            left = heapq.heappop(nodes)  # Extract node with lowest frequency
            right = heapq.heappop(nodes)  # Extract node with second lowest frequency
            
            # Record extraction
            self.steps.append(("extract", (left.char, left.freq), (right.char, right.freq)))  # Record nodes being merged
            
            # Create a new internal node with these two nodes as children
            # Use empty string for internal nodes
            internal = HuffmanNode('', left.freq + right.freq)  # Create new internal node with combined frequency
            internal.left = left  # Set left child
            internal.right = right  # Set right child
            
            # Add the new node back to the priority queue
            heapq.heappush(nodes, internal)  # Add the new internal node to the heap
            
            # Record heap after insertion
            self.steps.append(("insert", [(node.char, node.freq) for node in nodes]))  # Save heap state after insertion
        
        # The last remaining node is the root of the Huffman tree
        self.huffman_tree = nodes[0] if nodes else None  # Store the root of the Huffman tree
        
        # Generate codes
        self.codes = {}  # Initialize codes dictionary
        self._generate_codes(self.huffman_tree, "")  # Generate Huffman codes for each character
        
        self.execution_time = time.time() - start_time  # Calculate total execution time
        
        # Record final tree and codes
        self.steps.append(("final_tree", self.huffman_tree))  # Save the final Huffman tree
        self.steps.append(("codes", self.codes.copy()))  # Save the generated Huffman codes
        
        return self.huffman_tree  # Return the root of the Huffman tree
    
    def _generate_codes(self, node: Optional[HuffmanNode], code: str):
        """
        Recursively generate Huffman codes for each character
        
        Args:
            node: Current node in the tree
            code: Current code for the path to this node
        """
        if node is None:  # Base case: if node is None
            return  # Return without doing anything
        
        # If this is a leaf node, store the code
        if node.is_leaf():  # Check if this is a leaf node
            self.codes[node.char] = code  # Assign the current code to the character
            self.steps.append(("code", node.char, code))  # Record code assignment
            return  # Exit this branch
        
        # Recursively generate codes for left and right subtrees
        # Left branch gets a '0', right branch gets a '1'
        self._generate_codes(node.left, code + "0")  # Add '0' for left branch
        self._generate_codes(node.right, code + "1")  # Add '1' for right branch
    
    def encode(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Encode text using Huffman codes
        
        Args:
            text: Input text to encode
            
        Returns:
            Encoded binary string and the codes dictionary
        """
        if not self.huffman_tree:  # If tree hasn't been built yet
            self.build_huffman_tree(text)  # Build the Huffman tree first
        
        # Encode the text
        encoded_text = ""  # Initialize encoded text string
        for char in text:  # Iterate through each character in the input text
            encoded_text += self.codes[char]  # Add the Huffman code for this character
        
        # Record encoding
        self.steps.append(("encode", text, encoded_text))  # Save the encoding process
        
        return encoded_text, self.codes  # Return encoded text and codes dictionary
    
    def decode(self, encoded_text: str, tree: HuffmanNode) -> str:
        """
        Decode Huffman-encoded text using the Huffman tree
        
        Args:
            encoded_text: Binary string to decode
            tree: Huffman tree root node
            
        Returns:
            Decoded text
        """
        if not tree or not encoded_text:  # Check for empty inputs
            return ""  # Return empty string for empty inputs
        
        decoded_text = ""  # Initialize decoded text string
        current = tree  # Start at the root of the tree
        
        # Record decoding steps
        decode_steps = []  # List to track decoding steps for visualization
        
        for bit in encoded_text:  # Iterate through each bit in the encoded text
            # Follow tree based on the bit (0 = left, 1 = right)
            if bit == '0':  # If bit is '0'
                current = current.left  # Move to left child
                decode_steps.append(("left", bit))  # Record left movement
            else:  # If bit is '1'
                current = current.right  # Move to right child
                decode_steps.append(("right", bit))  # Record right movement
            
            # If we reach a leaf node, we've found a character
            if current.is_leaf():  # Check if current node is a leaf
                decoded_text += current.char  # Add character to decoded text
                decode_steps.append(("char", current.char))  # Record character found
                # Reset to the root for the next character
                current = tree  # Go back to the root to decode next character
        
        # Record decoding
        self.steps.append(("decode", encoded_text, decoded_text, decode_steps))  # Save the decoding process
        
        return decoded_text  # Return the decoded text
    
    def calculate_compression_ratio(self, text: str, encoded_text: str) -> float:
        """
        Calculate the compression ratio achieved
        
        Args:
            text: Original text
            encoded_text: Huffman-encoded binary string
            
        Returns:
            Compression ratio (original size / compressed size)
        """
        # Original size in bits (8 bits per character)
        original_size = len(text) * 8  # Calculate size of original text (assuming 8 bits per character)
        
        # Compressed size in bits
        compressed_size = len(encoded_text)  # Size of the encoded text in bits
        
        # Compression ratio
        ratio = original_size / compressed_size if compressed_size > 0 else 0  # Calculate ratio, avoid division by zero
        
        # Record compression statistics
        self.steps.append(("compression", original_size, compressed_size, ratio))  # Save compression statistics
        
        return ratio  # Return the compression ratio
    
    def get_tree_as_dict(self, node: Optional[HuffmanNode] = None, prefix: str = "", result: Optional[Dict] = None) -> Dict:
        """
        Convert the Huffman tree to a dictionary for visualization
        
        Args:
            node: Current node
            prefix: Current path prefix
            result: Dictionary to build up
            
        Returns:
            Dictionary representation of the tree
        """
        if result is None:  # Initialize result dictionary if not provided
            result = {}
        
        if node is None:  # If no node is provided
            node = self.huffman_tree  # Use the class's Huffman tree
            if node is None:  # If tree doesn't exist
                return {}  # Return empty dictionary
        
        # For leaf nodes, store character and frequency
        if node.is_leaf():  # Check if this is a leaf node
            result[prefix] = {  # Store node information in result dictionary
                "char": node.char,  # Character stored in this node
                "freq": node.freq,  # Frequency of the character
                "code": self.codes.get(node.char, "")  # Huffman code for this character
            }
        else:
            # For internal nodes, store frequency and recurse
            result[prefix] = {  # Store node information in result dictionary
                "char": "",  # Internal nodes don't have characters
                "freq": node.freq,  # Combined frequency of all descendants
                "code": ""  # Internal nodes don't have codes
            }
            self.get_tree_as_dict(node.left, prefix + "0", result)  # Recursively process left subtree
            self.get_tree_as_dict(node.right, prefix + "1", result)  # Recursively process right subtree
        
        return result  # Return the complete dictionary representation
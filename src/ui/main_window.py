import random  # Import the random module for generating random values
from PyQt5.QtWidgets import (  # Import Qt widgets for GUI components
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QLineEdit, QTabWidget, QSpinBox, QTableWidget, QTableWidgetItem,
    QGroupBox, QRadioButton, QSlider, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer  # Import Qt core components for signals and timing

# Import custom widgets for visualizing algorithms
from ui.widgets.array_visualizer import ArrayVisualizer  # Widget for visualizing arrays
from ui.widgets.metrics_table import MetricsTable  # Widget for displaying performance metrics

# Import sorting algorithm implementations
from algorithms.sorting.bubble_sort import BubbleSort  # Import Bubble Sort
from algorithms.sorting.heap_sort import HeapSort  # Import Heap Sort
from algorithms.sorting.insertion_sort import InsertionSort  # Import Insertion Sort
from algorithms.sorting.merge_sort import MergeSort  # Import Merge Sort
from algorithms.sorting.quick_sort import QuickSort  # Import Quick Sort
from algorithms.sorting.selection_sort import SelectionSort  # Import Selection Sort

# Import dynamic programming algorithm implementations
from algorithms.dynamic_programming.fibonacci import Fibonacci  # Import Fibonacci sequence algorithm
from algorithms.dynamic_programming.floyd_warshall import FloydWarshall  # Import Floyd-Warshall algorithm
from algorithms.dynamic_programming.knapsack import Knapsack  # Import Knapsack problem algorithm
from algorithms.dynamic_programming.lcs import LCS  # Import Longest Common Subsequence algorithm

# Import greedy algorithm implementations
from algorithms.greedy.activity_selection import ActivitySelection  # Import Activity Selection algorithm
from algorithms.greedy.coin_change import CoinChange  # Import Coin Change algorithm
from algorithms.greedy.huffman_coding import HuffmanCoding  # Import Huffman Coding algorithm
from algorithms.greedy.kruskal import Kruskal  # Import Kruskal's algorithm for minimum spanning trees

# Import search algorithm implementations
from algorithms.search.binary_search import BinarySearch  # Import Binary Search algorithm

class AlgorithmVisualizer(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()  # Initialize the parent QMainWindow
        self.setWindowTitle("Algorithm Visualizer")  # Set the window title
        self.setMinimumSize(1200, 800)  # Set the minimum window size
        
        # Initialize algorithm instances
        self.sort_algorithms = {  # Create a dictionary of sorting algorithm instances
            "Bubble Sort": BubbleSort(),
            "Heap Sort": HeapSort(),
            "Insertion Sort": InsertionSort(),
            "Merge Sort": MergeSort(),
            "Quick Sort": QuickSort(),
            "Selection Sort": SelectionSort()
        }
        
        self.dp_algorithms = {  # Create a dictionary of dynamic programming algorithm instances
            "Fibonacci": Fibonacci(),
            "Floyd Warshall": FloydWarshall(),
            "Knapsack": Knapsack(),
            "LCS": LCS()
        }
        
        self.greedy_algorithms = {  # Create a dictionary of greedy algorithm instances
            "Activity Selection": ActivitySelection(),
            "Coin Change": CoinChange(),
            "Huffman Coding": HuffmanCoding(),
            "Kruskal": Kruskal()
        }
        
        self.binary_search = BinarySearch()  # Create a binary search instance
        
        # Current data and state
        self.current_array = []  # Initialize empty current array
        self.current_step_index = 0  # Initialize step index to 0
        self.current_algorithm = None  # Initialize current algorithm to None
        self.current_steps = []  # Initialize empty steps list
        self.animation_speed = 500  # Initialize animation speed to 500ms delay between steps
        
        # Setup UI
        self.setup_ui()  # Call the method to set up the user interface
    
    def setup_ui(self):
        """Setup the main UI components"""
        central_widget = QWidget()  # Create a central widget
        self.setCentralWidget(central_widget)  # Set it as the main window's central widget
        
        main_layout = QVBoxLayout(central_widget)  # Create a vertical layout for the central widget
        
        # Create tabs for different algorithm categories
        self.tabs = QTabWidget()  # Create a tab widget to hold different algorithm categories
        self.tabs.setTabPosition(QTabWidget.North)  # Set tabs to appear at the top
        
        # Create tabs for each category
        self.sorting_tab = self.create_sorting_tab()  # Create the sorting algorithms tab
        self.dp_tab = self.create_dp_tab()  # Create the dynamic programming tab
        self.greedy_tab = self.create_greedy_tab()  # Create the greedy algorithms tab
        
        self.tabs.addTab(self.sorting_tab, "Sorting Algorithms")  # Add the sorting tab to the tab widget
        self.tabs.addTab(self.dp_tab, "Dynamic Programming")  # Add the DP tab to the tab widget
        self.tabs.addTab(self.greedy_tab, "Greedy Algorithms")  # Add the greedy tab to the tab widget
        
        main_layout.addWidget(self.tabs)  # Add the tab widget to the main layout
    
    def create_sorting_tab(self):
        """Create the sorting algorithms tab"""
        tab = QWidget()  # Create a widget for this tab
        layout = QVBoxLayout(tab)  # Create a vertical layout for the tab
        
        # Top controls
        top_layout = QHBoxLayout()  # Create a horizontal layout for the top controls
        
        # Algorithm selection
        algo_group = QGroupBox("Algorithm")  # Create a group box for algorithm selection
        algo_layout = QVBoxLayout(algo_group)  # Create a vertical layout for the group box
        self.sort_algo_combo = QComboBox()  # Create a combo box for selecting algorithms
        self.sort_algo_combo.addItems(self.sort_algorithms.keys())  # Add the names of sorting algorithms
        algo_layout.addWidget(self.sort_algo_combo)  # Add the combo box to the layout
        
        # List generation options
        list_group = QGroupBox("List Generation")  # Create a group box for list generation options
        list_layout = QVBoxLayout(list_group)  # Create a vertical layout for the group box
        
        # List type
        list_type_layout = QHBoxLayout()  # Create a horizontal layout for list type controls
        self.list_size_spin = QSpinBox()  # Create a spin box for list size
        self.list_size_spin.setRange(5, 100)  # Set the range of list sizes
        self.list_size_spin.setValue(20)  # Set the default list size
        list_type_layout.addWidget(QLabel("Size:"))  # Add a label
        list_type_layout.addWidget(self.list_size_spin)  # Add the spin box
        
        # List type radio buttons
        self.random_list_radio = QRadioButton("Random")  # Create a radio button for random lists
        self.sorted_list_radio = QRadioButton("Sorted")  # Create a radio button for sorted lists
        self.reverse_list_radio = QRadioButton("Reverse Sorted")  # Create a radio button for reverse sorted lists
        self.custom_list_radio = QRadioButton("Custom")  # Create a radio button for custom lists
        self.random_list_radio.setChecked(True)  # Set the random list option as default
        
        list_type_layout.addWidget(self.random_list_radio)  # Add the random list radio button
        list_type_layout.addWidget(self.sorted_list_radio)  # Add the sorted list radio button
        list_type_layout.addWidget(self.reverse_list_radio)  # Add the reverse sorted radio button
        list_type_layout.addWidget(self.custom_list_radio)  # Add the custom list radio button
        
        # Custom list input
        custom_layout = QHBoxLayout()  # Create a horizontal layout for custom list input
        self.custom_list_input = QLineEdit()  # Create a line edit for entering custom lists
        self.custom_list_input.setPlaceholderText("Enter comma-separated values")  # Set placeholder text
        self.custom_list_input.setEnabled(False)  # Disable it initially (since Random is selected)
        custom_layout.addWidget(QLabel("Custom:"))  # Add a label
        custom_layout.addWidget(self.custom_list_input)  # Add the line edit
        
        # Connect custom radio to enable/disable input
        self.custom_list_radio.toggled.connect(
            lambda checked: self.custom_list_input.setEnabled(checked))  # Enable custom input only when selected
        
        # Generate button
        self.generate_btn = QPushButton("Generate List")  # Create a button to generate lists
        self.generate_btn.clicked.connect(self.generate_list)  # Connect it to the generate_list method
        
        list_layout.addLayout(list_type_layout)  # Add list type controls to the list layout
        list_layout.addLayout(custom_layout)  # Add custom list input to the list layout
        list_layout.addWidget(self.generate_btn)  # Add the generate button to the list layout
        
        # Run controls
        run_group = QGroupBox("Run")  # Create a group box for run controls
        run_layout = QVBoxLayout(run_group)  # Create a vertical layout for the group box
        
        self.run_btn = QPushButton("Run Sort")  # Create a button to run sorting
        self.run_btn.clicked.connect(self.run_sort)  # Connect it to the run_sort method
        
        run_layout.addWidget(self.run_btn)  # Add the run button to the layout
        
        # Binary search controls
        search_group = QGroupBox("Binary Search")  # Create a group box for binary search
        search_layout = QHBoxLayout(search_group)  # Create a horizontal layout for the group box
        
        self.search_input = QLineEdit()  # Create a line edit for the search value
        self.search_input.setPlaceholderText("Enter value to search")  # Set placeholder text
        self.search_btn = QPushButton("Search")  # Create a search button
        self.search_btn.clicked.connect(self.run_binary_search)  # Connect it to the run_binary_search method
        
        search_layout.addWidget(QLabel("Value:"))  # Add a label
        search_layout.addWidget(self.search_input)  # Add the search input
        search_layout.addWidget(self.search_btn)  # Add the search button
        
        # Add all control groups to top layout
        top_layout.addWidget(algo_group)  # Add algorithm selection to top layout
        top_layout.addWidget(list_group)  # Add list generation to top layout
        top_layout.addWidget(run_group)  # Add run controls to top layout
        top_layout.addWidget(search_group)  # Add search controls to top layout
        
        layout.addLayout(top_layout)  # Add the top controls to the main layout
        
        # Animation controls
        anim_layout = QHBoxLayout()  # Create a horizontal layout for animation controls
        
        self.prev_step_btn = QPushButton("Previous Step")  # Create a button for previous step
        self.prev_step_btn.clicked.connect(self.show_previous_step)  # Connect to show_previous_step method
        self.prev_step_btn.setEnabled(False)  # Disable initially
        
        self.next_step_btn = QPushButton("Next Step")  # Create a button for next step
        self.next_step_btn.clicked.connect(self.show_next_step)  # Connect to show_next_step method
        self.next_step_btn.setEnabled(False)  # Disable initially
        
        self.play_btn = QPushButton("Play")  # Create a button to play animation
        self.play_btn.clicked.connect(self.play_animation)  # Connect to play_animation method
        self.play_btn.setEnabled(False)  # Disable initially
        
        self.reset_btn = QPushButton("Reset")  # Create a button to reset animation
        self.reset_btn.clicked.connect(self.reset_animation)  # Connect to reset_animation method
        self.reset_btn.setEnabled(False)  # Disable initially
        
        self.speed_slider = QSlider(Qt.Horizontal)  # Create a horizontal slider for animation speed
        self.speed_slider.setRange(1, 10)  # Set the range (1-10)
        self.speed_slider.setValue(5)  # Set default value
        self.speed_slider.setTickPosition(QSlider.TicksBelow)  # Show ticks below the slider
        self.speed_slider.valueChanged.connect(self.update_animation_speed)  # Connect to update_animation_speed method
        
        anim_layout.addWidget(self.prev_step_btn)  # Add previous step button
        anim_layout.addWidget(self.next_step_btn)  # Add next step button
        anim_layout.addWidget(self.play_btn)  # Add play button
        anim_layout.addWidget(self.reset_btn)  # Add reset button
        anim_layout.addWidget(QLabel("Animation Speed:"))  # Add a label
        anim_layout.addWidget(self.speed_slider)  # Add the speed slider
        
        layout.addLayout(anim_layout)  # Add the animation controls to the main layout
        
        # Main visualization area
        viz_layout = QHBoxLayout()  # Create a horizontal layout for visualization
        
        # Array visualization
        viz_group = QGroupBox("Visualization")  # Create a group box for visualization
        viz_inner_layout = QVBoxLayout(viz_group)  # Create a vertical layout for the group box
        
        self.array_viz = ArrayVisualizer()  # Create an array visualizer
        viz_inner_layout.addWidget(self.array_viz)  # Add it to the layout
        
        # Step description
        self.step_description = QTextEdit()  # Create a text edit for step descriptions
        self.step_description.setReadOnly(True)  # Make the text edit read-only since it's just for display
        self.step_description.setFixedHeight(100)  # Set a fixed height for the description area
        viz_inner_layout.addWidget(QLabel("Step Description:"))  # Add a label for the description area
        viz_inner_layout.addWidget(self.step_description)  # Add the description text edit to the visualization layout
        
        # Metrics visualization
        metrics_group = QGroupBox("Performance Metrics")  # Create a group box for performance metrics
        metrics_layout = QVBoxLayout(metrics_group)  # Create a vertical layout for the metrics group
        
        self.metrics_table = MetricsTable()  # Create a metrics table for displaying algorithm performance
        metrics_layout.addWidget(self.metrics_table)  # Add the metrics table to the layout
        
        viz_layout.addWidget(viz_group, 7)  # Add visualization group with 70% width
        viz_layout.addWidget(metrics_group, 3)  # Add metrics group with 30% width
        
        layout.addLayout(viz_layout)  # Add the visualization layout to the main layout
        
        # Setup animation timer
        self.animation_timer = QTimer(self)  # Create a timer for controlling animation playback
        self.animation_timer.timeout.connect(self.animation_step)  # Connect the timer to the animation_step method
        
        return tab  # Return the completed tab widget
    
    def create_dp_tab(self):
        """Create the dynamic programming algorithms tab"""
        tab = QWidget()  # Create a widget for this tab
        layout = QVBoxLayout(tab)  # Create a vertical layout for the tab
        
        # Controls
        controls_layout = QHBoxLayout()  # Create a horizontal layout for controls
        
        # Algorithm selection
        algo_group = QGroupBox("Algorithm")  # Create a group box for algorithm selection
        algo_layout = QVBoxLayout(algo_group)  # Create a vertical layout for the group box
        
        self.dp_algo_combo = QComboBox()  # Create a combo box for selecting DP algorithms
        self.dp_algo_combo.addItems(self.dp_algorithms.keys())  # Add the names of DP algorithms
        algo_layout.addWidget(self.dp_algo_combo)  # Add the combo box to the layout
        
        # Parameters for different DP algorithms
        params_group = QGroupBox("Parameters")  # Create a group box for algorithm parameters
        params_layout = QVBoxLayout(params_group)  # Create a vertical layout for the parameters
        
        self.dp_params_stack = QTabWidget()  # Create a tab widget to hold different parameter sets
        
        # Fibonacci parameters
        fib_widget = QWidget()  # Create a widget for Fibonacci parameters
        fib_layout = QVBoxLayout(fib_widget)  # Create a vertical layout for the widget
        self.fib_n_spin = QSpinBox()  # Create a spin box for the Fibonacci N value
        self.fib_n_spin.setRange(1, 40)  # Set the range (1-40)
        self.fib_n_spin.setValue(10)  # Set default value
        fib_layout.addWidget(QLabel("N:"))  # Add a label
        fib_layout.addWidget(self.fib_n_spin)  # Add the spin box
        self.dp_params_stack.addTab(fib_widget, "Fibonacci")  # Add the widget as a tab
        
        # Floyd-Warshall parameters
        fw_widget = QWidget()  # Create a widget for Floyd-Warshall parameters
        fw_layout = QVBoxLayout(fw_widget)  # Create a vertical layout for the widget
        self.fw_vertices_spin = QSpinBox()  # Create a spin box for number of vertices
        self.fw_vertices_spin.setRange(2, 10)  # Set the range (2-10)
        self.fw_vertices_spin.setValue(4)  # Set default value
        fw_layout.addWidget(QLabel("Vertices:"))  # Add a label
        fw_layout.addWidget(self.fw_vertices_spin)  # Add the spin box
        self.fw_graph_text = QTextEdit()  # Create a text edit for entering the graph
        self.fw_graph_text.setPlaceholderText("Enter adjacency matrix (comma-separated rows, INF for infinity)")  # Set placeholder text
        fw_layout.addWidget(QLabel("Graph:"))  # Add a label
        fw_layout.addWidget(self.fw_graph_text)  # Add the text edit
        self.dp_params_stack.addTab(fw_widget, "Floyd-Warshall")  # Add the widget as a tab
        
        # Knapsack parameters
        knapsack_widget = QWidget()  # Create a widget for Knapsack parameters
        knapsack_layout = QVBoxLayout(knapsack_widget)  # Create a vertical layout for the widget
        self.knapsack_capacity_spin = QSpinBox()  # Create a spin box for knapsack capacity
        self.knapsack_capacity_spin.setRange(1, 100)  # Set the range (1-100)
        self.knapsack_capacity_spin.setValue(10)  # Set default value
        knapsack_layout.addWidget(QLabel("Capacity:"))  # Add a label
        knapsack_layout.addWidget(self.knapsack_capacity_spin)  # Add the spin box
        self.knapsack_weights_input = QLineEdit()  # Create a line edit for item weights
        self.knapsack_weights_input.setPlaceholderText("Enter weights (comma-separated)")  # Set placeholder text
        knapsack_layout.addWidget(QLabel("Weights:"))  # Add a label
        knapsack_layout.addWidget(self.knapsack_weights_input)  # Add the line edit
        self.knapsack_values_input = QLineEdit()  # Create a line edit for item values
        self.knapsack_values_input.setPlaceholderText("Enter values (comma-separated)")  # Set placeholder text
        knapsack_layout.addWidget(QLabel("Values:"))  # Add a label
        knapsack_layout.addWidget(self.knapsack_values_input)  # Add the line edit
        self.dp_params_stack.addTab(knapsack_widget, "Knapsack")  # Add the widget as a tab
        
        # LCS parameters
        lcs_widget = QWidget()  # Create a widget for LCS parameters
        lcs_layout = QVBoxLayout(lcs_widget)  # Create a vertical layout for the widget
        self.lcs_str1_input = QLineEdit()  # Create a line edit for the first string
        self.lcs_str1_input.setPlaceholderText("Enter first string")  # Set placeholder text
        lcs_layout.addWidget(QLabel("String 1:"))  # Add a label
        lcs_layout.addWidget(self.lcs_str1_input)  # Add the line edit
        self.lcs_str2_input = QLineEdit()  # Create a line edit for the second string
        self.lcs_str2_input.setPlaceholderText("Enter second string")  # Set placeholder text
        lcs_layout.addWidget(QLabel("String 2:"))  # Add a label
        lcs_layout.addWidget(self.lcs_str2_input)  # Add the line edit
        self.dp_params_stack.addTab(lcs_widget, "LCS")  # Add the widget as a tab
        
        # Connect algorithm selection to parameter stack
        self.dp_algo_combo.currentIndexChanged.connect(self.dp_params_stack.setCurrentIndex)  # Switch parameter tab when algorithm changes
        
        params_layout.addWidget(self.dp_params_stack)  # Add the parameter stack to the layout
        
        # Run button
        run_group = QGroupBox("Run")  # Create a group box for run controls
        run_layout = QVBoxLayout(run_group)  # Create a vertical layout for the group box
        self.dp_run_btn = QPushButton("Run Algorithm")  # Create a button to run the algorithm
        self.dp_run_btn.clicked.connect(self.run_dp_algorithm)  # Connect it to the run_dp_algorithm method
        run_layout.addWidget(self.dp_run_btn)  # Add the button to the layout
        
        controls_layout.addWidget(algo_group)  # Add algorithm selection to controls layout
        controls_layout.addWidget(params_group)  # Add parameters to controls layout
        controls_layout.addWidget(run_group)  # Add run controls to controls layout
        
        layout.addLayout(controls_layout)  # Add the controls to the main layout
        
        # DP visualization area
        dp_viz_layout = QHBoxLayout()  # Create a horizontal layout for visualization
        
        # DP visualization panel
        dp_viz_group = QGroupBox("DP Visualization")  # Create a group box for visualization
        dp_viz_inner_layout = QVBoxLayout(dp_viz_group)  # Create a vertical layout for the group box
        
        self.dp_viz_text = QTextEdit()  # Create a text edit for displaying DP visualization
        self.dp_viz_text.setReadOnly(True)  # Make it read-only
        dp_viz_inner_layout.addWidget(self.dp_viz_text)  # Add it to the layout
        
        # DP metrics panel
        dp_metrics_group = QGroupBox("Performance Metrics")  # Create a group box for metrics
        dp_metrics_layout = QVBoxLayout(dp_metrics_group)  # Create a vertical layout for the group box
        
        self.dp_metrics_table = MetricsTable()  # Create a metrics table
        dp_metrics_layout.addWidget(self.dp_metrics_table)  # Add it to the layout
        
        dp_viz_layout.addWidget(dp_viz_group, 7)  # Add visualization with 70% width
        dp_viz_layout.addWidget(dp_metrics_group, 3)  # Add metrics with 30% width
        
        layout.addLayout(dp_viz_layout)  # Add the visualization layout to the main layout
        
        return tab  # Return the completed tab
    
    def create_greedy_tab(self):
        """Create the greedy algorithms tab"""
        tab = QWidget()  # Create a widget for this tab
        layout = QVBoxLayout(tab)  # Create a vertical layout for the tab
        
        # Controls
        controls_layout = QHBoxLayout()  # Create a horizontal layout for controls
        
        # Algorithm selection
        algo_group = QGroupBox("Algorithm")  # Create a group box for algorithm selection
        algo_layout = QVBoxLayout(algo_group)  # Create a vertical layout for the group box
        
        self.greedy_algo_combo = QComboBox()  # Create a combo box for selecting greedy algorithms
        self.greedy_algo_combo.addItems(self.greedy_algorithms.keys())  # Add the names of greedy algorithms
        algo_layout.addWidget(self.greedy_algo_combo)  # Add the combo box to the layout
        
        # Parameters for different greedy algorithms
        params_group = QGroupBox("Parameters")  # Create a group box for parameters
        params_layout = QVBoxLayout(params_group)  # Create a vertical layout for the group box
        
        self.greedy_params_stack = QTabWidget()  # Create a tab widget for different parameter sets
        
        # Activity Selection parameters
        activity_widget = QWidget()  # Create a widget for Activity Selection parameters
        activity_layout = QVBoxLayout(activity_widget)  # Create a vertical layout for the widget
        self.activity_start_input = QLineEdit()  # Create a line edit for start times
        self.activity_start_input.setPlaceholderText("Enter start times (comma-separated)")  # Set placeholder text
        activity_layout.addWidget(QLabel("Start Times:"))  # Add a label
        activity_layout.addWidget(self.activity_start_input)  # Add the line edit
        self.activity_end_input = QLineEdit()  # Create a line edit for end times
        self.activity_end_input.setPlaceholderText("Enter end times (comma-separated)")  # Set placeholder text
        activity_layout.addWidget(QLabel("End Times:"))  # Add a label
        activity_layout.addWidget(self.activity_end_input)  # Add the line edit
        self.greedy_params_stack.addTab(activity_widget, "Activity Selection")  # Add the widget as a tab
        
        # Coin Change parameters
        coin_widget = QWidget()  # Create a widget for Coin Change parameters
        coin_layout = QVBoxLayout(coin_widget)  # Create a vertical layout for the widget
        self.coin_denominations_input = QLineEdit()  # Create a line edit for coin denominations
        self.coin_denominations_input.setPlaceholderText("Enter coin denominations (comma-separated)")  # Set placeholder text
        coin_layout.addWidget(QLabel("Denominations:"))  # Add a label
        coin_layout.addWidget(self.coin_denominations_input)  # Add the line edit
        self.coin_amount_spin = QSpinBox()  # Create a spin box for the amount
        self.coin_amount_spin.setRange(1, 1000)  # Set the range (1-1000)
        self.coin_amount_spin.setValue(63)  # Set default value
        coin_layout.addWidget(QLabel("Amount:"))  # Add a label
        coin_layout.addWidget(self.coin_amount_spin)  # Add the spin box
        self.greedy_params_stack.addTab(coin_widget, "Coin Change")  # Add the widget as a tab
        
        # Huffman Coding parameters
        huffman_widget = QWidget()  # Create a widget for Huffman Coding parameters
        huffman_layout = QVBoxLayout(huffman_widget)  # Create a vertical layout for the widget
        self.huffman_text_input = QTextEdit()  # Create a text edit for the input text
        self.huffman_text_input.setPlaceholderText("Enter text to encode")  # Set placeholder text
        huffman_layout.addWidget(QLabel("Text:"))  # Add a label
        huffman_layout.addWidget(self.huffman_text_input)  # Add the text edit
        self.greedy_params_stack.addTab(huffman_widget, "Huffman Coding")  # Add the widget as a tab
        
        # Kruskal parameters
        kruskal_widget = QWidget()  # Create a widget for Kruskal parameters
        kruskal_layout = QVBoxLayout(kruskal_widget)  # Create a vertical layout for the widget
        self.kruskal_vertices_spin = QSpinBox()  # Create a spin box for number of vertices
        self.kruskal_vertices_spin.setRange(2, 10)  # Set the range (2-10)
        self.kruskal_vertices_spin.setValue(5)  # Set default value
        kruskal_layout.addWidget(QLabel("Vertices:"))  # Add a label
        kruskal_layout.addWidget(self.kruskal_vertices_spin)  # Add the spin box
        self.kruskal_edges_text = QTextEdit()  # Create a text edit for entering edges
        self.kruskal_edges_text.setPlaceholderText("Enter edges as 'u,v,weight' (one edge per line)")  # Set placeholder text
        kruskal_layout.addWidget(QLabel("Edges:"))  # Add a label
        kruskal_layout.addWidget(self.kruskal_edges_text)  # Add the text edit
        self.greedy_params_stack.addTab(kruskal_widget, "Kruskal")  # Add the widget as a tab
        
        # Connect algorithm selection to parameter stack
        self.greedy_algo_combo.currentIndexChanged.connect(self.greedy_params_stack.setCurrentIndex)  # Switch parameter tab when algorithm changes
        
        params_layout.addWidget(self.greedy_params_stack)  # Add the parameter stack to the layout
        
        # Run button
        run_group = QGroupBox("Run")  # Create a group box for run controls
        run_layout = QVBoxLayout(run_group)  # Create a vertical layout for the group box
        self.greedy_run_btn = QPushButton("Run Algorithm")  # Create a button to run the algorithm
        self.greedy_run_btn.clicked.connect(self.run_greedy_algorithm)  # Connect it to the run_greedy_algorithm method
        run_layout.addWidget(self.greedy_run_btn)  # Add the button to the layout
        
        controls_layout.addWidget(algo_group)  # Add algorithm selection to controls layout
        controls_layout.addWidget(params_group)  # Add parameters to controls layout
        controls_layout.addWidget(run_group)  # Add run controls to controls layout
        
        layout.addLayout(controls_layout)  # Add the controls to the main layout
        
        # Greedy visualization area
        greedy_viz_layout = QHBoxLayout()  # Create a horizontal layout for visualization
        
        # Greedy visualization panel
        greedy_viz_group = QGroupBox("Greedy Visualization")  # Create a group box for visualization
        greedy_viz_inner_layout = QVBoxLayout(greedy_viz_group)  # Create a vertical layout for the group box
        
        self.greedy_viz_text = QTextEdit()  # Create a text edit for displaying greedy visualization
        self.greedy_viz_text.setReadOnly(True)  # Make it read-only
        greedy_viz_inner_layout.addWidget(self.greedy_viz_text)  # Add it to the layout
        
        # Greedy metrics panel
        greedy_metrics_group = QGroupBox("Performance Metrics")  # Create a group box for metrics
        greedy_metrics_layout = QVBoxLayout(greedy_metrics_group)  # Create a vertical layout for the group box
        
        self.greedy_metrics_table = MetricsTable()  # Create a metrics table
        greedy_metrics_layout.addWidget(self.greedy_metrics_table)  # Add it to the layout
        
        greedy_viz_layout.addWidget(greedy_viz_group, 7)  # Add visualization with 70% width
        greedy_viz_layout.addWidget(greedy_metrics_group, 3)  # Add metrics with 30% width
        
        layout.addLayout(greedy_viz_layout)  # Add the visualization layout to the main layout
        
        return tab  # Return the completed tab

    def generate_list(self):
        """Generate a list based on user selection"""
        size = self.list_size_spin.value()  # Get the list size from the spin box
        
        if self.random_list_radio.isChecked():  # Check if random list option is selected
            self.current_array = [random.randint(1, 100) for _ in range(size)]  # Generate random integers between 1-100
        elif self.sorted_list_radio.isChecked():  # Check if sorted list option is selected
            self.current_array = list(range(1, size + 1))  # Generate a sorted list from 1 to size
        elif self.reverse_list_radio.isChecked():  # Check if reverse sorted option is selected
            self.current_array = list(range(size, 0, -1))  # Generate a reverse sorted list from size to 1
        elif self.custom_list_radio.isChecked():  # Check if custom list option is selected
            try:
                input_text = self.custom_list_input.text()  # Get the text from the custom input
                self.current_array = [int(x.strip()) for x in input_text.split(',')]  # Parse comma-separated integers
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter valid comma-separated integers.")  # Show error message
                return
        
        # Visualize the generated list
        self.array_viz.set_data(self.current_array)  # Update the array visualizer with the new list
        self.step_description.setText(f"Generated list: {self.current_array}")  # Display the generated list in the description
    
    def run_sort(self):
        """Run the selected sorting algorithm"""
        if not self.current_array:  # Check if there is a list to sort
            QMessageBox.warning(self, "No Data", "Please generate a list first.")  # Show error message
            return
        
        # Get selected algorithm
        algo_name = self.sort_algo_combo.currentText()  # Get the name of the selected algorithm
        self.current_algorithm = self.sort_algorithms[algo_name]  # Get the algorithm instance
        
        # Run the algorithm
        sorted_array = self.current_algorithm.sort(self.current_array)  # Sort the array using the selected algorithm
        
        # Get steps for visualization
        self.current_steps = self.current_algorithm.steps  # Get the steps recorded during sorting
        
        # Reset animation state
        self.current_step_index = 0  # Reset the step index to the beginning
        self.update_animation_controls(True)  # Update animation controls to initial state
        
        # Show initial state
        self.show_current_step()  # Display the first step
        
        # Update metrics
        metrics = self.current_algorithm.get_performance_metrics()  # Get performance metrics from the algorithm
        self.metrics_table.update_metrics(metrics)  # Update the metrics table
    
    def run_binary_search(self):
        """Run binary search on the sorted array"""
        # First check if we have a sorted array
        if not self.current_array:  # Check if there is a list to search
            QMessageBox.warning(self, "No Data", "Please generate and sort a list first.")  # Show error message
            return
        
        # Get target value
        try:
            target = int(self.search_input.text())  # Parse the target value as an integer
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid integer to search for.")  # Show error message
            return
        
        # Sort the array if not already sorted
        sorted_array = sorted(self.current_array)  # Sort the array (binary search requires sorted input)
        
        # Run binary search
        result = self.binary_search.search(sorted_array, target)  # Run binary search and get the result
        
        # Get steps for visualization
        self.current_steps = self.binary_search.steps  # Get the steps recorded during the search
        
        # Reset animation state
        self.current_step_index = 0  # Reset the step index to the beginning
        self.update_animation_controls(True)  # Update animation controls to initial state
        
        # Show initial state
        self.array_viz.set_data(sorted_array)  # Update the visualizer with the sorted array
        
        # Show result
        result_text = f"Target {target} found at index {result}" if result != -1 else f"Target {target} not found"  # Create result message
        self.step_description.setText(result_text)  # Display the result message
        
        # Update metrics
        metrics = {  # Create a dictionary of metrics
            "algorithm": "Binary Search",
            "comparisons": self.binary_search.comparisons,
            "execution_time": self.binary_search.execution_time
        }
        self.metrics_table.update_metrics(metrics)  # Update the metrics table
        
        # Show first step
        self.show_current_step()  # Display the first step
    
    def run_dp_algorithm(self):
        """Run the selected dynamic programming algorithm"""
        algo_name = self.dp_algo_combo.currentText()  # Get the name of the selected algorithm
        
        if algo_name == "Fibonacci":  # If Fibonacci is selected
            n = self.fib_n_spin.value()  # Get the value of n from the spin box
            result, metrics = self.dp_algorithms["Fibonacci"].compare_methods(n)  # Run both memoization and tabulation methods
            
            # Display results
            self.dp_viz_text.clear()  # Clear the visualization text
            self.dp_viz_text.append(f"Fibonacci({n}) = {result}\n")  # Display the result
            self.dp_viz_text.append("Memoization Steps:")  # Add header for memoization steps
            for step in metrics["memoization"]["steps"]:  # Loop through memoization steps
                self.dp_viz_text.append(str(step))  # Add each step to the visualization
            
            self.dp_viz_text.append("\nTabulation Steps:")  # Add header for tabulation steps
            for step in metrics["tabulation"]["steps"]:  # Loop through tabulation steps
                self.dp_viz_text.append(str(step))  # Add each step to the visualization
            
            # Update metrics
            self.dp_metrics_table.update_metrics({  # Update the metrics table with both methods' metrics
                "memo_operations": metrics["memoization"]["operations"],
                "memo_time": metrics["memoization"]["execution_time"],
                "memo_space": metrics["memoization"]["space_used"],
                "tab_operations": metrics["tabulation"]["operations"],
                "tab_time": metrics["tabulation"]["execution_time"],
                "tab_space": metrics["tabulation"]["space_used"]
            })
            
        elif algo_name == "Floyd Warshall":  # If Floyd-Warshall is selected
            vertices = self.fw_vertices_spin.value()  # Get the number of vertices from the spin box
            
            # Parse the graph input
            try:
                graph_text = self.fw_graph_text.toPlainText()  # Get the graph text
                if not graph_text:  # Generate random graph if empty
                    graph = [[float('inf') for _ in range(vertices)] for _ in range(vertices)]  # Initialize with infinity
                    # Add random edges
                    for i in range(vertices):
                        graph[i][i] = 0  # Distance to self is 0
                        for j in range(vertices):
                            if i != j and random.random() < 0.7:  # 70% chance of edge
                                graph[i][j] = random.randint(1, 10)  # Random weight between 1-10
                else:
                    rows = graph_text.strip().split('\n')  # Split into rows
                    graph = []  # Initialize graph
                    for row in rows:  # Process each row
                        values = []  # Initialize row values
                        for val in row.split(','):  # Process each value
                            val = val.strip()  # Remove whitespace
                            if val.upper() == 'INF':  # Handle infinity
                                values.append(float('inf'))
                            else:
                                values.append(float(val))  # Parse as float
                        graph.append(values)  # Add row to graph
                    
                    # Validate graph dimensions
                    if len(graph) != vertices or any(len(row) != vertices for row in graph):  # Check dimensions
                        raise ValueError("Graph dimensions do not match vertex count")  # Throw error if mismatch
                
                # Run the algorithm
                fw = self.dp_algorithms["Floyd Warshall"]  # Get the algorithm instance
                dist, pred = fw.solve(graph)  # Run the algorithm
                
                # Display results
                self.dp_viz_text.clear()  # Clear the visualization text
                self.dp_viz_text.append("Input Graph:")  # Add header for input graph
                self.dp_viz_text.append(fw.format_matrix(graph))  # Display formatted input graph
                
                self.dp_viz_text.append("\nDistance Matrix:")  # Add header for distance matrix
                self.dp_viz_text.append(fw.format_matrix(dist))  # Display formatted distance matrix
                
                self.dp_viz_text.append("\nPredecessor Matrix:")  # Add header for predecessor matrix
                self.dp_viz_text.append(fw.format_matrix(pred))  # Display formatted predecessor matrix
                
                # Show path examples
                self.dp_viz_text.append("\nSample Paths:")  # Add header for sample paths
                for i in range(min(3, vertices)):  # Loop through up to 3 source vertices
                    for j in range(min(3, vertices)):  # Loop through up to 3 destination vertices
                        if i != j:  # Skip paths to self
                            path = fw.get_path(pred, i, j)  # Get the path
                            path_str = " -> ".join(str(p) for p in path)  # Format the path
                            self.dp_viz_text.append(f"Path from {i} to {j}: {path_str}")  # Display the path
                
                # Update metrics
                self.dp_metrics_table.update_metrics({  # Update metrics table
                    "operations": fw.operations,
                    "execution_time": fw.execution_time,
                    "space_used": fw.space_used
                })
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error parsing graph: {str(e)}")  # Show error message
        
        elif algo_name == "Knapsack":  # If Knapsack is selected
            capacity = self.knapsack_capacity_spin.value()  # Get the capacity from the spin box
            
            try:
                weights_text = self.knapsack_weights_input.text()  # Get weights text
                values_text = self.knapsack_values_input.text()  # Get values text
                
                if not weights_text or not values_text:  # Generate random data if empty
                    n = 5  # Number of items
                    weights = [random.randint(1, 10) for _ in range(n)]  # Generate random weights
                    values = [random.randint(5, 50) for _ in range(n)]  # Generate random values
                    self.knapsack_weights_input.setText(",".join(str(w) for w in weights))  # Update weights input
                    self.knapsack_values_input.setText(",".join(str(v) for v in values))  # Update values input
                else:
                    weights = [int(w.strip()) for w in weights_text.split(',')]  # Parse weights
                    values = [int(v.strip()) for v in values_text.split(',')]  # Parse values
                
                # Validate input
                if len(weights) != len(values):  # Check if lengths match
                    raise ValueError("Weights and values must have the same length")  # Throw error if mismatch
                
                # Run the algorithm
                knapsack = self.dp_algorithms["Knapsack"]  # Get the algorithm instance
                results = knapsack.compare_knapsack_methods(weights, values, capacity)  # Compare 0/1 and fractional knapsack
                
                # Display results
                self.dp_viz_text.clear()  # Clear the visualization text
                self.dp_viz_text.append("Items:")  # Add header for items
                for i, (w, v) in enumerate(zip(weights, values)):  # Loop through items
                    self.dp_viz_text.append(f"Item {i}: Weight={w}, Value={v}")  # Display each item
                
                self.dp_viz_text.append(f"\nKnapsack Capacity: {capacity}")  # Display capacity
                
                self.dp_viz_text.append("\n0/1 Knapsack Result:")  # Add header for 0/1 knapsack results
                self.dp_viz_text.append(f"Max Value: {results['0/1']['value']}")  # Display max value
                self.dp_viz_text.append(f"Selected Items: {results['0/1']['items']}")  # Display selected items
                
                self.dp_viz_text.append("\nFractional Knapsack Result:")  # Add header for fractional knapsack results
                self.dp_viz_text.append(f"Max Value: {results['fractional']['value']}")  # Display max value
                self.dp_viz_text.append("Selected Items (index, fraction):")  # Add header for selected items
                for idx, frac in results['fractional']['items']:  # Loop through selected items
                    self.dp_viz_text.append(f"  Item {idx}: {frac:.2f}")  # Display each item and its fraction
                
                # Update metrics
                self.dp_metrics_table.update_metrics({  # Update metrics table for both methods
                    "0/1_operations": results['0/1']['metrics']['operations'],
                    "0/1_time": results['0/1']['metrics']['execution_time'],
                    "0/1_space": results['0/1']['metrics']['space_used'],
                    "frac_operations": results['fractional']['metrics']['operations'],
                    "frac_time": results['fractional']['metrics']['execution_time'],
                    "frac_space": results['fractional']['metrics']['space_used']
                })
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error with knapsack input: {str(e)}")  # Show error message
        
        elif algo_name == "LCS":  # If LCS is selected
            str1 = self.lcs_str1_input.text()  # Get the first string
            str2 = self.lcs_str2_input.text()  # Get the second string
            
            if not str1 or not str2:  # Check if both strings are provided
                QMessageBox.warning(self, "Invalid Input", "Please enter both strings.")  # Show error message
                return
            
            # Run the algorithm
            lcs = self.dp_algorithms["LCS"]  # Get the algorithm instance
            lcs_str, dp_table = lcs.find_lcs(str1, str2)  # Find the LCS
            
            # Display results
            self.dp_viz_text.clear()  # Clear the visualization text
            self.dp_viz_text.append(f"String 1: {str1}")  # Display first string
            self.dp_viz_text.append(f"String 2: {str2}")  # Display second string
            self.dp_viz_text.append(f"LCS: {lcs_str} (length: {len(lcs_str)})")  # Display LCS and its length
            
            # Show the alignment
            self.dp_viz_text.append("\nAlignment:")  # Add header for alignment
            alignment = lcs.print_lcs_alignment(str1, str2, lcs_str)  # Get the alignment visualization
            self.dp_viz_text.append(alignment)  # Display the alignment
            
            # Show DP table
            self.dp_viz_text.append("\nDP Table:")  # Add header for DP table
            for row in dp_table:  # Loop through each row
                self.dp_viz_text.append(" ".join(str(cell) for cell in row))  # Display formatted row
            
            # Update metrics
            self.dp_metrics_table.update_metrics({  # Update metrics table
                "operations": lcs.operations,
                "execution_time": lcs.execution_time,
                "space_used": lcs.space_used
            })

    def run_greedy_algorithm(self):
        """Run the selected greedy algorithm"""
        algo_name = self.greedy_algo_combo.currentText()  # Get the name of the selected algorithm
        
        if algo_name == "Activity Selection":  # If Activity Selection is selected
            try:
                start_text = self.activity_start_input.text()  # Get the start times text
                end_text = self.activity_end_input.text()  # Get the end times text
                
                if not start_text or not end_text:  # Generate random data if empty
                    n = 8  # Number of activities
                    # Generate non-overlapping activities
                    start_times = []  # Initialize start times list
                    end_times = []  # Initialize end times list
                    current_time = 0  # Start at time 0
                    
                    for _ in range(n):  # Generate n activities
                        duration = random.randint(1, 5)  # Random duration between 1-5
                        start_times.append(current_time)  # Add start time
                        current_time += duration  # Advance time by duration
                        end_times.append(current_time)  # Add end time
                        current_time += random.randint(0, 3)  # Add random gap between activities
                    
                    # Shuffle to make it interesting
                    combined = list(zip(start_times, end_times))  # Combine start and end times
                    random.shuffle(combined)  # Shuffle the activities
                    start_times, end_times = zip(*combined)  # Unzip the shuffled activities
                    
                    self.activity_start_input.setText(",".join(str(s) for s in start_times))  # Update start times input
                    self.activity_end_input.setText(",".join(str(e) for e in end_times))  # Update end times input
                else:
                    start_times = [int(s.strip()) for s in start_text.split(',')]  # Parse start times
                    end_times = [int(e.strip()) for e in end_text.split(',')]  # Parse end times
                
                # Validate input
                if len(start_times) != len(end_times):  # Check if lengths match
                    raise ValueError("Start times and end times must have the same length")  # Throw error if mismatch
                
                # Run the algorithm
                activity = self.greedy_algorithms["Activity Selection"]  # Get the algorithm instance
                results = activity.compare_approaches(start_times, end_times)  # Compare greedy and DP approaches
                
                # Display results
                self.greedy_viz_text.clear()  # Clear the visualization text
                self.greedy_viz_text.append("Activities:")  # Add header for activities
                for i, (s, e) in enumerate(zip(start_times, end_times)):  # Loop through activities
                    self.greedy_viz_text.append(f"Activity {i}: ({s}-{e})")  # Display each activity
                
                self.greedy_viz_text.append("\nGreedy Approach Result:")  # Add header for greedy results
                self.greedy_viz_text.append(f"Selected activities: {results['greedy']['selected']}")  # Display selected activities
                self.greedy_viz_text.append(f"Total activities selected: {results['greedy']['count']}")  # Display count
                
                self.greedy_viz_text.append("\nDP Approach Result:")  # Add header for DP results
                self.greedy_viz_text.append(f"Selected activities: {results['dp']['selected']}")  # Display selected activities
                self.greedy_viz_text.append(f"Total activities selected: {results['dp']['count']}")  # Display count
                
                # Show steps
                self.greedy_viz_text.append("\nGreedy Steps:")  # Add header for greedy steps
                for step in results['greedy']['metrics']['steps']:  # Loop through steps
                    self.greedy_viz_text.append(str(step))  # Display each step
                
                # Update metrics
                self.greedy_metrics_table.update_metrics({  # Update metrics table for both approaches
                    "greedy_operations": results['greedy']['metrics']['operations'],
                    "greedy_time": results['greedy']['metrics']['execution_time'],
                    "dp_operations": results['dp']['metrics']['operations'],
                    "dp_time": results['dp']['metrics']['execution_time']
                })
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error with activity selection input: {str(e)}")  # Show error message
        
        elif algo_name == "Coin Change":  # If Coin Change is selected
            try:
                amount = self.coin_amount_spin.value()  # Get the amount from the spin box
                coins_text = self.coin_denominations_input.text()  # Get the coin denominations text
                
                if not coins_text:  # Default to US coins if empty
                    coins = [1, 5, 10, 25, 50]  # US coin denominations
                    self.coin_denominations_input.setText(",".join(str(c) for c in coins))  # Update input
                else:
                    coins = [int(c.strip()) for c in coins_text.split(',')]  # Parse coin denominations
                
                # Run the algorithm
                coin_change = self.greedy_algorithms["Coin Change"]  # Get the algorithm instance
                results = coin_change.compare_approaches(coins, amount)  # Compare greedy and DP approaches
                
                # Display results
                self.greedy_viz_text.clear()  # Clear the visualization text
                self.greedy_viz_text.append(f"Amount: {amount}")  # Display the amount
                self.greedy_viz_text.append(f"Coin denominations: {coins}")  # Display coin denominations
                
                self.greedy_viz_text.append("\nGreedy Approach Result:")  # Add header for greedy results
                if results['greedy']['count'] == -1:  # Check if no solution was found
                    self.greedy_viz_text.append("No solution found")  # Display no solution message
                else:
                    self.greedy_viz_text.append(f"Coins used: {results['greedy']['coins']}")  # Display coins used
                    self.greedy_viz_text.append(f"Total coins: {results['greedy']['count']}")  # Display total coins
                
                self.greedy_viz_text.append("\nDP Approach Result:")  # Add header for DP results
                if results['dp']['count'] == -1:  # Check if no solution was found
                    self.greedy_viz_text.append("No solution found")  # Display no solution message
                else:
                    self.greedy_viz_text.append(f"Coins used: {results['dp']['coins']}")  # Display coins used
                    self.greedy_viz_text.append(f"Total coins: {results['dp']['count']}")  # Display total coins
                
                # Show steps
                self.greedy_viz_text.append("\nGreedy Steps:")  # Add header for greedy steps
                for step in results['greedy']['metrics']['steps']:  # Loop through steps
                    self.greedy_viz_text.append(str(step))  # Display each step
                
                # Update metrics
                self.greedy_metrics_table.update_metrics({  # Update metrics table for both approaches
                    "greedy_operations": results['greedy']['metrics']['operations'],
                    "greedy_time": results['greedy']['metrics']['execution_time'],
                    "dp_operations": results['dp']['metrics']['operations'],
                    "dp_time": results['dp']['metrics']['execution_time']
                })
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error with coin change input: {str(e)}")  # Show error message
        
        elif algo_name == "Huffman Coding":  # If Huffman Coding is selected
            text = self.huffman_text_input.toPlainText()  # Get the input text
            
            if not text:  # Check if text is provided
                QMessageBox.warning(self, "Invalid Input", "Please enter text to encode.")  # Show error message
                return
            
            # Run the algorithm
            huffman = self.greedy_algorithms["Huffman Coding"]  # Get the algorithm instance
            huffman.build_huffman_tree(text)  # Build the Huffman tree
            encoded_text, codes = huffman.encode(text)  # Encode the text
            decoded_text = huffman.decode(encoded_text, huffman.huffman_tree)  # Decode the text
            ratio = huffman.calculate_compression_ratio(text, encoded_text)  # Calculate compression ratio
            
            # Display results
            self.greedy_viz_text.clear()  # Clear the visualization text
            self.greedy_viz_text.append(f"Original text: {text}")  # Display original text
            self.greedy_viz_text.append(f"Text length: {len(text)} characters")  # Display text length
            
            self.greedy_viz_text.append("\nHuffman Codes:")  # Add header for Huffman codes
            for char, code in sorted(codes.items()):  # Loop through codes sorted by character
                self.greedy_viz_text.append(f"'{char}': {code}")  # Display each character's code
            
            self.greedy_viz_text.append(f"\nEncoded text: {encoded_text}")  # Display encoded text
            self.greedy_viz_text.append(f"Encoded length: {len(encoded_text)} bits")  # Display encoded length
            
            self.greedy_viz_text.append(f"\nDecoded text: {decoded_text}")  # Display decoded text
            self.greedy_viz_text.append(f"Compression ratio: {ratio:.2f}x")  # Display compression ratio
            
            # Show tree structure
            tree_dict = huffman.get_tree_as_dict()  # Get the tree as a dictionary
            self.greedy_viz_text.append("\nHuffman Tree Structure:")  # Add header for tree structure
            for path, node_info in tree_dict.items():  # Loop through nodes
                char_display = f"'{node_info['char']}'" if node_info['char'] else 'Internal'  # Format character display
                self.greedy_viz_text.append(f"Path: {path}, {char_display}, Freq: {node_info['freq']}")  # Display node info
            
            # Update metrics
            self.greedy_metrics_table.update_metrics({  # Update metrics table
                "operations": huffman.operations,
                "execution_time": huffman.execution_time,
                "original_size": len(text) * 8,  # Assuming 8 bits per character
                "compressed_size": len(encoded_text),
                "compression_ratio": ratio
            })
        
        elif algo_name == "Kruskal":  # If Kruskal's algorithm is selected
            vertices = self.kruskal_vertices_spin.value()  # Get the number of vertices from the spin box
            
            try:
                edges_text = self.kruskal_edges_text.toPlainText()  # Get the edges text
                
                if not edges_text:  # Generate random graph if empty
                    edges = []  # Initialize edges list
                    # Generate random edges
                    for u in range(vertices):  # Loop through vertices
                        for v in range(u+1, vertices):  # Consider only upper triangular part for undirected graph
                            if random.random() < 0.7:  # 70% chance of edge
                                weight = random.randint(1, 20)  # Random weight between 1-20
                                edges.append((u, v, weight))  # Add the edge
                    
                    # Generate edge text
                    edge_lines = [f"{u},{v},{w}" for u, v, w in edges]  # Format each edge
                    self.kruskal_edges_text.setPlainText("\n".join(edge_lines))  # Update edges text
                else:
                    edges = []  # Initialize edges list
                    for line in edges_text.strip().split('\n'):  # Process each line
                        u, v, w = map(int, line.split(','))  # Parse edge data
                        edges.append((u, v, w))  # Add the edge
                
                # Run the algorithm
                kruskal = self.greedy_algorithms["Kruskal"]  # Get the algorithm instance
                
                # Check if graph is connected
                if not kruskal.is_connected(vertices, edges):  # Check if graph is connected
                    self.greedy_viz_text.clear()  # Clear the visualization text
                    self.greedy_viz_text.append("Warning: The graph is not connected. MST will be incomplete.")  # Show warning
                
                mst = kruskal.find_mst(vertices, edges)  # Find the minimum spanning tree
                mst_weight = kruskal.calculate_mst_weight(mst)  # Calculate the total weight
                
                # Display results
                self.greedy_viz_text.clear()  # Clear the visualization text
                self.greedy_viz_text.append(f"Graph has {vertices} vertices and {len(edges)} edges")  # Display graph info
                
                self.greedy_viz_text.append("\nInput Edges:")  # Add header for input edges
                for u, v, w in edges:  # Loop through edges
                    self.greedy_viz_text.append(f"Edge ({u}-{v}) with weight {w}")  # Display each edge
                
                self.greedy_viz_text.append("\nMinimum Spanning Tree:")  # Add header for MST
                for u, v, w in mst:  # Loop through MST edges
                    self.greedy_viz_text.append(f"Edge ({u}-{v}) with weight {w}")  # Display each edge
                
                self.greedy_viz_text.append(f"\nTotal MST weight: {mst_weight}")  # Display total MST weight
                
                # Show steps
                self.greedy_viz_text.append("\nKruskal's Algorithm Steps:")  # Add header for steps
                for step_type, edge, mst_edges in kruskal.steps:  # Loop through steps
                    if step_type == "init":  # Initial step
                        self.greedy_viz_text.append(f"Initial edges: {edge}")  # Display initial edges
                    elif step_type == "sort":  # Sort step
                        self.greedy_viz_text.append(f"Sorted edges by weight: {edge}")  # Display sorted edges
                    elif step_type == "add":  # Add edge step
                        self.greedy_viz_text.append(f"Added edge {edge} to MST")  # Display added edge
                    elif step_type == "skip":  # Skip edge step
                        self.greedy_viz_text.append(f"Skipped edge {edge} (would create cycle)")  # Display skipped edge
                    elif step_type == "final":  # Final step
                        self.greedy_viz_text.append(f"Final MST: {mst_edges}")  # Display final MST
                
                # Update metrics
                self.greedy_metrics_table.update_metrics({  # Update metrics table
                    "operations": kruskal.operations,
                    "execution_time": kruskal.execution_time,
                    "input_edges": len(edges),
                    "mst_edges": len(mst),
                    "mst_weight": mst_weight
                })
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error with Kruskal MST input: {str(e)}")  # Show error message
    
    def show_current_step(self):
        """Show the current step in the animation"""
        if not self.current_steps or self.current_step_index >= len(self.current_steps):  # Check if we have valid steps
            return
        
        step = self.current_steps[self.current_step_index]  # Get the current step
        step_type = step[0]  # Get the step type
        
        # For sorting visualization
        if step_type in ("initial", "final", "swap", "assign", "heapify", "merge", "partition"):  # Check if it's a sorting step
            i, j, arr = step[1], step[2], step[3]  # Extract step data
            
            # Highlight indices involved in the operation
            highlights = {}  # Initialize empty highlights dictionary
            if i >= 0:  # If i is valid
                highlights[i] = 'red'  # Highlight i in red
            if j >= 0:  # If j is valid
                highlights[j] = 'green'  # Highlight j in green
                
            self.array_viz.set_data(arr, highlights)  # Update the visualization
            
            # Update description
            if step_type == "initial":  # Initial step
                desc = "Initial array"  # Set description
            elif step_type == "final":  # Final step
                desc = "Final sorted array"  # Set description
            elif step_type == "swap":  # Swap step
                desc = f"Swap elements at indices {i} and {j}"  # Set description
            elif step_type == "assign":  # Assign step
                desc = f"Assign value {j} to index {i}"  # Set description
            elif step_type == "heapify":  # Heapify step
                desc = f"Heapify: adjust subtree rooted at {i}, largest is {j}"  # Set description
            elif step_type == "merge":  # Merge step
                desc = f"Merge subarrays from index {i} to {j}"  # Set description
            elif step_type == "partition":  # Partition step
                desc = f"Partition array from index {i} to {j}"  # Set description
            
            self.step_description.setText(desc)  # Update the step description
        
        # For binary search visualization
        elif step_type in ("search", "found", "left", "right"):  # Check if it's a binary search step
            left, right, arr = step[1], step[2], step[3]  # Extract step data
            
            # Highlight current search range
            highlights = {}  # Initialize empty highlights dictionary
            if left >= 0 and right >= 0:  # If we have a valid range
                mid = (left + right) // 2  # Calculate middle
                for i in range(left, right + 1):  # Loop through range
                    highlights[i] = 'lightblue'  # Highlight range in light blue
                highlights[mid] = 'red'  # Highlight middle element in red
            elif left >= 0:  # Found case
                highlights[left] = 'green'  # Highlight found element in green
            
            self.array_viz.set_data(arr, highlights)  # Update the visualization
            
            # Update description
            if step_type == "search":  # Search step
                desc = f"Searching in range [{left}, {right}]"  # Set description
            elif step_type == "found":  # Found step
                desc = f"Found target at index {left}"  # Set description
            elif step_type == "left":  # Left search step
                desc = f"Target is in left half, search range [{left}, {right}]"  # Set description
            elif step_type == "right":  # Right search step
                desc = f"Target is in right half, search range [{left}, {right}]"  # Set description
            
            self.step_description.setText(desc)  # Update the step description
    
    def show_next_step(self):
        """Show the next step in the animation"""
        if self.current_step_index < len(self.current_steps) - 1:  # Check if we're not at the last step
            self.current_step_index += 1  # Increment step index
            self.show_current_step()  # Show the updated step
            self.update_animation_controls()  # Update animation controls
    
    def show_previous_step(self):
        """Show the previous step in the animation"""
        if self.current_step_index > 0:  # Check if we're not at the first step
            self.current_step_index -= 1  # Decrement step index
            self.show_current_step()  # Show the updated step
            self.update_animation_controls()  # Update animation controls
    
    def play_animation(self):
        """Start or stop the animation playback"""
        if self.animation_timer.isActive():  # Check if the animation is already running
            self.animation_timer.stop()  # Stop the animation timer
            self.play_btn.setText("Play")  # Change button text to "Play"
        else:
            self.animation_timer.start(self.animation_speed)  # Start the animation timer with current speed
            self.play_btn.setText("Pause")  # Change button text to "Pause"
    
    def animation_step(self):
        """Advance animation by one step"""
        if self.current_step_index < len(self.current_steps) - 1:  # Check if we're not at the last step
            self.show_next_step()  # Show the next step
        else:
            self.animation_timer.stop()  # Stop the animation if we've reached the end
            self.play_btn.setText("Play")  # Reset the play button text
    
    def reset_animation(self):
        """Reset the animation to the beginning"""
        self.current_step_index = 0  # Reset the step index to 0
        self.show_current_step()  # Show the first step
        self.update_animation_controls()  # Update animation controls
        
        if self.animation_timer.isActive():  # Check if animation is active
            self.animation_timer.stop()  # Stop the animation
            self.play_btn.setText("Play")  # Reset the play button text
    
    def update_animation_controls(self, just_started=False):
        """Update the state of animation control buttons"""
        has_steps = len(self.current_steps) > 0  # Check if we have steps
        at_start = self.current_step_index == 0  # Check if we're at the beginning
        at_end = self.current_step_index >= len(self.current_steps) - 1  # Check if we're at the end
        
        self.prev_step_btn.setEnabled(has_steps and not at_start)  # Enable previous button if not at start
        self.next_step_btn.setEnabled(has_steps and not at_end)  # Enable next button if not at end
        self.play_btn.setEnabled(has_steps and not at_end)  # Enable play button if not at end
        self.reset_btn.setEnabled(has_steps and (not at_start or just_started))  # Enable reset button if not at start
    
    def update_animation_speed(self):
        """Update animation speed based on slider value"""
        # Convert slider value (1-10) to delay in ms (1000-100)
        self.animation_speed = 1100 - (self.speed_slider.value() * 100)  # Calculate speed from slider
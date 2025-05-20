import matplotlib.pyplot as plt  # Import matplotlib for creating plots
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # Import Qt canvas for embedding matplotlib in Qt applications

class ArrayVisualizer(FigureCanvas):
    """Widget for visualizing arrays/lists with matplotlib"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)  # Create a new figure and axis with specified dimensions
        super().__init__(self.fig)  # Initialize the parent FigureCanvas with our figure
        self.setParent(parent)  # Set the parent widget for Qt integration
        self.data = []  # Initialize empty list to store data to be visualized
        self.highlights = {}  # Initialize empty dictionary to store highlighted indices and their colors

    def set_data(self, data, highlights=None):
        self.data = data  # Set the data to be visualized
        self.highlights = {} if highlights is None else highlights  # Set highlights (or empty dict if None)
        self.plot()  # Update the plot with new data

    def plot(self):
        self.ax.clear()  # Clear the previous plot
        if not self.data:  # If there's no data to plot
            return  # Exit without doing anything

        bars = self.ax.bar(range(len(self.data)), self.data, color='skyblue')  # Create bar chart with indices as x-values and data as heights

        for idx, color in self.highlights.items():  # Iterate through highlighted indices and their colors
            if 0 <= idx < len(bars):  # Check if index is valid
                bars[idx].set_color(color)  # Set the color of the highlighted bar

        self.ax.set_xlabel('Index')  # Set x-axis label
        self.ax.set_ylabel('Value')  # Set y-axis label
        self.ax.set_xticks(range(len(self.data)))  # Set x-axis ticks to show indices
        self.fig.tight_layout()  # Adjust layout to prevent clipping of labels
        self.draw()  # Render the updated plot
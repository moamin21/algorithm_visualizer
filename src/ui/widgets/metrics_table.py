from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem  # Import Qt widgets for creating tables

class MetricsTable(QTableWidget):
    """Widget for displaying algorithm performance metrics"""

    def __init__(self, parent=None):
        super().__init__(parent)  # Initialize the parent QTableWidget
        self.setColumnCount(2)  # Set the table to have 2 columns
        self.setHorizontalHeaderLabels(['Metric', 'Value'])  # Set column headers
        self.horizontalHeader().setStretchLastSection(True)  # Make the last column stretch to fill available space
        self.verticalHeader().setVisible(False)  # Hide the vertical header (row numbers)

    def update_metrics(self, metrics):
        self.setRowCount(0)  # Clear all existing rows
        for i, (key, value) in enumerate(metrics.items()):  # Iterate through metrics key-value pairs
            self.insertRow(i)  # Insert a new row for this metric
            self.setItem(i, 0, QTableWidgetItem(str(key)))  # Set the first column to the metric name
            self.setItem(i, 1, QTableWidgetItem(str(value)))  # Set the second column to the metric value
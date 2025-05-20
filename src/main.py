import sys  # Import the sys module for system-specific parameters and functions
from PyQt5.QtWidgets import QApplication  # Import QApplication class to create the Qt application
from ui.main_window import AlgorithmVisualizer  # Import our custom main window class

def main():
    app = QApplication(sys.argv)  # Create a new Qt application instance with command line arguments
    window = AlgorithmVisualizer()  # Create an instance of our main window
    window.show()  # Display the main window
    sys.exit(app.exec_())  # Start the application's event loop and exit with its return code

if __name__ == "__main__":  # Check if this script is being run directly (not imported)
    main()  # Call the main function to start the application
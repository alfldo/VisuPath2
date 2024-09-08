import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QComboBox, QPushButton, QLabel
from PySide6.QtCore import Qt
from visualization.visualizer import Visualizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.visualizer = Visualizer()
        self.setWindowTitle("Algorithm Visualizer")
        self.setGeometry(100, 100, 800, 600)
        
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        self.algorithm_info = {
            'sorting': {
                "Bubble Sort": "Bubble Sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
                "Quick Sort": "Quick Sort is a divide-and-conquer algorithm that works by selecting a 'pivot' element from the array and partitioning the other elements into two sub-arrays, according to whether they are less than or greater than the pivot.",
                "Merge Sort": "Merge Sort is a divide-and-conquer algorithm that divides the array into two halves, sorts them, and then merges them back together."
            },
            'graph': {
                "BFS": "Breadth-First Search (BFS) is an algorithm for traversing or searching tree or graph data structures.",
                "DFS": "Depth-First Search (DFS) is an algorithm for traversing or searching tree or graph data structures."
            },
            'tree': {
                "Dijkstra": "Dijkstra's algorithm is a graph search algorithm that finds the shortest path between nodes in a graph."
            }
        }
        
        self.setup_tabs()
    
    def setup_tabs(self):
        # Define tab configurations
        tabs = {
            'Sorting Algorithms': ('sorting', ["Bubble Sort", "Quick Sort", "Merge Sort"]),
            'Graph Algorithms': ('graph', ["BFS", "DFS"]),
            'Tree Algorithms': ('tree', ["Dijkstra"])
        }
        
        # Setup each tab
        for tab_name, (category, algorithms) in tabs.items():
            self.create_tab(tab_name, category, algorithms)
        
        # Connect tab change event to update run button state
        self.tab_widget.currentChanged.connect(self.update_run_button_state)
    
    def create_tab(self, tab_name, category, algorithms):
        tab = QWidget()
        layout = QVBoxLayout()
        
        combo = QComboBox()
        combo.addItems(algorithms)
        combo.currentIndexChanged.connect(lambda index: self.update_info(category, combo.currentText()))
        
        info_label = QLabel(f"Select a {tab_name.lower()} to see information")
        run_button = QPushButton("Run")
        run_button.clicked.connect(lambda: self.run_algorithm(category, combo.currentIndex()))
        run_button.setEnabled(False)  # Initially disable the run button
        
        # Store references to the combo box and info label for updates
        setattr(self, f'{category}_combo', combo)
        setattr(self, f'{category}_info_label', info_label)
        setattr(self, f'{category}_run_button', run_button)
        
        layout.addWidget(combo)
        layout.addWidget(info_label)
        layout.addWidget(run_button)
        tab.setLayout(layout)
        
        self.tab_widget.addTab(tab, tab_name)
    
    def update_info(self, category, selected_algorithm):
        info = self.algorithm_info.get(category, {}).get(selected_algorithm, "No information available")
        getattr(self, f'{category}_info_label').setText(info)
    
    def update_run_button_state(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_tab_category = list(self.algorithm_info.keys())[current_tab_index]
        combo = getattr(self, f'{current_tab_category}_combo')
        run_button = getattr(self, f'{current_tab_category}_run_button')
        run_button.setEnabled(combo.currentIndex() != -1)
    
    def run_algorithm(self, category, index):
        algorithms = {
            'sorting': ["bubble_sort", "quick_sort", "merge_sort"],
            'graph': ["bfs", "dfs"],
            'tree': ["dijkstra"]
        }
        
        selected_algorithm = algorithms[category][index]
        is_sorting = category == 'sorting'
        is_tree = category == 'tree'
        
        self.visualizer.visualize_algorithm(selected_algorithm, is_sorting=is_sorting, is_tree=is_tree)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

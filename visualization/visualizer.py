from visualization.sortingvisualizer import SortingVisualizer
from visualization.graphvisualizer import GraphVisualizer
from visualization.treevisualizer import TreeVisualizer

class Visualizer:
    def __init__(self):
        self.sorting_visualizer = SortingVisualizer()
        self.graph_visualizer = GraphVisualizer()
        self.tree_visualizer = TreeVisualizer()
    
    def visualize_algorithm(self, algorithm_type, is_sorting=True, is_tree=False):
        if is_sorting:
            self.sorting_visualizer.visualize_algorithm(algorithm_type)
        elif is_tree:
            self.tree_visualizer.visualize_algorithm(algorithm_type)
        else:
            self.graph_visualizer.visualize_algorithm(algorithm_type)

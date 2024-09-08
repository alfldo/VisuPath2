import pygame
import sys
import threading
import random
import time
from algorithms.tree.dijkstra import dijkstra

class TreeVisualizer:
    def __init__(self):
        self.pygame_thread = None
        self.visualization_thread = None
        self.run_visualization = True
        self.graph = {}
        self.COLORS = {
            "background": (245, 245, 245),  # Light gray
            "default": (74, 144, 226),      # Soft blue
            "highlight": (245, 166, 35),    # Soft orange
            "path": (126, 211, 33)          # Light green
        }
        self.algorithm_function = None
        self.lock = threading.Lock()
        self.pygame_initialized = False

    def visualize_algorithm(self, algorithm_type):
        if self.pygame_thread and self.pygame_thread.is_alive():
            pygame.quit()
            self.pygame_thread.join()

        self.run_visualization = True
        self.pygame_thread = threading.Thread(target=self._run_pygame_window, args=(algorithm_type,))
        self.pygame_thread.start()

    def _run_pygame_window(self, algorithm_type):
        pygame.init()
        self.pygame_initialized = True
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Tree Algorithm Visualization")

        # Define a simple tree graph for demonstration purposes
        self.graph = {
            0: {1: 10, 2: 15},
            1: {3: 12, 4: 15},
            2: {5: 10},
            3: {},
            4: {},
            5: {}
        }

        self.algorithm_function = {
            "dijkstra": dijkstra
        }.get(algorithm_type)

        # Initial draw
        screen.fill(self.COLORS["background"])
        self._draw_tree(screen, self.graph, self.COLORS["default"])
        pygame.display.flip()

        # Algorithm thread start
        if self.algorithm_function:
            self.visualization_thread = threading.Thread(target=self._algorithm_data, args=(screen,))
            self.visualization_thread.start()

        # Pygame main loop
        while self.run_visualization:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_visualization = False
            self._handle_events(screen)

        pygame.quit()
        self.pygame_initialized = False
        sys.exit()

    def _algorithm_data(self, screen):
        def update(path, current):
            if not self.pygame_initialized:
                return
            with self.lock:
                if self.run_visualization:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"path": path, "current": current}))
                    time.sleep(0.5)  # Update screen every 0.5 seconds

        start_node = 0
        self.algorithm_function(self.graph, start_node, callback=update)
        if self.pygame_initialized:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"path": [], "current": None}))

    def _handle_events(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self._update_screen(screen, event.dict["path"], event.dict["current"])
            elif event.type == pygame.QUIT:
                self.run_visualization = False

    def _update_screen(self, screen, path, current):
        if not self.pygame_initialized:
            return
        screen.fill(self.COLORS["background"])
        self._draw_tree(screen, self.graph, self.COLORS["default"], path, current)
        pygame.display.flip()

    def _draw_tree(self, screen, graph, color, path=[], current=None):
        positions = {
            0: (400, 50),
            1: (300, 200),
            2: (500, 200),
            3: (200, 350),
            4: (400, 350),
            5: (600, 350)
        }
        radius = 20
        for node, edges in graph.items():
            x, y = positions[node]
            pygame.draw.circle(screen, color, (x, y), radius)
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(node), True, (0, 0, 0))
            screen.blit(text, (x - radius // 2, y - radius // 2))
            if node == current:
                pygame.draw.circle(screen, self.COLORS["highlight"], (x, y), radius)
            for dest, weight in edges.items():
                dest_x, dest_y = positions[dest]
                pygame.draw.line(screen, color, (x, y), (dest_x, dest_y), 2)
                mid_point = ((x + dest_x) // 2, (y + dest_y) // 2)
                font = pygame.font.SysFont(None, 18)
                text = font.render(str(weight), True, (0, 0, 0))
                screen.blit(text, (mid_point[0] - 10, mid_point[1] - 10))
        
        if path:
            for i in range(len(path) - 1):
                start_pos = positions[path[i]]
                end_pos = positions[path[i + 1]]
                pygame.draw.line(screen, self.COLORS["path"], start_pos, end_pos, 4)

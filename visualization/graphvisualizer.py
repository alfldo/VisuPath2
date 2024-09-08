import pygame
import sys
import threading
import time
import random
from algorithms.graph.dfs import dfs
from algorithms.graph.bfs import bfs

def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]

    def carve_path(x, y):
        maze[y][x] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                if dx == 0:
                    maze[(y + ny) // 2][x] = 0
                else:
                    maze[y][(x + nx) // 2] = 0
                carve_path(nx, ny)

    start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)
    carve_path(start_x, start_y)
    return maze, (start_x, start_y), (width - 2, height - 2)


class GraphVisualizer:
    def __init__(self):
        self.pygame_thread = None
        self.algorithm_thread = None
        self.run_visualization = True
        self.COLORS = {
            "background": (245, 245, 245),
            "wall": (0, 0, 0),
            "path": (245, 166, 35),
            "visited": (126, 211, 33),
            "start": (0, 255, 0),
            "end": (255, 0, 0)
        }
        self.algorithm_function = None
        self.lock = threading.Lock()
        self.pygame_initialized = False
        self.maze, self.start_node, self.target_node = generate_maze(31, 31)

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
        self.cell_size = 20
        self.screen_width = len(self.maze[0]) * self.cell_size
        self.screen_height = len(self.maze) * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Maze Algorithm Visualization")

        self.algorithm_function = {
            "bfs": bfs,
            "dfs": dfs
        }.get(algorithm_type)

        self.screen.fill(self.COLORS["background"])
        self._draw_maze()
        pygame.display.flip()

        if self.algorithm_function:
            self.algorithm_thread = threading.Thread(target=self._run_algorithm)
            self.algorithm_thread.start()

        clock = pygame.time.Clock()
        while self.run_visualization:
            self._handle_events()
            clock.tick(10)  # Control the frame rate here, 10 frames per second

        pygame.quit()
        self.pygame_initialized = False
        sys.exit()

    def _run_algorithm(self):
        def update(visited_nodes, path):
            if not self.pygame_initialized:
                return
            with self.lock:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"visited": visited_nodes, "path": path}))

        path = self.algorithm_function(self.maze, self.start_node, self.target_node, callback=update)
        if path:
            # Draw the final path
            for step in path:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"visited": set([step]), "path": [step]}))

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                visited = event.dict["visited"]
                path = event.dict["path"]
                self._update_screen(visited, path)
            elif event.type == pygame.QUIT:
                self.run_visualization = False

    def _update_screen(self, visited, path):
        if not self.pygame_initialized:
            return
        self.screen.fill(self.COLORS["background"])
        self._draw_maze(visited, path)
        pygame.display.flip()

    def _draw_maze(self, visited=set(), path=[]):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if cell == 1:
                    pygame.draw.rect(self.screen, self.COLORS["wall"], rect)
                elif (x, y) == self.start_node:
                    pygame.draw.rect(self.screen, self.COLORS["start"], rect)
                elif (x, y) == self.target_node:
                    pygame.draw.rect(self.screen, self.COLORS["end"], rect)
                elif (x, y) in visited:
                    pygame.draw.rect(self.screen, self.COLORS["visited"], rect)
                if (x, y) in path:
                    pygame.draw.rect(self.screen, self.COLORS["path"], rect)

        for step in path:
            pygame.draw.rect(self.screen, self.COLORS["path"], pygame.Rect(step[0] * self.cell_size, step[1] * self.cell_size, self.cell_size, self.cell_size))


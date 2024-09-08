import pygame
import sys
import threading
import random
import time
from algorithms.sorting.bubblesort import bubble_sort
from algorithms.sorting.quicksort import quick_sort
from algorithms.sorting.mergesort import merge_sort

class SortingVisualizer:
    def __init__(self):
        self.pygame_thread = None
        self.sort_thread = None
        self.run_visualization = True
        self.data = []
        self.sorted_data = []
        self.COLORS = {
            "background": (245, 245, 245),
            "default": (74, 144, 226),
            "comparison": (245, 166, 35),
            "sorted": (126, 211, 33)
        }
        self.sort_function = None
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
        pygame.display.set_caption("Sorting Algorithm Visualization")

        self.data = [random.randint(10, 500) for _ in range(40)]
        self.sorted_data = self.data.copy()
        self.sort_function = {
            "bubble_sort": bubble_sort,
            "quick_sort": quick_sort,
            "merge_sort": merge_sort
        }.get(algorithm_type)

        screen.fill(self.COLORS["background"])
        self._draw_bars(screen, self.data, self.COLORS["default"])
        pygame.display.flip()

        if self.sort_function:
            self.sort_thread = threading.Thread(target=self._sort_data, args=(screen,))
            self.sort_thread.start()

        while self.run_visualization:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_visualization = False
            self._handle_events(screen)

        pygame.quit()
        self.pygame_initialized = False
        sys.exit()

    def _sort_data(self, screen):
        def update(arr, i, j):
            if not self.pygame_initialized:
                return
            with self.lock:
                if self.run_visualization:
                    self.sorted_data = arr.copy()
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"data": arr, "i": i, "j": j}))
                    time.sleep(0.05)

        self.sort_function(self.data, callback=update)
        if self.pygame_initialized:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"data": self.sorted_data, "i": None, "j": None}))

    def _handle_events(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self._update_screen(screen, event.dict["data"], event.dict["i"], event.dict["j"])
            elif event.type == pygame.QUIT:
                self.run_visualization = False

    def _update_screen(self, screen, data, i, j):
        if not self.pygame_initialized:
            return
        screen.fill(self.COLORS["background"])
        for idx, value in enumerate(data):
            color = self.COLORS["comparison"] if idx == i or idx == j else self.COLORS["default"]
            pygame.draw.rect(screen, color, (idx * 20, 600 - value, 18, value))
        pygame.display.flip()

    def _draw_bars(self, screen, data, color):
        for idx, value in enumerate(data):
            pygame.draw.rect(screen, color, (idx * 20, 600 - value, 18, value))

import random
import queue
from tkinter import Canvas


class Maze(object):
    class _Node:
        wall_pairs = {'N': 'S',
                      'S': 'N',
                      'E': 'W',
                      'W': 'E'}

        def __init__(self, x, y):
            self.x, self.y = x, y
            self.walls = {'N': 0, 'S': 0, 'E': 0, 'W': 0}

        def getLocation(self):
            return {self.x, self.y}

        def draw(self, canvas: Canvas, block_size: int):
            top_left = self.x * block_size, self.y * block_size
            top_right = self.x * block_size + block_size, self.y * block_size
            btm_left = self.x * block_size, self.y * block_size + block_size
            btm_right = self.x * block_size + block_size, self.y * block_size + block_size

            self.walls['N'] = canvas.create_line(*top_left, *top_right)
            self.walls['S'] = canvas.create_line(*btm_left, *btm_right)
            self.walls['E'] = canvas.create_line(*top_right, *btm_right)
            self.walls['W'] = canvas.create_line(*top_left, *btm_left)

        def destroy_wall(self, other, wall, canvas: Canvas):
            canvas.delete(self.walls[wall])
            self.walls[wall] = -1
            canvas.delete(other.walls[self.wall_pairs[wall]])
            other.walls[self.wall_pairs[wall]] = -1

    def __init__(self, length, width, method=0):
        self.GRID_LENGTH, self.GRID_WIDTH = length, width
        self.grid = [[self._Node(col, row) for col in range(self.GRID_WIDTH)] for row in range(self.GRID_LENGTH)]

        self.START = random.randint(1, self.GRID_LENGTH - 1)
        self.GOAL = random.randint(1, self.GRID_LENGTH - 1)

        self.__generateMaze(method)

    def __generateMaze(self, method):
        self.__populateInner()

    def __populateInner(self):
        # growing tree algorithm
        return 0

    def draw(self, canvas: Canvas, block_size):
        for row in self.grid:
            for node in row:
                node.draw(canvas, block_size)

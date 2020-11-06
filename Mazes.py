import random
from tkinter import Canvas

class Maze(object):

    class _Node:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.n, self.e, self.s, self.w = True, True, True, True

        def getLocation(self):
            return {self.x, self.y}

        def draw(self, canvas: Canvas, block_size: int):
            top_left = self.x * block_size, self.y * block_size
            top_right = self.x * block_size + block_size, self.y * block_size
            btm_left = self.x * block_size, self.y * block_size + block_size
            btm_right = self.x * block_size + block_size, self.y * block_size + block_size
            canvas.create_line(*top_left, *top_right)
            canvas.create_line(*top_left, *btm_left)
            canvas.create_line(*top_right, *btm_right)
            canvas.create_line(*btm_left, *btm_right)

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


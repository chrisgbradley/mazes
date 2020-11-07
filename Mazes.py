import random
from math import atan2
from math import pi
from tkinter import Canvas


class Maze(object):
    class _Node:
        wall_pairs = {'N': 'S',
                      'S': 'N',
                      'E': 'W',
                      'W': 'E'}

        def __init__(self, x, y):
            self.x, self.y = x, y
            self.walls = {}
            self.color = None
            # todo: add a visited boolean

        def getLocation(self):
            return self.x, self.y

        def draw(self, canvas: Canvas, block_size: int):
            top_left = self.x * block_size, self.y * block_size
            top_right = self.x * block_size + block_size, self.y * block_size
            btm_left = self.x * block_size, self.y * block_size + block_size
            btm_right = self.x * block_size + block_size, self.y * block_size + block_size

            self.walls['N'] = canvas.create_line(*top_left, *top_right)
            self.walls['S'] = canvas.create_line(*btm_left, *btm_right)
            self.walls['E'] = canvas.create_line(*top_right, *btm_right)
            self.walls['W'] = canvas.create_line(*top_left, *btm_left)

        def destroy_wall(self, other, canvas: Canvas):
            wall = self.__get_cardinal(self, other)
            canvas.delete(self.walls[wall])
            self.walls[wall] = -1
            canvas.delete(other.walls[self.wall_pairs[wall]])
            other.walls[self.wall_pairs[wall]] = -1

        def shade_me(self, canvas: Canvas, block_size: int):
            top_left = self.x * block_size, self.y * block_size
            btm_right = self.x * block_size + block_size, self.y * block_size + block_size
            self.color = canvas.create_rectangle(*top_left, *btm_right, fill='gray60', outline="")

        def __get_cardinal(self, node_a, node_b):
            x0, y0 = node_a.getLocation()
            x1, y1 = node_b.getLocation()

            dx = x1 - x0
            dy = y1 - y0

            degrees = atan2(dx, dy) / pi * 180

            if degrees < 0:
                degrees_final = 360 + degrees
            else:
                degrees_final = degrees

            cardinal = ["N", "E", "S", "W", "N"]

            cardinal_lookup = round(degrees_final / 90)

            return cardinal[cardinal_lookup]

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

    def __init__(self, length, width, canvas: Canvas, block_size: int, method=0):
        self.canvas = canvas
        self.block_size = block_size
        self.GRID_LENGTH, self.GRID_WIDTH = length, width
        self.grid = [[self._Node(col, row) for col in range(self.GRID_WIDTH)] for row in range(self.GRID_LENGTH)]

        self.START = random.randint(1, self.GRID_LENGTH - 1)
        self.GOAL = random.randint(1, self.GRID_LENGTH - 1)

        self.__draw()

    def generateMaze(self):
        self.__populate()

    def __populate(self):
        open_list = []
        closed_list = [] # todo: sub closed list for visited booleans

        x = random.randint(1, self.GRID_WIDTH - 1)
        y = random.randint(1, self.GRID_LENGTH - 1)
        random_node = self.grid[y][x]

        open_list.append(random_node)
        neighbors = []
        while open_list:
            if not neighbors:
                active = self.__heuristic_select(open_list)
            active.shade_me(self.canvas, self.block_size)
            neighbors = self.__get_neighbors(active, closed_list, open_list)
            if not neighbors:
                continue
            else:
                future = self.__heuristic_select(neighbors)
                [open_list.append(neighbor) for neighbor in neighbors]
                active.destroy_wall(future, self.canvas)
                closed_list.append(active)
                active = future

    def __get_neighbors(self, node, closed, openl):
        n, s, e, w = 0, 0, 0, 0

        neighbors = []

        if node.y >= 1:
            n = self.grid[node.y - 1][node.x]
        if node.y < self.GRID_LENGTH - 1:
            s = self.grid[node.y + 1][node.x]
        if node.x >= 1:
            e = self.grid[node.y][node.x - 1]
        if node.x < self.GRID_WIDTH - 1:
            w = self.grid[node.y][node.x + 1]

        for neighbor in [n, s, e, w]:
            if not isinstance(neighbor, int):
                if neighbor not in closed and node not in openl:
                    # todo: if not neighbor.visited
                    neighbors.append(neighbor)
        return neighbors

    def __heuristic_select(self, alist):
        return alist.pop()

    def __draw(self):
        for row in self.grid:
            for node in row:
                node.draw(self.canvas, self.block_size)

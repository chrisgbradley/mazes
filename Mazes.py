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
            self.visited = False
            self.prev = None

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
            print(wall)
            canvas.delete(self.walls[wall])
            self.walls[wall] = -1
            canvas.delete(other.walls[self.wall_pairs[wall]])
            other.walls[self.wall_pairs[wall]] = -1
            print(self.walls)
            print(other.walls)
            canvas.update()

        def shade_me(self, canvas: Canvas, block_size: int, color: str):
            top_left = self.x * block_size + 5, self.y * block_size + 5
            btm_right = self.x * block_size + block_size - 5, self.y * block_size + block_size - 5
            self.color = canvas.create_rectangle(*top_left, *btm_right, fill=color, outline="")
            canvas.update()

        def unshade_me(self, canvas: Canvas):
            canvas.delete(self.color)
            canvas.update()

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

            cardinal = ["S", "SE", "E", "NE", "N", "NW", "W", "SW", "S"]

            cardinal_lookup = round(degrees_final / 45)

            return cardinal[cardinal_lookup]

        def set_prev(self, prev):
            self.prev = prev

        def get_prev(self):
            return self.prev

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

        # get random cell
        x = random.randint(1, self.GRID_WIDTH - 1)
        y = random.randint(1, self.GRID_LENGTH - 1)
        random_node = self.grid[y][x]

        # add random node to open list
        open_list.append(random_node)
        # init neighbors
        neighbors = []
        active = None
        count = 0

        # while open list has cells
        while open_list:
            if active is None:
                active = open_list.pop()

            print("\n\nevaluating: ", active.getLocation())
            active.visited = True
            neighbors = self.__get_neighbors(active)
            if active.color is not None:
                active.unshade_me(self.canvas)
            active.shade_me(self.canvas, self.block_size, 'red')
            self.canvas.after(25)
            # if neighbors is empty
            if not neighbors:
                # walk backwards
                print("walking")
                while not neighbors:
                    print("current: ", active.getLocation())
                    active = active.get_prev()
                    print("previous, now current", active.getLocation())
                    neighbors = self.__get_neighbors(active)
            else:
                for neighbor in neighbors:
                    neighbor.shade_me(self.canvas, self.block_size, 'grey70')
                future = self.__heuristic_select(neighbors)
                for neighbor in neighbors:
                    if neighbor is not active.get_prev() and neighbor not in open_list:
                        open_list.append(neighbor)
                print("destroying wall between: ", active.getLocation(), future.getLocation())
                active.destroy_wall(future, self.canvas)
                future.set_prev(active)

                active = future

    def __get_neighbors(self, node):
        n, s, e, w = 0, 0, 0, 0

        neighbors = []

        x, y = node.getLocation()

        if y >= 1:
            n = self.grid[y - 1][x]
        if y < self.GRID_LENGTH - 1:
            s = self.grid[y + 1][x]
        if x >= 1:
            e = self.grid[y][x - 1]
        if x < self.GRID_WIDTH - 1:
            w = self.grid[y][x + 1]

        for neighbor in [n, s, e, w]:
            if isinstance(neighbor, self._Node):
                if not neighbor.visited:
                    neighbors.append(neighbor)
        print("Neighbors: ", " ".join(str(x.getLocation()) for x in neighbors))
        return neighbors

    def __heuristic_select(self, alist):
        if random.randrange(0, 99) < 100:
            element = alist[random.randint(0, len(alist)-1)]
            alist.remove(element)
        else:
            element = alist.pop()
        return element

    def __draw(self):
        for row in self.grid:
            for node in row:
                node.draw(self.canvas, self.block_size)

    def detectWalls(self):
        for row in self.grid:
            for n in row:
                print(n.walls)

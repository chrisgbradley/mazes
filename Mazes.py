import random


class Maze(object):

    class _Node:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def getLocation(self):
            return {self.x, self.y}

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


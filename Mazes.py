import random


class Maze(object):
    def __init__(self, length, width, method=0):
        self.GRID_LENGTH, self.GRID_WIDTH = length, width
        self.grid = [[0 for col in range(self.GRID_WIDTH)] for row in range(self.GRID_LENGTH)]
        self.START = random.randint(1, self.GRID_LENGTH - 1)
        self.GOAL = random.randint(1, self.GRID_LENGTH - 1)

        self.__generateMaze(method)

    def print(self):
        print('\n'.join('   '.join(str(x) for x in row) for row in self.grid))

    def __generateMaze(self, method):
        self.__buildWall()
        self.__populateInner()

    def __buildWall(self):
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_LENGTH):
                if x == 0 or y == 0 or x == self.GRID_WIDTH - 1 or y == self.GRID_LENGTH - 1:
                    self.grid[y][x] = 1
        self.grid[self.START][0] = 0
        self.grid[self.GOAL][self.GRID_WIDTH - 1] = 0

    def __populateInner(self):
        # some algorithm to populate

        return 0
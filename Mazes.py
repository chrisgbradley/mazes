import random
from math import atan2
from math import pi
from tkinter import Canvas
from pathlib import Path
import re


class Maze(object):
    """  """
    class _Node:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.walls = {}
            self.color = None
            self.visited = False
            self.prev = None
            self._DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]

        def getLocation(self):
            return self.x, self.y

        def draw(self, canvas: Canvas, block_size: int):
            top_left = self.x * block_size, self.y * block_size
            top_right = self.x * block_size + block_size, self.y * block_size
            btm_left = self.x * block_size, self.y * block_size + block_size
            btm_right = self.x * block_size + block_size, self.y * block_size + block_size

            if 'N' not in self.walls.keys():
                self.walls['N'] = canvas.create_line(*top_left, *top_right)
            elif 'N' in self.walls.keys():
                if self.walls['N'] != -1:
                    self.walls['N'] = canvas.create_line(*top_left, *top_right)

            if 'S' not in self.walls.keys():
                self.walls['S'] = canvas.create_line(*btm_left, *btm_right)
            elif 'S' in self.walls.keys():
                if self.walls['S'] != -1:
                    self.walls['S'] = canvas.create_line(*btm_left, *btm_right)

            if 'E' not in self.walls.keys():
                self.walls['E'] = canvas.create_line(*top_right, *btm_right)
            elif 'E' in self.walls.keys():
                if self.walls['E'] != -1:
                    self.walls['E'] = canvas.create_line(*top_right, *btm_right)

            if 'W' not in self.walls.keys():
                self.walls['W'] = canvas.create_line(*top_left, *btm_left)
            elif 'W' in self.walls.keys():
                if self.walls['W'] != -1:
                    self.walls['W'] = canvas.create_line(*top_left, *btm_left)

        def destroy_wall(self, other, canvas: Canvas, visualize: bool):
            wall = self.get_cardinal_from_nodes(self, other)
            opposite_wall = self.__get_opposite_DIR(wall)

            # VISUAL CUE
            if visualize:
                canvas.delete(self.walls[wall])
                canvas.delete(other.walls[opposite_wall])
                canvas.update()
            # END VISUAL CUE

            self.walls[wall] = -1
            other.walls[opposite_wall] = -1

        def shade_me(self, canvas: Canvas, block_size: int, color: str):
            self.unshade_me(canvas)
            size = 3
            top_left = self.x * block_size + size, self.y * block_size + size
            btm_right = self.x * block_size + block_size - size, self.y * block_size + block_size - size
            self.color = canvas.create_rectangle(*top_left, *btm_right, fill=color, outline="")
            canvas.update()

        def unshade_me(self, canvas: Canvas):
            canvas.delete(self.color)
            canvas.update()

        def get_cardinal_from_nodes(self, a, b):
            if not isinstance(a, type(self)) or not isinstance(b, type(self)):
                raise ValueError("a and b must be of type _Node."
                                 "\na: " + type(a) +
                                 "\nb: " + type(b))
            x0, y0 = a.getLocation()
            x1, y1 = b.getLocation()

            cardinal_lookup = self.__determine_cardinal_index(x0, x1, y0, y1)

            return self._DIRS[cardinal_lookup]

        def get_cardinal_from_coords(self, x0, x1, y0, y1):
            cardinal_lookup = self.__determine_cardinal_index(x0, x1, y0, y1)
            return self._DIRS[cardinal_lookup]

        def __determine_cardinal_index(self, x0, x1, y0, y1):
            dx = x1 - x0
            dy = y1 - y0

            # unit circle!
            degrees = atan2(dx, dy) / pi * 180
            if degrees < 0:
                degrees_final = 360 + degrees
            else:
                degrees_final = degrees

            cardinal_index = round(degrees_final / 45)

            if cardinal_index > len(self._DIRS):
                raise IndexError("cardinal_index is not within the index range of _Node._DIRS.\n"
                                 "Something is probably wrong with the values being passed to "
                                 "cardinal determination function.")

            return cardinal_index

        def __get_opposite_DIR(self, DIR):
            index = self._DIRS.index(DIR) + 4
            if index >= len(self._DIRS):
                index = index - len(self._DIRS)
            return self._DIRS[index]

        def set_prev(self, prev):
            self.prev = prev

        def get_prev(self):
            return self.prev

        def put_wall_at_cardinal(self):

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

    def __init__(self,
                 file_name="", cell_wall_coords=None,  # use a file name to construct
                 length=0, width=0, block_size=0,  # use cell dimensions to construct maze
                 iterate_delay=0, method=0, canvas=None, visualize_gen=False
                 ):
        self._file_name = file_name

        self._cell_wall_coords = cell_wall_coords

        self.block_size = block_size
        self.GRID_LENGTH, self.GRID_WIDTH = length, width
        self.grid = [[self._Node(col, row) for col in range(self.GRID_WIDTH)] for row in range(self.GRID_LENGTH)]

        self.START = random.randint(1, self.GRID_LENGTH - 1)
        self.GOAL = random.randint(1, self.GRID_LENGTH - 1)

        # OPTIONS
        self._iterate_delay = iterate_delay
        self._method = method
        self.canvas = canvas
        self.visualize_gen = visualize_gen

        if self._file_name:
            self.load_from_svg(self._file_name)
        elif not all([length, width, block_size]):
            raise ValueError("Must have either a file name or non-zero tuple<int, int, int>")
        elif self._cell_wall_coords is not None:
            self.__construct_maze_from_coords()
        if self.visualize_gen:
            self.__construct_maze_with_vis()

    def __carve_maze(self):
        open_list = []

        # get random cell
        x = random.randint(1, self.GRID_WIDTH - 1)
        y = random.randint(1, self.GRID_LENGTH - 1)
        random_node = self.grid[y][x]

        # add random node to open list
        open_list.append(random_node)
        active = None

        # while open list has cells
        while open_list:
            # should only get called on first loop
            if active is None:
                active = open_list.pop()

            # mark the node
            active.visited = True
            # get node neighbors
            neighbors = self.__get_neighbors(active)

            # VISUAL CUE
            if self.visualize_gen:
                if active.color is not None:
                    active.unshade_me(self.canvas)
                active.shade_me(self.canvas, self.block_size, 'red')
                self.canvas.after(self._iterate_delay)
            # END VISUAL CUE

            # if neighbors is empty
            if not neighbors:
                # walk backwards
                while not neighbors:
                    active = active.get_prev()
                    if active is None:
                        return
                    neighbors = self.__get_neighbors(active)
            else:
                # VISUAL CUE
                if self.visualize_gen:
                    for neighbor in neighbors:
                        neighbor.shade_me(self.canvas, self.block_size, 'grey70')
                # END VISUAL CUE

                # pick next node to visit
                future = self.__heuristic_select(neighbors)
                # add other neighbors to open list, if any
                for neighbor in neighbors:
                    if neighbor is not active.get_prev() and neighbor not in open_list:
                        open_list.append(neighbor)

                active.destroy_wall(future, self.canvas, self.visualize_gen)

                # allow back tracing
                future.set_prev(active)
                # proceed to next node
                active = future

        # VISUAL CUE
        if self.canvas is not None and not self.visualize_gen:
            self.__construct_maze_with_vis()
        # END VISUAL CUE

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
        return neighbors

    def __heuristic_select(self, alist):
        if random.randrange(0, 99) < 100:
            element = alist[random.randint(0, len(alist)-1)]
            alist.remove(element)
        else:
            element = alist.pop()
        return element

    def __construct_maze_from_coords(self):
        coords_index = 0
        wall = None
        for row in self.grid:
            for cell in row:
                while True:  # while in current cell's bounds
                    wall = self._cell_wall_coords[coords_index]  # get the next wall (carries to next cell)
                    highest_val = max(wall)  # largest value from the coordinate set
                    cell_x, cell_y = cell.getLocation()  # get cell's coords
                    if highest_val > cell_x or highest_val > cell_y:  # check if in cell bounds
                        break
                    cardinal = cell.get_cardinal_from_coords(*wall)
                    if self.canvas is not None:
                        cell.put_wall_at_cardinal(cardinal, self.canvas, self.block_size)
                    coords_index += 1  # update coords index
                cell.update_any_empty_walls()

    def __construct_maze_with_vis(self):
        for row in self.grid:
            for node in row:
                node.draw(self.canvas, self.block_size)

    def generate_maze(self):
        self.__carve_maze()

    def unshade_everything(self):
        number_of_diagonals = self.GRID_WIDTH + self.GRID_LENGTH - 1

        for diagonal_row in range(number_of_diagonals):
            if diagonal_row <= self.GRID_WIDTH - 1:
                for y, x in zip(range(self.GRID_LENGTH), range(diagonal_row - 1, -1, -1)):
                    node = self.grid[y][x]
                    node.unshade_me(self.canvas)
            elif diagonal_row >= self.GRID_WIDTH:
                x = self.GRID_WIDTH - 1
                for y in range(diagonal_row - self.GRID_WIDTH, self.GRID_LENGTH):
                    if x == self.GRID_WIDTH - self.GRID_LENGTH - 1:
                        x = self.GRID_WIDTH - 1
                    node = self.grid[y][x]
                    x -= 1
                    node.unshade_me(self.canvas)
            else:
                for y, x in zip(range(0, self.GRID_LENGTH), range(self.GRID_WIDTH - 1, self.GRID_LENGTH - self.GRID_WIDTH, -1)):
                    node = self.grid[y][x]
                    node.unshade_me(self.canvas)

        self.grid[self.GRID_LENGTH - 1][self.GRID_WIDTH - 1].unshade_me(self.canvas)

    def save_to_svg(self, file_name: str, add_styling=False):
        # If file exists append a number
        if Path(file_name).exists():
            index = 1
            new_file_name = file_name + "_" + str(index)
            while Path(file_name).exists():
                if Path(new_file_name).exists():
                    index += 1
                    new_file_name = file_name + "_" + str(index)
            file_name = new_file_name

        file_name += ".svg"

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # make file path and open file
        file_path = Path(file_name)
        file = open(file_path, "w")

        styles = ""
        if add_styling:
            styles = "border:25px solid black;margin:50px auto;padding:10px;"

        # BEGIN SVG EDIT
        file.write("<svg width=\"" + str(width) + "px\" height=\"" + str(height) + "px\" "
                   "viewBox=\"0 0 " + str(width) + " " + str(height) + "\" "
                   "preserveAspectRatio=\"xMinYMin meet\" "
                   "style=\""
                   "display:flex;"
                   "justify-content:center;"
                   "align-items:center;"
                   "" + styles + "\" "
                   "xmlns=\"http://www.w3.org/2000/svg\">")  # end opening tag

        for row in self.grid:
            for node in row:        # for each node in the grid
                for direction in node.walls:  # grab that node's walls
                    wall = node.walls[direction]
                    if wall != -1:      # ignore the "wall" if it was carved out
                        x1, y1, x2, y2 = self.canvas.coords(wall)
                        file.write("<line x1=\"" + str(x1) + "\"  x2=\"" + str(x2) + "\" ")
                        file.write("y1=\"" + str(y1) + "\"  y2=\"" + str(y2) + "\" ")
                        file.write("stroke=\"#000000\" stroke-width=\"1\"/>")

        file.write("</svg>")
        # END SVG EDIT

        # remember to close file when done
        file.close()

        return self

    def load_from_svg(self, file_name: str):
        """
        :param file_name:
        :type file_name:
        :return:
        :rtype:
        """
        if not Path(file_name).exists():
            FileNotFoundError(file_name + " does not exist.")
            return -1

        file = open(Path(file_name), "r")
        coordinate_string = 'x1="[0-9]+.[0-9]+"  x2="[0-9]+.[0-9]+" y1="[0-9]+.[0-9]+"  y2="[0-9]+.[0-9]+"'
        # whole string > first char > first char > minus first char > first char
        regex = r'(?:(' + coordinate_string + '))'

        coords = []
        for coord_set in self.__each_chunk(file, regex=regex):
            # if last element contains the closing svg tag, it wont have coords in it
            # you've already got all the coords
            if "</svg>" in coord_set:
                break
            # process coordinate set
            coords.append([int(float(x)) for x in re.findall(r'[0-9]+.[0-9]+', coord_set)])

        any_coordinate_set = coords[random.randint(0, len(coords) - 1)]

        dx = abs(any_coordinate_set[0] - any_coordinate_set[1])
        dy = abs(any_coordinate_set[2] - any_coordinate_set[3])

        block_size = max(dx, dy)

        width, length = 0, 0

        for wall in coords:
            width = max(width, wall[0], wall[1])
            length = max(length, wall[2], wall[3])

        maze = Maze(cell_wall_coords=coords, length=length, width=width, block_size=block_size)

        file.close()

    def __each_chunk(self, stream, regex):
        """

        :param stream:
        :type stream:
        :param separator:
        :type separator:
        :return:
        :rtype:
        :see: https://stackoverflow.com/questions/47927039/reading-a-file-until-a-specific-character-in-python
        """
        CHUNK_SIZE = 4096
        buffer = ''
        while True:  # break on EOF
            chunk = stream.read(CHUNK_SIZE)
            if not chunk:  # EOF
                yield buffer
                break  # kill loop
            buffer += chunk
            # break apart buffer into parts
            while True:  # until no separator is found
                try:
                    trash, part, buffer = re.split(regex, buffer, maxsplit=1)
                except ValueError:
                    break
                else:
                    yield part

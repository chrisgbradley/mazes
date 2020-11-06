from Mazes import Maze
from tkinter import *


def main():
    height = 50
    width = 75
    unit_size = 15

    root = Tk()
    root.title("Maze")
    canvas = Canvas(root, width=1125, height=750, background='gray90')
    canvas.pack()

    canvas.create_line(1, 1, 1, width * unit_size)
    canvas.create_line(width * unit_size, 1, width * unit_size, height * unit_size)
    canvas.create_line(1, 1, 1, height)
    canvas.create_line(1, height * unit_size, width * unit_size, height * unit_size)

    maze = Maze(height, width)

    root.mainloop()


main()
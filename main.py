from Mazes import Maze
import tkinter as tk


def main():
    height = 50
    width = 75
    unit_size = 15

    root = tk.Tk()
    root.title("Maze")
    root.configure(background="black")
    canvas = tk.Canvas(root, width=1125, height=750, background='gray90', borderwidth=0, highlightthickness=False)
    canvas.pack(padx=10, pady=10)

    maze = Maze(height, width)

    maze.draw(canvas, block_size=unit_size)

    root.mainloop()


main()
from Mazes import Maze
import tkinter as tk
from tkinter import ttk


def main():
    height = 25
    width = 50
    unit_size = 25
    iterate_delay = 1

    root = tk.Tk()
    root.title("Maze")
    root.configure(background="black")
    canvas = tk.Canvas(master=root, width=1250, height=625, background='gray90', borderwidth=0, highlightthickness=False)
    canvas.pack(padx=10, pady=10)

    maze = Maze(height, width, unit_size, iterate_delay=iterate_delay, canvas=canvas, visualize_gen=False)

    buttons = tk.Frame(root, padx="5", pady="10", bg="black")
    buttons.pack()

    button = tk.Button(buttons, text="Generate Maze", command=maze.generate_maze, justify=tk.CENTER, padx=50, pady=10)
    button.pack(side=tk.LEFT)

    button = tk.Button(buttons, text="Save Maze", command=lambda: maze.save_to_svg("maze", True), justify=tk.CENTER, padx=50, pady=10)
    button.pack(side=tk.RIGHT)

    button = tk.Button(buttons, text="Unshade Maze", command=maze.unshade_everything, justify=tk.CENTER, padx=50, pady=10)
    button.pack(side=tk.RIGHT)

    root.mainloop()


main()
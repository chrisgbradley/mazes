from Mazes import Maze
import tkinter as tk


def main():
    height = 25
    width = 50
    unit_size = 50
    iterate_delay = 10

    root = tk.Tk()
    root.title("Maze")
    root.configure(background="black")
    canvas = tk.Canvas(master=root, width=2500, height=1250, background='gray90', borderwidth=0, highlightthickness=False)
    canvas.pack(padx=10, pady=10)

    maze = Maze(height, width, unit_size, iterate_delay=iterate_delay, canvas=canvas, visualize_gen=False)

    button = tk.Button(master=root, text="Generate Maze", command=maze.generateMaze, justify=tk.CENTER, padx=5, pady=10)
    button.pack()

    button = tk.Button(master=root, text="Unshade Maze", command=maze.unshade_everything, justify=tk.CENTER, padx=5, pady=10)
    button.pack()

    root.mainloop()


main()
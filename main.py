from Mazes import Maze
import tkinter as tk


def main():
    height = 50
    width = 75
    unit_size = 15

    root = tk.Tk()
    root.title("Maze")
    root.configure(background="black")
    canvas = tk.Canvas(master=root, width=1125, height=750, background='gray90', borderwidth=0, highlightthickness=False)
    canvas.pack(padx=10, pady=10)

    maze = Maze(height, width, canvas, unit_size)

    button = tk.Button(master=root, text="Generate Maze", command=maze.generateMaze, justify=tk.CENTER, padx=5, pady=10)
    button.pack()

    root.mainloop()


main()
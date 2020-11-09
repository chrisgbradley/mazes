# Mazes.py
At the moment, a simple maze builder. It may stay that way. I may turn it into an actual maze game. Maybe something in between.
It uses Tkinter's Canvas object to draw on and can be used to visualize a growing tree algorithm or just simply produce the maze.


## Obstacles

### First time using GUI in Python
This wasn't a terrible struggle by any means. Tkinter is very well documented and pretty easy to follow. I definitely see 
a lot of potential implementing a GUI in Python vs Java. Been there and got kicked by that horse.

### Getting Canvas to update during the visualization process
Unfortunately, this one hurt. Every search I did produced results surrounding `.after`. Only after many hours did I discover the
ever so conveniently and aptly name `canvas.update()`. Never again will I not look for the simplest function first. Wow.

### Growing Tree Algorithm
It's hard to tell how much I struggled on this. Part of me says not at all and part of me says a decent bit. This came after the `.update()`
struggle and I had already implemented a decent bit of the algorithm. What ended up happening was I was debugging the algorithm when I initially
thought `.after()` was working. This could have been easily remedied if I just tested the canvas a bit before diving into the
algorithm.


## Potential Goals
Some things that I would like to play around with and implement, but life is busy right now and I may or may not get
around to it.

#### File writing
* ~~Saving the maze to SVG~~ 🗸
* Loading a maze from SVG

#### OpenCV
* Using OCR to load a maze from any type of picture

#### Algorithms
* Maze pathfinder with multiple algorithms and comparisons
* Growing Binary Tree algorithm
* Heuristic options for the next node selection

#### User interaction
* Turn the maze into a game and actually play the maze live'

#### UI Feedback
* Add a progress bar for progress until maze is generated

#### GIT
* Use branches and merges for future features

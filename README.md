# Project 64x32

**64x32** is a set of visualizations to be displayed on a 64x32 grid of individually addressable LEDs (such as WS2812B, NeoPixel, etc).  
This project also includes a python script called PC Graphics Interface that demos these visualizations on a computer.

### Requirements
- Python 3.x 
- Pygame (if you want to display the visualizations on a PC instead of an LED grid)

---

## Current Visualization Modes  

### Maze Solve : Wide Search 
- Solves a maze with a breadth-first algorthm. Checks every possible path simultaneously, one step at a time. This algorithm will explore by generating paths every time it encounters a fork. Because it works its paths concurrently it slows down as more path options are created, but speeds up as paths encounter dead ends. Colors of explored portions of the maze represent the distance from the origin. The more red-shifted the color the more steps a point is from the start of the maze.
- Options
  - **whole_layer_step**: False will animate each path taking 1 step sequentially. True will animate all paths taking a step concurrently.
  - **show_maze_build**: True will animate the creation of the maze. False will start animation with maze already constructed.  
![image](https://github.com/user-attachments/assets/ff47a288-1467-4449-8376-7c003bf57a61)
### Maze Solve : Deep Search
- Solves a maze with a depth-first algorthm. Will try to follow one path until it reaches a dead end. Will backtrack to the last point in the path with an unexplored branch and will start again from there.
- Options
  - **show_seek**: True will animate each step while advancing down an unexplored path. False will animate only the path when a dead end is reached.
  - **show_retreat**: True will animate each step while backtracking from a dead-end to a previously visited branch. False is more accurate to the speed of the algorithm and backtracks instantly.
  - **show_solve**: False will skip all solving animation and only show the correct path.
  - **show_visited**: True will shade any visited location gray if it turned out to lead to a dead end. Good for visualizing wasted effort when trying to solve maze.  
![image](https://github.com/user-attachments/assets/038be4dd-7459-4e5e-980e-95691e9d1736)
### Maze Solve : Verses
- Shows a depth-first and breadth-first algorithm competing on identical mazes. Options are pre-selected to make competition fair by having each frame of animation be roughly equivalent computations for each algorithm.  
![image](https://github.com/user-attachments/assets/c98e3592-82ff-4307-ac07-2aeb1bbaec8a)
### Starfield
- Animates a point of view of traveling through stars.  
![image](https://github.com/user-attachments/assets/d77605d2-513f-4953-87d1-cc7c9449f78e)
### Rainfall
- Animates rainfall. Water level will eventually start to rise and droplets will cause splashes. Animation will reset when screen fills with water.  
![image](https://github.com/user-attachments/assets/ce66b498-faae-4fc7-aead-23d95b34f09e)

## Instructions for Display on Computer
Switch Mode: Space  
Quit: Escape

---

## Acknowledgements
#### Maze Generation Algorthm [CaptainLuma](https://github.com/CaptainLuma/New-Maze-Generating-Algorithm)  
He has a simple method to randomly generate a maze that is garenteed to have 1 and only 1 solution during its entire randomizing process.
#### Color Spectrum Code [Grismar](https://stackoverflow.com/questions/66630051/how-to-create-a-1000-color-rgb-rainbow-gradient-in-python)  
Grismar has a nifty solution to make a color gradient in 24 bit RGB transitions smoothly through the visual light spectrum.

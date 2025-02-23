# Project 64x32

**64x32** is a set of visualizations to be displayed on a 64x32 grid of individually addressable LEDs (such as WS2812B, NeoPixel, etc).  
This project also includes a python script called PC Graphics Interface that demos these visualizations on a computer.

### Requirements
- Python 3.x 
- Pygame (if you want to display the visualizations on a PC instead of an LED grid)

---

## Current Visualization Modes  

- Maze Solve (Wide Search). Solves a maze by checking every possible path simultaneously, one step at a time. This algorithm will explores by generating paths every time it encounters a fork. Because it works its paths concurently it slows down as more path options are created, but speeds up as paths encounter dead ends.

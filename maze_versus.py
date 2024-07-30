# Spectrum code by Grismar credit: https://stackoverflow.com/questions/66630051/how-to-create-a-1000-color-rgb-rainbow-gradient-in-python
# Maze randomization algorithm by CaptainLuma credit: https://github.com/CaptainLuma/New-Maze-Generating-Algorithm

from maze import Maze
from Pixel_Grid import Pixel_Grid
from maze_deep import Deep_Maze_Solver
from maze_wide import Wide_Maze_Solver


class Versus_Solver:
    def __init__(self, grid):
        self.grid = grid
        self.x_size = grid.cols // 2
        self.y_size = grid.rows
        self.background = [20,20,20]
        self.deep_grid = Pixel_Grid(self.x_size, self.y_size, self.background)
        self.deep_maze = Maze(self.deep_grid, self.x_size//2, self.y_size//2 )
        self.deep_solver = Deep_Maze_Solver(self.deep_grid, show_solve=True, show_seek=True, show_retreat=True)
        self.wide_grid = Pixel_Grid(self.x_size, self.y_size, self.background)
        self.wide_maze = Maze(self.wide_grid, self.x_size//2, self.y_size//2)
        self.wide_solver = Wide_Maze_Solver(self.wide_grid, show_solve=True )
        max_shuffles = self.y_size * self.x_size * 10
        for s in range(max_shuffles):
            self.deep_maze.shuffle()
        self.deep_maze.fixed_anchor()
        for node_counter in range (len(self.deep_maze.nodes)):
            self.wide_maze.nodes[node_counter] = self.deep_maze.nodes[node_counter]
        self.wide_maze.anchor = self.deep_maze.anchor
        self.deep_solver.set_maze(self.deep_maze)
        self.wide_solver.set_maze(self.wide_maze)




    def step(self):
        """advances one graphical step. Returns false when it is time to create a new Versus_Solver object"""
        if self.deep_solver.step() and self.wide_solver.step():
            self.draw()
            return True
        self.draw()
        return False

    def draw(self):
        for row in range(self.deep_grid.rows):
            for col in range(self.deep_grid.cols):
                self.grid.set_pixel(col, row,
                                    self.deep_grid.get_pixel(col, row))
        for row in range(self.wide_grid.rows):
            for col in range(self.wide_grid.cols):
                self.grid.set_pixel(col + self.deep_grid.cols, row,
                                    self.wide_grid.get_pixel(col, row))




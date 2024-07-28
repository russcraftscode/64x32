# Maze randomization algorithm by CaptainLuma credit: https://github.com/CaptainLuma/New-Maze-Generating-Algorithm
# Spectrum code by Grismar credit: https://stackoverflow.com/questions/66630051/how-to-create-a-1000-color-rgb-rainbow-gradient-in-python

import random
from maze import Maze

class Deep_Maze_Solver:
    def __init__(self, grid, show_seek=False, show_retreat=False, show_solve=False, show_maze_build=False):
        self.grid = grid
        self.visited_spaces = []
        self.current_path = []
        self.x_size = grid.cols // 2
        self.y_size = grid.rows // 2
        self.maze = Maze(self.grid, self.x_size, self.y_size)
        self.current_path.append(self.maze.get_node(0, 0))
        self.maze_built = False
        self.shuffle_count = 0
        self.max_shuffles = self.y_size * self.x_size * 10
        self.SHOW_SEEK = show_seek
        self.SHOW_RETREAT = show_retreat
        self.SHOW_SOLVE = show_solve
        self.SHOW_MAZE = show_maze_build
        self.spectrum = []
        for r, g, b in zip(
                (list(reversed(range(256))) + [0] * 256),
                (list(range(256)) + list(reversed(range(256)))),
                ([0] * 256 + list(range(256)))):
            self.spectrum.append([r, g, b])
        self.spectrum.reverse()

    def get_options(self, node):
        """ gets all spaces that are next to the node that are linked to or from the node"""
        options = []
        # add the node that this node points to as an option to move to
        if node.next != None: options.append(node.next)
        # add the nodes that neighbor this node and point to this node as options to move to
        if node.north != None:
            if node.north.next == node: options.append(node.north)
        if node.east != None:
            if node.east.next == node: options.append(node.east)
        if node.south != None:
            if node.south.next == node: options.append(node.south)
        if node.west != None:
            if node.west.next == node: options.append(node.west)
        random.shuffle(options)
        return options

    def move(self):
        """either seeks towards a possible solution or retreats if at a dead end.
        Returns true if seeking and false if retreating"""
        # determine if we are searching or retreating
        if True:
            options = self.get_options(self.current_path[-1])
            viable_options = []
            for option in options:
                if option not in self.visited_spaces:
                    viable_options.append(option)
            if len(viable_options) > 0:
                self.seek(viable_options)
                return True
            else:
                self.retreat()
                return False

    def at_end_of_path(self):
        """Returns true if at end of path"""
        options = self.get_options(self.current_path[-1])
        viable_options = []
        for option in options:
            if option not in self.visited_spaces:
                viable_options.append(option)
        if len(viable_options) > 0: return False
        return True


    def step(self):
        """advances one graphical step. Returns false when it is time to create a new Deep_Maze_Solver object"""
        if self.maze_built == False:  # step the maze generation
            if self.SHOW_MAZE == False:  # if maze generation is not to be shown
                for s in range(self.max_shuffles):
                    self.maze.shuffle()
                self.maze.fixed_anchor()
                self.maze_built = True
            # if maze generation is to be shown
            elif self.shuffle_count < self.max_shuffles:
                self.maze.shuffle()
                self.shuffle_count += 1
                self.maze.draw()
                if self.shuffle_count > self.max_shuffles:
                    self.maze_built = True
        else:  # step the solving
            # if the steps of solving the maze is to be shown
            if self.SHOW_SOLVE:
                # if the individual steps towards a path end are to be shown
                if self.SHOW_SEEK:
                    # if not animating retreat then first pull back until a new path is found
                    if not self.SHOW_RETREAT:
                        while self.at_end_of_path():
                            self.move()
                    self.move()
                    self.draw()
                    # if the maze is solved return false to stop the loop in the main class
                    if self.is_solved():
                        return False
                # if the only thing to be shown is the path when it reaches an end
                if not self.SHOW_SEEK:
                    # first retreat until a new path is found
                    while self.at_end_of_path():
                        self.move()
                    # seek until a path has no more options
                    while not self.at_end_of_path():
                        self.move()
                        if self.is_solved():
                            self.draw()
                            return False
                    self.draw()
                    if self.is_solved():
                        return False
            # if the steps of solving the maze are not to be shown
            else:
                while not self.is_solved():
                    self.move()
                self.draw()
                return False # return false to indicate maze is solved
        return True # if the maze has not been solved return true

    def seek(self, viable_options):
        """seeks out one more space that has not been visited"""
        self.visited_spaces.append(viable_options[0])
        self.current_path.append(viable_options[0])

    def retreat(self):
        """backtracks one space"""
        self.current_path.pop()

    def draw(self):
        """updates the display with data based on the maze and pathfinder. Pixel locations are doubled to account for space between nodes"""
        self.maze.draw()
        prev_square = self.current_path[0]
        for n in self.current_path:
            self.grid.set_pixel(n.x_pos * 2, n.y_pos * 2, [10, 200, 10])
            if prev_square != n:  # connect node with it's previous node
                self.grid.set_pixel((n.x_pos + prev_square.x_pos) * 2 // 2, (n.y_pos + prev_square.y_pos) * 2 // 2,
                                    [10, 200, 10])
            prev_square = n

    def is_solved(self):
        """returns true if the maze is solved"""
        if self.maze.anchor in self.current_path:
            return True
        else:
            return False

import copy
import random


class Maze:
    def __init__(self, grid, x_size, y_size):
        self.cols = x_size // 2
        self.rows = y_size // 2
        self.max_shuffles = 5000
        self.current_shuffles = 0
        self.grid = grid
        # create the nodes
        self.nodes = []
        for x in range(self.cols):
            for y in range(self.rows):
                self.nodes.append(Maze_Node(x, y))
        # link the nodes to their surroundings
        for x in range(1, self.cols):  # center nodes
            for y in range(1, self.rows):
                n = self.get_node(x, y)
                n.north = self.get_node(x, y - 1)
                n.east = self.get_node(x + 1, y)
                n.west = self.get_node(x - 1, y)
                n.south = self.get_node(x, y + 1)
        y = 0  # top row
        for x in range(1, self.cols):
            n = self.get_node(x, y)
            n.east = self.get_node(x + 1, y)
            n.west = self.get_node(x - 1, y)
            n.south = self.get_node(x, y + 1)
        y = self.rows - 1  # bottom row
        for x in range(1, self.cols):
            n = self.get_node(x, y)
            n.north = self.get_node(x, y - 1)
            n.east = self.get_node(x + 1, y)
            n.west = self.get_node(x - 1, y)
        x = 0  # left side
        for y in range(1, self.rows):
            n = self.get_node(x, y)
            n.north = self.get_node(x, y - 1)
            n.east = self.get_node(x + 1, y)
            n.south = self.get_node(x, y + 1)
        x = self.cols - 1  # right side
        for y in range(1, self.rows):
            n = self.get_node(x, y)
            n.north = self.get_node(x, y - 1)
            n.west = self.get_node(x - 1, y)
            n.south = self.get_node(x, y + 1)
        # upper left corner
        x = 0
        y = 0
        n = self.get_node(x, y)
        n.east = self.get_node(x + 1, y)
        n.south = self.get_node(x, y + 1)
        # upper right corner
        x = self.cols - 1
        y = 0
        n = self.get_node(x, y)
        n.west = self.get_node(x - 1, y)
        n.south = self.get_node(x, y + 1)
        # lower left corner
        x = 0
        y = self.rows - 1
        n = self.get_node(x, y)
        n.north = self.get_node(x, y - 1)
        n.east = self.get_node(x + 1, y)
        # lower right corner
        x = self.cols - 1
        y = self.rows - 1
        n = self.get_node(x, y)
        n.north = self.get_node(x, y - 1)
        n.west = self.get_node(x - 1, y)
        self.anchor = n

        # add the direction properties to each node by linking it to the next node
        for y in range(self.rows):
            for x in range(self.cols):
                self.get_node(x, y).next = self.get_node(x, y).east
            self.get_node(self.cols - 1, y).next = self.get_node(self.cols - 1, y).south

    def shuffle(self):
        """Uses CaptainLuma's maze generation algorithm to randomize a maze"""
        # credit: https://github.com/CaptainLuma/New-Maze-Generating-Algorithm
        next_to_anchor = self.next_to(self.anchor)
        new_anchor = random.choice(next_to_anchor)
        self.anchor.next = new_anchor
        self.anchor = new_anchor
        self.anchor.next = None
        self.current_shuffles += 1
        if self.current_shuffles >= self.max_shuffles:
            return True
        return False

    def next_to(self, node):
        """returns all the existing nodes that are next to a given node"""
        next_to_node = []
        if node.north != None: next_to_node.append(node.north)
        if node.east != None: next_to_node.append(node.east)
        if node.west != None: next_to_node.append(node.west)
        if node.south != None: next_to_node.append(node.south)
        return next_to_node

    def get_node(self, x, y):
        for n in self.nodes:
            if n.x_pos == x and n.y_pos == y:
                return n
        return None

    def draw(self):
        """updates the display with data based on the maze. Pixel locations are doubled to account for space between nodes"""
        self.grid.wipe()
        for n in self.nodes:
            if n == self.anchor:
                self.grid.set_pixel(n.x_pos * 2, n.y_pos * 2, [200, 10, 10])
            else:
                self.grid.set_pixel(n.x_pos * 2, n.y_pos * 2, [200, 200, 200])
            if n.next != None:
                self.grid.set_pixel((n.x_pos * 2 + n.next.x_pos * 2) // 2, (n.y_pos * 2 + n.next.y_pos * 2) // 2,
                                    [200, 200, 200])


class Maze_Node:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.next = None


class Width_Maze_Solver:
    """ solves a maze by searching wide"""
    def __init__(self, maze, grid):
        self.grid = grid
        self.visited_spaces = []
        self.maze = maze
        self.layers = [[self.maze.nodes[0]]]
        self.current_layer = [self.maze.nodes[0]]
        self.working_layer = []
        self.spectrum = []
        for r, g, b in zip(
                (list(reversed(range(256))) + [0] * 256),
                (list(range(256)) + list(reversed(range(256)))),
                ([0] * 256 + list(range(256)))):
            self.spectrum.append([r, g, b])
        self.spectrum.reverse()

    def step(self):
        """searches another node and returns true if goal is found"""
        # determine if we have a full layer
        full_layer = True
        for n in self.current_layer:
            if n not in self.working_layer:
                full_layer = False

        if full_layer:
            new_layer = []
            for n in self.current_layer:
                new_layer.append(n)
            self.layers.append(new_layer)
            self.current_layer = self.next_layer()
            self.working_layer = []
        else:
            # grab the next node from the current layer to add to the working layer
            self.working_layer.append(self.current_layer[len(self.working_layer)])
        solved = self.maze.anchor in self.working_layer
        return solved

    def next_layer(self):
        """finds the next layer of spaces that can be reached"""
        next_layer = []
        for n in self.layers[-1]:
            if n.next != None:
                if n.next not in self.visited_spaces:
                    next_layer.append(n.next)
            # add the nodes that neighbor this node and point to this node as options to move to
            if n.north != None:
                if n.north not in self.visited_spaces:
                    if n.north.next == n: next_layer.append(n.north)
            if n.east != None:
                if n.east not in self.visited_spaces:
                    if n.east.next == n: next_layer.append(n.east)
            if n.south != None:
                if n.south not in self.visited_spaces:
                    if n.south.next == n: next_layer.append(n.south)
            if n.west != None:
                if n.west not in self.visited_spaces:
                    if n.west.next == n: next_layer.append(n.west)
        #update visited spaces
        for n in next_layer:
            self.visited_spaces.append(n)
        return next_layer

    def draw(self):
        """updates the display with data based on the maze and pathfinder. Pixel locations are doubled to account for space between nodes"""
        self.maze.draw()
        color_counter = 0
        for l_count, layer in enumerate(self.layers):
            if color_counter < len(self.spectrum) - 20: color_counter += 10
            for n in layer:
                self.grid.set_pixel(n.x_pos * 2, n.y_pos * 2,
                                    [self.spectrum[color_counter][0], self.spectrum[color_counter][1],
                                     self.spectrum[color_counter][2]])
                if l_count > 1:
                    # connect node with its previous node
                    prev_node = None
                    if n.north in self.layers[l_count-1]:
                        if n.north.next == n: prev_node = n.north
                        if n.next == n.north: prev_node = n.north
                    if n.east in self.layers[l_count-1]:
                        if n.east.next == n: prev_node = n.east
                        if n.next == n.east: prev_node = n.east
                    if n.west in self.layers[l_count-1]:
                        if n.west.next == n: prev_node = n.west
                        if n.next == n.west: prev_node = n.west
                    if n.south in self.layers[l_count-1]:
                        if n.south.next == n:prev_node = n.south
                        if n.next == n.south:prev_node = n.south
                    if prev_node != None:
                        self.grid.set_pixel((n.x_pos + prev_node.x_pos)*2 // 2, (n.y_pos + prev_node.y_pos)*2 // 2, [self.spectrum[color_counter  ][0], self.spectrum[color_counter ][1],
                                                                                                                     self.spectrum[color_counter ][2]])

        for n in self.working_layer:
            self.grid.set_pixel(n.x_pos * 2, n.y_pos * 2,
                                [self.spectrum[color_counter + 10][0], self.spectrum[color_counter + 10][1],
                                 self.spectrum[color_counter + 10][2]])
            # connect node with its previous node
            prev_node = None
            if n.north in self.layers[-1]:
                if n.north.next == n: prev_node = n.north
                if n.next == n.north: prev_node = n.north
            if n.east in self.layers[-1]:
                if n.east.next == n: prev_node = n.east
                if n.next == n.east: prev_node = n.east
            if n.west in self.layers[-1]:
                if n.west.next == n: prev_node = n.west
                if n.next == n.west: prev_node = n.west
            if n.south in self.layers[-1]:
                if n.south.next == n: prev_node = n.south
                if n.next == n.south:prev_node = n.south
                if n.next == n.south:prev_node = n.south
            if prev_node != None:
                self.grid.set_pixel((n.x_pos + prev_node.x_pos)*2 // 2, (n.y_pos + prev_node.y_pos)*2 // 2, [self.spectrum[color_counter + 10][0], self.spectrum[color_counter + 10][1],
                                                                                                             self.spectrum[color_counter + 10][2]])

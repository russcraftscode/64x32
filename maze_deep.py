import random


class Maze:
    def __init__(self, grid, x_size, y_size):
        self.cols = x_size
        self.rows = y_size
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


    def fixed_anchor(self):
        """this sets the anchor to the bottom right of the maze"""
        while self.anchor !=  self.get_node(self.cols-1, self.rows-1):
            self.shuffle()
            print(f"{self.anchor.x_pos}, {self.anchor.y_pos}")

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


class Deep_Maze_Solver:
    def __init__(self, grid, show_seek=None, show_retreat=None, show_solve=None, show_maze_build=None):
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
        if show_seek is None:
            self.SHOW_SEEK = False
        else:
            self.SHOW_SEEK = show_seek
        if show_retreat is None:
            self.SHOW_RETREAT = False
        else:
            self.SHOW_RETREAT = show_retreat
        if show_solve is None:
            self.SHOW_SOLVE = False
        else:
            self.SHOW_SOLVE = show_solve
        if show_maze_build is None:
            self.SHOW_MAZE = False
        else:
            self.SHOW_MAZE = show_maze_build

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
        """either seeks towards a possible solution or retreats if at a dead end"""
        # determine if we are searching or retreating
        if True:
            options = self.get_options(self.current_path[-1])
            viable_options = []
            for option in options:
                if option not in self.visited_spaces:
                    viable_options.append(option)
            if len(viable_options) > 0:
                self.seek(viable_options)
            else:
                self.retreat()

    def step(self):
        """advances one graphical step. Returns false when it is time to create a new Deep_Maze_Solver object"""
        if self.maze_built == False: # step the maze generation
            if self.SHOW_MAZE == False: # if maze generation is not to be shown
                for s in range(self.max_shuffles):
                    self.maze.shuffle()
                # if the maze solving process is not to be animated, just put the anchor on the bottom right
                if self.SHOW_SOLVE == False:
                    self.maze.fixed_anchor()
                self.maze_built = True
            # if maze generation is to be shown
            elif self.shuffle_count < self.max_shuffles:
                self.maze.shuffle()
                self.shuffle_count += 1
                print(self.shuffle_count)
                if self.shuffle_count > self.max_shuffles:
                    self.maze_built = True
        else: # step the solving
            # if the steps of solving the maze is to be shown
            if self.SHOW_SOLVE:
                if self.SHOW_SOLVE:
                    pass
            # if the steps of solving the maze are not to be shown
            else:
                while not self.is_solved():
                    self.move()
                self.draw()
                return False

        return True

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

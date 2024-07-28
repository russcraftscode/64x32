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
        while self.anchor != self.get_node(self.cols - 1, self.rows - 1):
            self.shuffle()

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


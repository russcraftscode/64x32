import random
import pygame


######################
# Constants
######################
square_size = 30
square_start_x = square_size * 2
square_start_y = square_size * 2
MAP_X_SIZE = 64
MAP_Y_SIZE = 32
SCREEN_X = (square_start_x) + square_size * MAP_X_SIZE + (square_start_x)
SCREEN_Y = (square_start_y) + square_size * MAP_Y_SIZE + (square_start_y)

######################
# PyGame setup
######################

# Define the background color
# using RGB color coding.
background_color = (30, 30, 30)

# Define the dimensions of
# screen object(width,height)
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

# Set the caption of the screen
pygame.display.set_caption('MazeGen Test')

# Fill the background color to the screen
screen.fill(background_color)


######################
# Game Functions
######################


class Maze:
    def __init__(self):
        # create the nodes
        self.nodes = []
        for x in range(32):
            for y in range(16):
                self.nodes.append(Maze_Node(x, y))
        # link the nodes to their surroundings
        for x in range(1, 31):  # center nodes
            for y in range(1, 15):
                n = self.get_node(x, y)
                n.north = self.get_node(x, y - 1)
                n.east = self.get_node(x + 1, y)
                n.west = self.get_node(x - 1, y)
                n.south = self.get_node(x, y + 1)
        y = 0  # top row
        for x in range(1, 31):
            n = self.get_node(x, y)
            n.east = self.get_node(x + 1, y)
            n.west = self.get_node(x - 1, y)
            n.south = self.get_node(x, y + 1)
        y = 15  # bottom row
        for x in range(1, 31):
            n = self.get_node(x, y)
            n.north = self.get_node(x, y - 1)
            n.east = self.get_node(x + 1, y)
            n.west = self.get_node(x - 1, y)
        x = 0  # left side
        for y in range(1, 15):
            n = self.get_node(x, y)
            n.north = self.get_node(x, y - 1)
            n.east = self.get_node(x + 1, y)
            n.south = self.get_node(x, y + 1)
        x = 31  # right side
        for y in range(1, 15):
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
        x = 31
        y = 0
        n = self.get_node(x, y)
        n.west = self.get_node(x - 1, y)
        n.south = self.get_node(x, y + 1)
        # lower left corner
        x = 0
        y = 15
        n = self.get_node(x, y)
        n.north = self.get_node(x, y - 1)
        n.east = self.get_node(x + 1, y)
        # lower right corner
        x = 31
        y = 15
        n = self.get_node(x, y)
        n.north = self.get_node(x, y - 1)
        n.west = self.get_node(x - 1, y)
        self.anchor = n

        # add the direction properties to each node by linking it to the next node
        for y in range(16):
            for x in range(31):
                self.get_node(x, y).next = self.get_node(x, y).east
            self.get_node(31, y).next = self.get_node(31, y).south

    def shuffle(self):
        next_to_anchor = self.next_to(self.anchor)
        new_anchor = random.choice(next_to_anchor)
        self.anchor.next = new_anchor
        self.anchor = new_anchor
        self.anchor.next = None

    def next_to(self, node):
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
        screen.fill(background_color)
        for n in self.nodes:
            square = (
                n.x_pos * 2 * square_size + square_start_x, n.y_pos * 2 * square_size + square_start_y, square_size,
                square_size)
            if n == self.anchor:
                pygame.draw.rect(screen, (200, 0, 0), square)
            else:
                pygame.draw.rect(screen, (200, 200, 200), square)
            if n.next != None:
                #print(n.next)
                #print(f"{n.x_pos}   {n.y_pos}")
                #print(n.x_pos + " " + n.y_pos)
                square = ((n.x_pos + n.next.x_pos) / 2 * 2 * square_size + square_start_x,
                          (n.y_pos + n.next.y_pos) / 2 * 2 * square_size + square_start_y, square_size, square_size)
                pygame.draw.rect(screen, (200, 200, 200), square)


class Maze_Node:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.next = None


class Depth_Maze_Solver:
    def __init__(self, maze):
        self.visited_spaces = []
        self.current_path = []
        self.maze = maze
        self.current_path.append(maze.get_node(0, 0))

    # this function returns the options leading out of the given maze location
    def get_options(self, node):
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

    # this function will either move one more space towards the goal or retreat to look for another path
    def move(self):
        # determine if we are searching or retreating
        options = self.get_options(self.current_path[-1])
        viable_options = []
        for option in options:
            if option not in self.visited_spaces:
                viable_options.append(option)
        if len(viable_options) > 0:
            self.search(viable_options)
        else:
            self.retreat();


    def search(self, viable_options):
        self.visited_spaces.append(viable_options[0])
        self.current_path.append(viable_options[0])

    def retreat(self):
        self.current_path.pop()

    def draw(self):
        self.maze.draw()
        prev_square = self.current_path[0]
        for n in self.current_path:
            square = (
                n.x_pos * 2 * square_size + square_start_x, n.y_pos * 2 * square_size + square_start_y, square_size,
                square_size)
            pygame.draw.rect(screen, (0, 200, 0), square)
            if prev_square != n:
                square = ((n.x_pos + prev_square.x_pos) / 2 * 2 * square_size + square_start_x,
                          (n.y_pos + prev_square.y_pos) / 2 * 2 * square_size + square_start_y, square_size, square_size)
                pygame.draw.rect(screen, (0, 200, 0), square)
            prev_square = n

        n = self.current_path[-1]
        square = (
            n.x_pos * 2 * square_size + square_start_x, n.y_pos * 2 * square_size + square_start_y, square_size,
            square_size)
        pygame.draw.rect(screen, (0, 250, 0), square)

    def is_solved(self):
        if self.maze.anchor in self.current_path:
            return True
        else: return False




pygame.init()
while True:
    maze = Maze()
    solver = Depth_Maze_Solver(maze)

    running = True

    draw_counter = 0

    # game loop
    maze.draw()
    pygame.display.update()
    while running:
        maze.shuffle()
        #maze.draw()
        #pygame.display.flip()
        # pygame.time.wait(10)
        draw_counter += 1
        if draw_counter == 4000: running = False

    solver.draw()
    pygame.display.flip()
    while solver.is_solved() == False:
        solver.move()
        solver.draw()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.time.wait(4000)
pygame.quit()

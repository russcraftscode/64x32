# Spectrum code by Grismar credit: https://stackoverflow.com/questions/66630051/how-to-create-a-1000-color-rgb-rainbow-gradient-in-python
# Maze randomization algorithm by CaptainLuma credit: https://github.com/CaptainLuma/New-Maze-Generating-Algorithm



from maze import Maze

COLOR_ADVANCE = 5



class Width_Maze_Solver:
    """ solves a maze by searching wide"""

    def __init__(self, grid, whole_layer_step=False, show_solve = False, show_maze_build = False):
        self.grid = grid
        self.visited_spaces = []
        self.x_size = grid.cols // 2
        self.y_size = grid.rows // 2
        self.maze = Maze(self.grid, self.x_size, self.y_size)
        self.layers = [[self.maze.nodes[0]]]
        self.current_layer = [self.maze.nodes[0]]
        self.working_layer = []
        self.spectrum = []
        self.maze_built = False
        self.shuffle_count = 0
        self.max_shuffles = self.y_size * self.x_size * 10
        for r, g, b in zip(
                (list(reversed(range(256))) + [0] * 256),
                (list(range(256)) + list(reversed(range(256)))),
                ([0] * 256 + list(range(256)))):
            self.spectrum.append([r, g, b])
        self.spectrum.reverse()
        self.WHOLE_LAYER_STEPS = whole_layer_step
        self.SHOW_SOLVE = show_solve
        self.SHOW_MAZE = show_maze_build


    def step(self):
        """advances one graphical step. Returns false when it is time to create a new Wide_Maze_Solver object"""
        if self.maze_built == False:  # step the maze generation
            if self.SHOW_MAZE == False:  # if maze generation is not to be shown
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
                self.maze.draw()
                if self.shuffle_count > self.max_shuffles:
                    self.maze_built = True
        else:  # step the solving
            # determine if we have a full layer
            full_layer = True
            for n in self.current_layer:
                if n not in self.working_layer:
                    full_layer = False
            # if only animating whole layers
            if self.WHOLE_LAYER_STEPS:
                # fill up the layer
                while not full_layer:
                    self.working_layer.append(self.current_layer[len(self.working_layer)])
                    full_layer = True
                    for n in self.current_layer:
                        if n not in self.working_layer:
                            full_layer = False
                new_layer = []
                for n in self.current_layer:
                    new_layer.append(n)
                self.layers.append(new_layer)
                self.current_layer = self.next_layer()
                self.draw()
                #if the maze hase been solved
                if self.maze.anchor in self.working_layer:
                    return False
                self.working_layer = []
            if not self.WHOLE_LAYER_STEPS:
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
                self.draw()
                solved = self.maze.anchor in self.working_layer
                return not solved
        return True

    def step_old(self):
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
        #draw the prvious layers
        for l_count, layer in enumerate(self.layers):
            if color_counter < len(self.spectrum) - 20: color_counter += COLOR_ADVANCE
            for n in layer:
                self.grid.set_pixel(n.x_pos * 2, n.y_pos * 2,
                                    [self.spectrum[color_counter][0], self.spectrum[color_counter][1],
                                     self.spectrum[color_counter][2]])
                if l_count > 1:
                    # connect node with its previous node
                    prev_node = None
                    if n.north in self.layers[l_count - 1]:
                        if n.north.next == n: prev_node = n.north
                        if n.next == n.north: prev_node = n.north
                    if n.east in self.layers[l_count - 1]:
                        if n.east.next == n: prev_node = n.east
                        if n.next == n.east: prev_node = n.east
                    if n.west in self.layers[l_count - 1]:
                        if n.west.next == n: prev_node = n.west
                        if n.next == n.west: prev_node = n.west
                    if n.south in self.layers[l_count - 1]:
                        if n.south.next == n: prev_node = n.south
                        if n.next == n.south: prev_node = n.south
                    if prev_node != None:
                        self.grid.set_pixel((n.x_pos + prev_node.x_pos) * 2 // 2, (n.y_pos + prev_node.y_pos) * 2 // 2,
                                            [self.spectrum[color_counter][0], self.spectrum[color_counter][1],
                                             self.spectrum[color_counter][2]])
        #draw the current search layer
        for n in self.working_layer:
            self.grid.set_pixel(n.x_pos * 2, n.y_pos * 2,
                                [self.spectrum[color_counter + COLOR_ADVANCE][0],
                                 self.spectrum[color_counter + COLOR_ADVANCE][1],
                                 self.spectrum[color_counter + COLOR_ADVANCE][2]])
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
                if n.next == n.south: prev_node = n.south
                if n.next == n.south: prev_node = n.south
            if prev_node != None:
                self.grid.set_pixel((n.x_pos + prev_node.x_pos) * 2 // 2, (n.y_pos + prev_node.y_pos) * 2 // 2,
                                    [self.spectrum[color_counter + COLOR_ADVANCE][0],
                                     self.spectrum[color_counter + COLOR_ADVANCE][1],
                                     self.spectrum[color_counter + COLOR_ADVANCE][2]])

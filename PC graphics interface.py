"""This acts as the interface to run the 64x32 modules on a desktop with pygame."""

import pygame
from maze_depth_first import Maze, Depth_Maze_Solver
import Pixel_Grid
from maze_wide import Width_Maze_Solver

# Constants
FRAME_RATE = 30
SQUARE_SIZE = 30
SQUARE_START_X = SQUARE_SIZE * 2
SQUARE_START_Y = SQUARE_SIZE * 2
PIXELS_X = 64
PIXELS_Y = 32
SCREEN_SIZE_X = (SQUARE_START_X) + SQUARE_SIZE * PIXELS_X + (SQUARE_START_X)
SCREEN_SIZE_Y = (SQUARE_START_Y) + SQUARE_SIZE * PIXELS_Y + (SQUARE_START_Y)
BACKGROUND_COLOR = [30, 30, 30]
MAX_MAZE_SHUFFLES = 4000

######################
# PyGame setup
######################


# Define the dimensions of
# screen object(width,height)
screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))

# Set the caption of the screen
pygame.display.set_caption('64x32 Desktop')

# Fill the background color to the screen
screen.fill(BACKGROUND_COLOR)


######################
# UI Functions
######################

def draw(grid):
    #grid.fill(BACKGROUND_COLOR)
    for y in range(grid.rows):
        for x in range(grid.cols):
            square = (x * SQUARE_SIZE + SQUARE_START_X, y * SQUARE_SIZE + SQUARE_START_Y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, grid.get_pixel(x, y), square)
    pygame.display.flip()


######################
# PyGame Execute
######################
mode = "startup"
grid = Pixel_Grid.Pixel_Grid(PIXELS_X, PIXELS_Y, BACKGROUND_COLOR)

print("initializing pygame")
pygame.init()
print("pygame initialized")
while True:
    match mode:
        case "startup":

            mode = "main menu"
            print("startup")
            #grid.fill((100, 10, 10))
            draw(grid)
            #mode = "pixel test"
        case "main menu":
            print("main menu")
            mode = "width"

        case "pixel test":
            spectrum = []
            for r, g, b in zip(
                    (list(reversed(range(256))) + [0] * 256),
                    (list(range(256)) + list(reversed(range(256)))),
                    ([0] * 256 + list(range(256)))):
                        spectrum.append([r, g, b])
            spectrum.pop()
            running = True
            while running:
                # input
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        show_shuffle = False
                        if event.key == pygame.K_SPACE:
                            running = False
                            print("space key")
                            mode = "width"
                            solved = True
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                for row in range(PIXELS_Y):
                    for col in range(PIXELS_X):
                        color_count += 1
                        if color_count >= len(spectrum): color_count = 0
                        grid.set_pixel(col, row, spectrum[color_count])
                draw(grid)
                pygame.time.wait(1000 // FRAME_RATE)

        case "depth":
            # Create Objects
            maze = Maze(grid, PIXELS_X, PIXELS_Y)
            solver = Depth_Maze_Solver(maze, grid)
            #set up loop
            running = True
            solved = False
            show_shuffle = False
            shuffling_done = False
            #main mode loop
            while not solved:
                # input
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        show_shuffle = False
                        if event.key == pygame.K_SPACE:
                            running = False
                            print("space key")
                            mode = "breadth"
                            solved = True
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()

                #check sub mode
                if not shuffling_done:
                    shuffling_done = maze.shuffle()
                    if show_shuffle:
                        maze.draw()
                        draw(grid)
                        #pygame.time.wait(1000 // FRAME_RATE)
                else:
                    solver.move()
                    solver.draw()
                    draw(grid)
                    if solver.is_solved(): solved = True
                    pygame.time.wait(1000 // FRAME_RATE)
            mode = "width"
        case "width":
            # Create Objects
            maze = Maze(grid, PIXELS_X, PIXELS_Y)
            solver = Width_Maze_Solver(maze, grid)
            #set up loop
            running = True
            solved = False
            show_shuffle = False
            shuffling_done = False
            #main mode loop
            while not solved:
                # input
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        show_shuffle = False
                        if event.key == pygame.K_SPACE:
                            running = False
                            print("space key")
                            mode = "main menu"
                            solved = True
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()

                #check sub mode
                if not shuffling_done:
                    shuffling_done = maze.shuffle()
                    if show_shuffle:
                        maze.draw()
                        draw(grid)
                else:
                    #solved = solver.move()
                    solved = solver.step()
                    solver.draw()
                    draw(grid)
                    pygame.time.wait(1000 // FRAME_RATE)
            mode = "depth"

d

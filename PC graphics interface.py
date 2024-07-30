"""This acts as the interface to run the 64x32 modules on a desktop with pygame."""

import pygame
import Pixel_Grid
from maze_wide import Wide_Maze_Solver
from maze_deep import Deep_Maze_Solver
from maze_versus import Versus_Solver
from rainfall import Rainfall
from starfield import Starfield

# Constants
FRAME_RATE = 30

SQUARE_SIZE = 46
#SQUARE_SIZE = 8

PIXELS_X = 64
PIXELS_Y = 32
#PIXELS_X = 256
#PIXELS_Y = 128

SQUARE_START_X = SQUARE_SIZE * 2
SQUARE_START_Y = SQUARE_SIZE * 2
SCREEN_SIZE_X = (SQUARE_START_X) + SQUARE_SIZE * PIXELS_X + (SQUARE_START_X)
SCREEN_SIZE_Y = (SQUARE_START_Y) + SQUARE_SIZE * PIXELS_Y + (SQUARE_START_Y)
BACKGROUND_COLOR = [30, 30, 30]
MAX_MAZE_SHUFFLES = 4000

######################
# PyGame setup
######################


# Define the dimensions of
# screen object(width,height)
#screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
screen = pygame.display.set_mode((3840, 2160), pygame.FULLSCREEN ,  display=1)



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

            mode = "starfield"
            print("startup")
            draw(grid)

        case "starfield":
            stars = Starfield(grid )
            while stars.step() and mode == "starfield":
                draw(grid)
                pygame.time.wait(1000 // FRAME_RATE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            mode = "rainfall"
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
            draw(grid)
            pygame.time.wait(1000)

        case "rainfall":
            rain = Rainfall(grid, fillable=True )
            while rain.step() and mode == "rainfall":
                draw(grid)
                pygame.time.wait(1000 // FRAME_RATE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            mode = "wide"
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
            draw(grid)
            pygame.time.wait(1000)

        case "wide":
            solver = Wide_Maze_Solver(grid, whole_layer_step=True )
            while solver.step() and mode == "wide":
                draw(grid)
                #pygame.time.wait(1000 // FRAME_RATE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            mode = "deep"
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
            draw(grid)
            pygame.time.wait(1000)

        case "deep":
            solver = Deep_Maze_Solver(grid, show_solve=True, show_seek=True, show_visited=True )
            while solver.step() and mode == "deep":
                draw(grid)
                pygame.time.wait(1000 // FRAME_RATE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            mode = "versus"
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
            draw(grid)
            pygame.time.wait(1000)

        case "versus":
            solver = Versus_Solver(grid )
            while solver.step() and mode == "versus":
                draw(grid)
                pygame.time.wait(1000 // FRAME_RATE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            mode = "starfield"
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
            draw(grid)
            pygame.time.wait(1000)




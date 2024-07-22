"""This acts as the interface to run the 64x32 modules on a desktop with pygame."""

import pygame
import maze_depth_first



# Constants
FRAME_RATE = 30
SQUARE_SIZE = 30
SQUARE_START_X = SQUARE_SIZE * 2
SQUARE_START_Y = SQUARE_SIZE * 2
PIXELS_X = 64
PIXELS_Y = 32
SCREEN_SIZE_X = (SQUARE_START_X) + SQUARE_SIZE * PIXELS_X + (SQUARE_START_X)
SCREEN_SIZE_Y = (SQUARE_START_Y) + SQUARE_SIZE * PIXELS_Y + (SQUARE_START_Y)
BACKGROUND_COLOR = (30, 30, 30)

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
# PyGame Execute
######################

running = True
while running:
    #exit if escape or xbutton is pushed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #maze = Maze()
    #solver = Depth_Maze_Solver(maze)




pygame.quit()
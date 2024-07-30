"""This holds the RGB data for all pixels"""

class Pixel_Grid:
    def __init__(self, cols, rows, background):
        self.cols = cols
        self.rows = rows
        self.background_color = background
        total_pixels = cols * rows
        self.pixels = [[0, 0, 0] for x in range(total_pixels)]


    def fill(self, color):
        """ fills the entire grid with a specified color"""
        for i in range(len(self.pixels)):
            self.pixels[i] = color


    def wipe(self):
        """ clears the entire grid and fills it with the default color"""
        for i in range(len(self.pixels)):
            self.pixels[i] = self.background_color

    def get_pixel(self, x_pos, y_pos):
        """ returns the color of a specific pixel"""
        return self.pixels[y_pos * self.cols + x_pos]

    def set_pixel(self, x_pos, y_pos, color):
        """ sets the color of a specific pixel"""
        self.pixels[y_pos * self.cols + x_pos] = color
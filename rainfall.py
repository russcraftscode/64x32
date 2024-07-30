import random


class Rainfall:
    def __init__(self, grid, fillable=False):
        self.grid = grid
        self.x_size = grid.cols
        self.y_size = grid.rows
        self.droplets = []
        self.water_level = self.y_size
        self.max_water_level = 4
        self.drop_count = 0
        self.fillable = fillable

    def draw(self):
        self.grid.wipe()
        for drop in self.droplets:
            # of the drop hasn't hit the water, draw it falling
            if drop.row < self.water_level:
                self.grid.set_pixel(drop.col, drop.row, drop.color)
            # if the drop hit the water this frame or the previous frame draw a splash
            if drop.row == self.water_level:
                self.grid.set_pixel(drop.col-1, self.water_level-1, drop.color)
                self.grid.set_pixel(drop.col+1, self.water_level-1, drop.color)
        #draw the rising water
        if self.water_level < self.y_size:
            for row_count in range( self.water_level, self.y_size):
                for col_count in range( self.x_size):
                    self.grid.set_pixel( col_count, row_count, [10,10,200])


    def step(self):
        # add a new drop in a random location
        self.droplets.append(Droplet(random.randint(1,self.x_size-2), self.y_size, [10, 10, 200]))
        # move each drop
        for drop in self.droplets:
            if not drop.move():
                self.droplets.remove(drop)
                self.drop_count += 1
        # if enough drops have fallen raise the water level by 1 row
        if self.fillable:
            if self.drop_count > (self.x_size * 5):
                self.water_level -= 1
                self.drop_count = 0
                # don't raise the water level above max
                if self.water_level < self.max_water_level:
                    #self.water_level = self.max_water_level
                    return False

        self.draw()
        return True


class Droplet:
    def __init__(self, col, bottom_row, color):
        self.row = 0
        self.col = col
        self.bottom_row = bottom_row
        self.color = color

    def move(self):
        """moves the drop 1 row down. Returns False when drop goes off screen"""
        self.row += 1
        if self.row >= self.bottom_row:
            return False
        return True

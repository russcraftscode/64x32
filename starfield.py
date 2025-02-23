import random


class Starfield:
    def __init__(self, grid, ):
        self.grid = grid
        self.x_size = grid.cols
        self.y_size = grid.rows
        self.stars = []
        self.x_center = self.x_size // 2
        self.y_center = self.y_size // 2

    def draw(self):
        self.grid.wipe()
        for star in self.stars:
            #print(f"{star.x_pos=}, {star.y_pos=}")
            # if the star is out of view, don't draw it
            if star.x_pos > 0 and star.x_pos < self.x_size and star.y_pos > 0 and star.y_pos < self.y_size:
                self.grid.set_pixel(int(star.x_pos), int(star.y_pos), star.color)

    def step(self):
        # add a new star in a random location
        dist = random.random() * 5
        rise = (random.random() * 2 - 1 ) / dist
        run = (random.random() * 2 - 1 ) / dist
        color = (170 - 20 * int (dist))
        #print(color)
        self.stars.append(
            Star(self.x_center + dist*10 * run, self.y_center + dist*10 * rise, rise, run, dist,[color, color, color])
        )
        #print(self.stars)# DEBUG
        # move each star
        for star in self.stars:
            star.move()
        self.draw()
        return True



class Star:
    def __init__(self, x, y, rise, run, dist, color):
        self.x_pos = x
        self.y_pos = y
        self.rise = rise
        self.run = run
        self.dist = dist
        self.color = color

    def move(self):
        """moves the star"""
        self.x_pos += self.run
        self.y_pos += self.rise
        self.rise = self.rise* (1+(6-self.dist)/100)
        self.run = self.run* (1+(6-self.dist)/100)


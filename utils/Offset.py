from math import *


class Offset:
    def __init__(self):
        self.center_x = 0.0
        self.center_y = 0.0
        self.min_y = inf
        self.max_y = -inf
        self.min_x = inf
        self.max_x = -inf

    def modify_offset(self, point):
        if(point.x < self.min_x):
            self.min_x = point.x
        if(point.x > self.max_x):
            self.max_x = point.x
        if (point.y < self.min_y):
            self.min_y = point.y
        if (point.y > self.max_y):
            self.max_y = point.y

    def setup_offset(self):
        self.center_x = self.min_x + ((self.max_x - self.min_x) / 2.0)
        self.center_y = self.min_y + ((self.max_y - self.min_y) / 2.0)

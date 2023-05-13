from math import *


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

# This function will return the vector normal of a triangle
def normal(a, b, c):
    N1 = (b.y - a.y) * (c.z - a.z) - (b.z - a.z) * (c.y - a.y)
    N2 = (b.z - a.z) * (c.x - a.x) - (b.x - a.x) * (c.z - a.z)
    N3 = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    return ceil(N1*100)/100, ceil(N2*100)/100, ceil(N3*100)/100

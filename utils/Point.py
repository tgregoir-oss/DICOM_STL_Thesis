class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


def make_point_offset(x, y, z, i, GO, z_values, size):
    new_x = 0.0
    new_y = 0.0
    new_z = 0.0
    x = x -size/2
    y = y -size/2
    if   (i == 0):
        new_x = ((x+1)/size)*(GO.max_x - GO.min_x) + GO.center_x
        new_y = (((2*y+1)/2)/size)*(GO.max_y - GO.min_y) + GO.center_y
        new_z = z_values[z+1]
    elif (i == 1):
        new_x = (((2*x+1)/2)/size)* (GO.max_x - GO.min_x) + GO.center_x
        new_y = ((y+1) / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = z_values[z + 1]
    elif (i == 2):
        new_x = (x/ size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = (((2*y+1)/2)/size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = z_values[z + 1]
    elif (i == 3):
        new_x = (((2*x+1)/2)/size)  * (GO.max_x - GO.min_x) + GO.center_x
        new_y = (y/ size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = z_values[z + 1]
    elif (i == 4):
        new_x = ((x + 1) / size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = (((2 * y + 1) / 2) / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = z_values[z]
    elif (i == 5):
        new_x = (((2 * x + 1) / 2) / size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = ((y + 1) / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = z_values[z]
    elif (i == 6):
        new_x = (x / size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = (((2 * y + 1) / 2) / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = z_values[z ]
    elif (i == 7):
        new_x = (((2 * x + 1) / 2) / size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = (y / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = z_values[z]
    elif (i == 8):
        new_x = ((x+1) / size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = (y / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = (z_values[z]+z_values[z+1])/2
    elif (i == 9):
        new_x = ((x + 1) / size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = ((y+1) / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = (z_values[z] + z_values[z + 1]) / 2
    elif (i == 10):
        new_x = ((x) / size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = ((y+1) / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = (z_values[z] + z_values[z + 1]) / 2
    else:
        new_x = (x / size) * (GO.max_x - GO.min_x) + GO.center_x
        new_y = (y / size) * (GO.max_y - GO.min_y) + GO.center_y
        new_z = (z_values[z] + z_values[z + 1]) / 2
    return Point(new_x, new_y, new_z)

def make_point(x, y, z, i, z_values):
    new_x = 0.0
    new_y = 0.0
    new_z = 0.0
    if   (i == 0):
        new_x = (x+1)
        new_y = ((2*y+1)/2)
        new_z = z_values[z+1]
    elif (i == 1):
        new_x = ((2*x+1)/2)
        new_y = (y+1)
        new_z = z_values[z + 1]
    elif (i == 2):
        new_x = x
        new_y = ((2*y+1)/2)
        new_z = z_values[z + 1]
    elif (i == 3):
        new_x = ((2*x+1)/2)
        new_y = y
        new_z = z_values[z + 1]
    elif (i == 4):
        new_x = (x + 1)
        new_y = ((2 * y + 1) / 2)
        new_z = z_values[z]
    elif (i == 5):
        new_x = ((2 * x + 1) / 2)
        new_y = (y + 1)
        new_z = z_values[z]
    elif (i == 6):
        new_x = x
        new_y = ((2 * y + 1) / 2)
        new_z = z_values[z ]
    elif (i == 7):
        new_x = ((2 * x + 1) / 2)
        new_y = y
        new_z = z_values[z]
    elif (i == 8):
        new_x = (x+1)
        new_y = y
        new_z = (z_values[z]+z_values[z+1])/2
    elif (i == 9):
        new_x = (x + 1)
        new_y = (y+1)
        new_z = (z_values[z] + z_values[z + 1]) / 2
    elif (i == 10):
        new_x = (x)
        new_y = (y+1)
        new_z = (z_values[z] + z_values[z + 1]) / 2
    else:
        new_x = x
        new_y = y
        new_z = (z_values[z] + z_values[z + 1]) / 2
    return Point(new_x, new_y, new_z)

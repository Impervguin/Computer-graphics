def sign(x):
    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    return -1

def color_intensity(color, intensity):
    return tuple(int(c + (255 - c) * (1 - intensity)) for c in color)
def sign(x):
    if (x > 0):
        return 1
    elif (x == 0):
        return 0
    return -1

def color_intensity(color, intensity):
    return tuple(int(c + (255 - c) * (1 - intensity)) for c in color)

def mathRound(x):
    i = int(x)
    if x - i >= 0.5:
        return i + 1
    return i

def average(lst):
    if (len(lst)) == 0:
        return 0
    return sum(lst) / len(lst)
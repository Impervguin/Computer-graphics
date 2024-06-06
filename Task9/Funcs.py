from Point import Point

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

def line_koefs(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return a, b, c

def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1 * b2 - a2 * b1
    opr1 = (-c1) * b2 - b1 * (-c2)
    opr2 = a1 * (-c2) - (-c1) * a2

    x = opr1 / opr
    y = opr2 / opr

    return x, y


def interval_intersection(p1, p2, c1, N : Point):
    D = Point(p2[0] - p1[0], p2[1] - p1[1])
    Wi = Point(p1[0] - c1[0], p1[1] - c1[1])

    Wscalar = N.scalar(Wi)
    Dscalar = N.scalar(D)
    if Dscalar == 0:
        raise ValueError("No intersection")

    t = - Wscalar / Dscalar

    return Point(p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1]- p1[1]) * t)

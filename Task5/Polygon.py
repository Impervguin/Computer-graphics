from Point import *
from Funcs import *
from math import ceil

class Polygon:
    def __init__(self, *points):
        self.points = [p for p in points]
    
    def __len__(self):
        return len(self.points)
    
    def __getitem__(self, key):
        return self.points[key]

    def XRange(self):
        return min(p[0] for p in self.points), max(p[0] for p in self.points) + 1

    def YRange(self):
        return min(p[1] for p in self.points), max(p[1] for p in self.points)
    
    def IntersectionWScan(self):
        pixels = []
        for i in range(-1, len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            min_y = min(p1[1], p2[1])
            max_y = max(p1[1], p2[1])
            x = p1[0]
            if (p1[1] > p2[1]):
                x = p2[0]
            if (p1[1] == p2[1]):
                continue
            a_side, b_side, c_side = line_koefs(p1[0], p1[1], p2[0], p2[1])
            for y in range(min_y, max_y):
                a_scan_line, b_scan_line, c_scan_line = line_koefs(x, y, x + 1, y)

                x_intersec, _ = solve_lines_intersection(a_side, b_side, c_side, a_scan_line, b_scan_line, c_scan_line)
                x_ = int(x_intersec + 0.5)
                if ((x_,y) in pixels):
                    del pixels[pixels.index((x_, y))]
                    # x_ += 1
                else:
                    pixels.append((x_, y))
                
        return pixels


if __name__ == "__main__":
    p = Polygon((1, 1), (1, 7), (5, 3), (8, 6), (8, 1))
    p = p.IntersectionWScan()
    print(*sorted(p, key=lambda x: x[0]), sep="\n")

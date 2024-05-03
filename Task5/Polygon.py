from Point import *
from Funcs import mathRound


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
        return min(p[1] for p in self.points), max(p[1] for p in self.points) + 1
    
    def IntersectionWScan(self, y):
        pixels = []
        i = -1
        while i < len(self) - 1:
            # p1, p2 = self[i], self[i + 1]
            # if (p1[1] == p2[1]):
            #     i += 1
            #     continue
            # dx = (p2[0] - p1[0]) / abs(p2[1] - p1[1])
            # # print(dx)
            # j = 0
            # # print(f"{p1}, {p2}:")
            # for y in range(p1[1], p2[1], 1 if p1[1] < p2[1] else -1):
            #     x = mathRound(p1[0] + dx * j)
            #     # print(x)
            #     pixels.append((x, y))
            #     j += 1
            # i += 1

            p1, p2 = self[i], self[i + 1]
            if max(p1[1], p2[1]) < y or min(p1[1], p2[1]) > y:
                i += 1
                continue
            if p1[1] == p2[1]:
                i += 1
                continue
            if (p2[1] == y):
                if max(self[i - 1], self[i + 1])[1] > p2[1] and min(self[i - 1], self[i + 1])[1] < p2[1]:
                    pixels.append(p2[0])
                i += 2
                continue

            x = int(p1[0] + (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1]))
            # if x >= min(p1[0], p2[0]) and x <= max(p1[0], p2[0]):
            pixels.append(x)
            i += 1
        return pixels


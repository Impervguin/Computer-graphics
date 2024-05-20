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
                    # x_ += 1
                    del pixels[pixels.index((x_, y))]
                else:
                    pixels.append((x_, y))
                
        return pixels
    
    def IntersectionWScanWOtherPixels(self, pixels):
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
                else:
                    pixels.append((x_, y))
                
        return pixels

    def AddPoint(self, p : Point):
        self.points.append(p)
    
    def Pop(self):
        return self.points.pop()
    

class Rectangle(Polygon):
    def __init__(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        super().__init__(Point(x1, y1), Point(x1, y2), Point(x2, y2), Point(x2, y1))
        self.left = min(x1, x2)
        self.right = max(x1, x2)
        self.bottom = min(y1, y2)
        self.top = max(y1, y2)
    
    def SutherlandCohenCode(self, p : Point):
        code = 0
        if p[0] < self.left:
            code |= 1
        if p[0] > self.right:
            code |= 2
        if p[1] < self.bottom:
            code |= 4
        if p[1] > self.top:
            code |= 8
        return code


    def SutherlandCohen(self, p1 : Point, p2: Point):
        p1 = p1.copy()
        p2 = p2.copy()
        FL = 0
        rect = [self.left, self.right, self.bottom, self.top]
        T1 = self.SutherlandCohenCode(p1)
        T2 = self.SutherlandCohenCode(p2)
        if T1 & T2 != 0: # Отрезок невидим
            return Point(0, 0), Point(0, 0)

        if (p1[0] == p2[0]):
            FL = -1
        else:
            m = (p2[1] - p1[1]) / (p2[0] - p1[0])
            if m == 0:
                FL = 1
        
        for i in range(4):
            T1 = self.SutherlandCohenCode(p1)
            T2 = self.SutherlandCohenCode(p2)
            if T1 == 0 and T2 == 0: # Отрезок полностью видим
                return p1, p2
            if T1 & T2 != 0: # Отрезок невидим
                return Point(0, 0), Point(0, 0)
            
            if T2 & (2 ** i) == 0 and T1 & (2 ** i) == 0:
                continue
            if T1 & (2 ** i) == 0:
                p1, p2 = p2, p1
            if FL == -1:
                p1[1] = rect[i]
            elif i < 2:
                p1[1] = m * (rect[i] - p1[0]) + p1[1]
                p1[0] = rect[i]
            else:
                p1[0] = (rect[i] - p1[1]) / m + p1[0]
                p1[1] = rect[i]
        return p1, p2




if __name__ == "__main__":
    rect = Rectangle((439, 355), (861, 575))
    p1 = Point(932, 271)
    p2 = Point(486, 753)
    print(*rect.SutherlandCohen(p1, p2), sep=" ")

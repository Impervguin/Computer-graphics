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
    
    def IsDegenerate(self):
        vectors = [Point(self.points[i + 1][0] - self.points[i][0], self.points[i + 1][1] - self.points[i][1]) for i in range(-1, len(self.points) - 1)]
        
        return len(self.points) < 3 or all([vectors[i].vector(vectors[i + 1]) == 0 for i in range(-1, len(self.points) - 1)])

    def IsCortex(self):
        vectors = [Point(self.points[i + 1][0] - self.points[i][0], self.points[i + 1][1] - self.points[i][1]) for i in range(-1, len(self.points) - 1)]
        
        return len(self.points) < 3 or \
            (all([vectors[i].vector(vectors[i + 1]) > 0 for i in range(-1, len(vectors) - 1)]) or \
            all([vectors[i].vector(vectors[i + 1]) < 0 for i in range(-1, len(vectors) - 1)])) and \
            not self.IsDegenerate()
    
    def getInnerNormal(self, index):
        if not self.IsCortex():
            raise ValueError("Polygon is not cortex.")
        p1 = self.points[index]
        p2 = self.points[(index + 1) % len(self.points)]

        vec = Point(p2[0] - p1[0], p2[1] - p1[1])
        normal = Point(-vec[1], vec[0])
        normal = Point(normal[0] / normal.vectorLength(), normal[1] / normal.vectorLength())

        for i in range(2, len(self.points)):
            p3 = self.points[(index + i) % len(self.points)]
            otherVec = Point(p3[0] - p1[0], p3[1] - p1[1])
            if normal.scalar(otherVec) < 0:
                normal = Point(-normal[0], -normal[1])
                return normal
            elif normal.scalar(otherVec) > 0:
                return normal
        
        return normal
    
    def KirusBeck(self, p1: Point, p2: Point):
        D = Point(p2[0] - p1[0], p2[1] - p1[1])
        ts, te = 0, 1

        for i in range(len(self.points)):
            N = self.getInnerNormal(i)
            Wi = Point(p1[0] - self.points[i][0], p1[1] - self.points[i][1])

            Wscalar = N.scalar(Wi)
            Dscalar = N.scalar(D)
            if Dscalar == 0 and Wscalar < 0:
                return Point(0, 0), Point(0, 0)
            elif Dscalar == 0:
                continue
            
            t = - Wscalar / Dscalar

            if Dscalar > 0:
                ts = max(ts, t)
            else:
                te = min(te, t)
        
        if ts > te:
            return Point(0, 0), Point(0, 0)
        start = Point(p1[0] + (p2[0] - p1[0]) * ts, p1[1] + (p2[1]- p1[1]) * ts)
        end = Point(p1[0] + (p2[0] - p1[0]) * te, p1[1] + (p2[1]- p1[1]) * te)
        return start, end

    def SutherlandHojmann(self, polygon):
        res = Polygon()
        for i in range(len(self)):
            # print(i)
            p1, p2 = self[i], self[(i + 1) % len(self)]
            N = self.getInnerNormal(i)
            res = Polygon()

            for j in range(len(polygon)):
                cp1, cp2 = polygon[j], polygon[(j + 1) % len(polygon)]

                vec1 = Point(cp1[0] - p1[0], cp1[1] - p1[1])
                vec2 = Point(cp2[0] - p1[0], cp2[1] - p1[1])

                scalar1 = N.scalar(vec1)
                scalar2 = N.scalar(vec2)

                if scalar1 <= 0 and scalar2 <= 0:
                    continue
                elif scalar1 > 0 and scalar2 > 0:
                    res.AddPoint(cp2)
                    continue
                elif scalar1 <= 0 and scalar2 > 0:
                    res.AddPoint(interval_intersection(cp1, cp2, p1, N))
                    res.AddPoint(cp2)
                    continue
                else:
                    res.AddPoint(interval_intersection(cp1, cp2, p1, N))
            
            if (len(res) == 0):
                return res
            # cp1, cp2 = polygon[-1], polygon[0]
            # vec1 = Point(cp1[0] - p1[0], cp1[1] - p1[1])
            # vec2 = Point(cp2[0] - p1[0], cp2[1] - p1[1])

            # scalar1 = N.scalar(vec1)
            # scalar2 = N.scalar(vec2)

            # if scalar1 < 0 and scalar2 >= 0 or scalar1 >= 0 and scalar2 < 0:
            #     res.AddPoint(interval_intersection(cp1, cp2, p1, N))

            polygon = res
        return res
            
            




            
                    

    

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
            
            if T2 & (2 ** i) == T1 & (2 ** i):
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

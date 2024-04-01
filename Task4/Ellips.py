from Point import Point
from DrawField import DrawField
from Funcs import sign, color_intensity, mathRound
import math as m
import time

class Ellips:
    def __init__(self, center, w, h) -> None:
        self.c = center
        self.w = w
        self.h = h
    
    def draw(self, screen : DrawField, color=(0, 0, 0)):
        points = self._draw()
        for p in points:
            self.DrawPixel(screen, p[0], p[1], color_intensity(color, p.intensity))
    
    def _draw(self) -> list[Point]:
        pass

    # def drawSpectre(self, step, screen : DrawField, color=(0,0,0)):
    #     r = self.r
    #     s_p2 = self.p2
    #     a = 0
    #     l = ((self.p1[0] - self.p2[0]) ** 2 + (self.p1[1] - self.p2[0]) ** 2) ** 0.5
    #     while a < 360:
    #         self.p2 = Point(l * m.cos(m.radians(a)) + self.p1[0], l * m.sin(m.radians(a)) + self.p1[1])
    #         self.draw(screen, color)
    #         a += step
    #     self.p2 = s_p2


    def DrawPixel(self, screen : DrawField, x, y, color=(0,0,0)):
        screen.SetColor(color)
        screen.DrawPixel(x, y)
    
    def timeDraw(self, screen : DrawField, color=(0, 0, 0)):

        ts = time.time_ns()
        self.draw(screen, color)
        te = time.time_ns()

        return te - ts
    
    def shiftCenter(self, x, y):
        self.c.x += x
        self.c.y += y
    
    def getSymmetricPixels(self, x, y):
        cx = int(self.c[0])
        cy = int(self.c[1])
        dx = x - cx
        dy = y - cy

        return [Point(x, y), Point(cx - dx, cy + dy), Point(cx - dx, cy - dy), Point(cx + dx, cy - dy)]


class CanonicEllips(Ellips):
    def _draw(self) -> list[Point]:
        points = []
        sqrw = self.w ** 2
        sqrh = self.h ** 2
        xc, yc = self.c
        rightx = mathRound(xc + self.w / (m.sqrt(1 + sqrh / sqrw)))
        topy = mathRound(yc + self.h / (m.sqrt(1 + sqrw / sqrh)))
        # rightx, topy = topy, rightx

        for x in range(mathRound(xc), rightx + 1):
            y = mathRound(yc + self.h / self.w * m.sqrt(sqrw - (x - xc) ** 2))
            points.extend(self.getSymmetricPixels(x, y))
            # points.append(Point(x, y))
        
        for y in range(mathRound(yc), topy + 1):
            x = mathRound(xc + self.w / self.h * m.sqrt(sqrh - (y - yc) ** 2))
            points.extend(self.getSymmetricPixels(x, y))
            # points.append(Point(x, y))

        return points

class ParametricEllips(Ellips):
    def _draw(self) -> list[Point]:
        if self.w > self.h:
            step = 1 / self.w
        else:
            step = 1 / self.h
        points = []

        a = 0
        while a < m.pi / 2:
            x = mathRound(self.c[0] + self.w * m.cos(a))
            y = mathRound(self.c[1] + self.h * m.sin(a))
            points.extend(self.getSymmetricPixels(x, y))
            a += step
        return points

class BrezenhemEllips(Ellips):
    def _draw(self) -> list[Point]:
        points = []
        c = self.c.copy()
        self.shiftCenter(-c[0], -c[1])

        w = mathRound(self.w)
        h = mathRound(self.h)
        sqrh = h * h
        sqrw = w * w


        x = 0
        y = h
        points.extend(self.getSymmetricPixels(x, y))
        re = sqrh + sqrw * (h - 1) ** 2 - sqrw * sqrh
        
        while y >= 0:
            print(re)
            if re < 0:
                x += 1
                d = -2 * sqrw * y + sqrw
                if d >= 0:
                    y -= 1
                    re += 2 * sqrh * x - 2 * sqrw * y + sqrw + sqrh
                else:
                    re += 2 * sqrh * x + sqrh
            elif re > 0:
                y -= 1
                d = 2 * sqrh * x + sqrh
                if d >= 0:
                    x += 1
                    re += 2 * sqrh * x - 2 * sqrw * y + sqrw + sqrh
                else:
                    re -= 2 * sqrw * y + sqrw
            else:
                x += 1
                y -= 1
                re += 2 * sqrh * x - 2 * sqrw * y + sqrw + sqrh
            points.extend(self.getSymmetricPixels(x, y))

        for p in points:
            p.shift(int(c[0]), int(c[1]))
        self.shiftCenter(c[0], c[1])
        return points

class MidPointEllips(Ellips):
    def _draw(self) -> list[Point]:
        points = []
        c = self.c.copy()
        self.shiftCenter(-c[0], -c[1])

        x = 0
        y = mathRound(self.h)
        points.extend(self.getSymmetricPixels(x, y))
        
        sqrw = self.w ** 2
        sqrh = self.h ** 2
        rightx = mathRound(self.w / (m.sqrt(1 + sqrh / sqrw)))
        topy = mathRound(self.h / (m.sqrt(1 + sqrw / sqrh)))
        
        crit = sqrh + sqrw * (y - 1 / 2) ** 2 - sqrw * sqrh  

        for x in range(1, rightx + 1):
            if crit > 0:
                y -= 1
                crit -= 2 * sqrw * y
            points.extend(self.getSymmetricPixels(x, y))
            crit  += 2 * sqrh * x + sqrh
        
        x = mathRound(self.w)

        crit = sqrh * (x - 1 / 2) ** 2  + sqrw - sqrw * sqrh

        for y in range(1, topy + 1):
            if crit > 0:
                x -= 1
                crit -= 2 * sqrh * x
            points.extend(self.getSymmetricPixels(x, y))
            crit += 2 * sqrw * y + sqrw
        
        for p in points:
            p.shift(int(c[0]), int(c[1]))
        self.shiftCenter(c[0], c[1])

        return points


class LibraryEllips(Ellips):
    def draw(self, screen: DrawField, color=(0, 0, 0)):
        screen.drawEllipse(self.c, self.w, self.h, color)
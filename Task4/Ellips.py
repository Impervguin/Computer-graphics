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

    def drawSpectre(self, step, cnt, screen : DrawField, color=(0,0,0)):
        s_w = self.w
        s_h = self.h
        i = 0
        while i < cnt:
            self.draw(screen, color)
            self.h += step
            self.w += step
            i += 1
        self.w = s_w
        self.h = s_h

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

    def __str__(self) -> str:
        return "Канонический"

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

    def __str__(self) -> str:
        return "Параметрический"
    
class BrezenhemEllips(Ellips):
    def _draw(self) -> list[Point]:
        points = []
        c = self.c.copy()
        self.shiftCenter(-c[0], -c[1])

        w = mathRound(self.w)
        h = mathRound(self.h)
        sqrh = h * h
        sqrw = w * w
        sqrs = sqrh * sqrw


        x = 0
        y = h
        points.extend(self.getSymmetricPixels(x, y))
        re = sqrh + sqrw * (h - 1) ** 2 - sqrs
        
        while y >= 0:
            if re < 0 and re + sqrh * (x + 1) ** 2 - sqrs + sqrw * y ** 2 < 0:
                x += 1
                re += 2 * sqrh * x + sqrh
            elif re > 0 and re + sqrw * (y - 1) ** 2 - sqrs + sqrh * x ** 2 > 0:
                y -= 1
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

    def __str__(self) -> str:
        return "Брезенхем"

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
        sqrs = sqrw * sqrh
        rightx = mathRound(self.w / (m.sqrt(1 + sqrh / sqrw)))
        topy = mathRound(self.h / (m.sqrt(1 + sqrw / sqrh)))
        
        crit = sqrh + sqrw * (y - 1 / 2) ** 2 - sqrs

        for x in range(1, rightx + 1):
            if crit > 0:
                y -= 1
                crit -= 2 * sqrw * y
            points.extend(self.getSymmetricPixels(x, y))
            crit  += 2 * sqrh * x + sqrh
        
        x = mathRound(self.w)

        crit = sqrh * (x - 1 / 2) ** 2  + sqrw - sqrs

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

    def __str__(self) -> str:
        return "Средней точки"


class LibraryEllips(Ellips):
    def draw(self, screen: DrawField, color=(0, 0, 0)):
        screen.drawEllipse(self.c, self.w, self.h, color)
    
    def __str__(self) -> str:
        return "Библиотечный"
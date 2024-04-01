from Point import Point
from DrawField import DrawField
from Funcs import sign, color_intensity, mathRound
import math as m
import time

class Circle:
    def __init__(self, center, r) -> None:
        self.c = center
        self.r = r
    
    def draw(self, screen : DrawField, color=(0, 0, 0)):
        points = self._draw()
        for p in points:
            self.DrawPixel(screen, p[0], p[1], color_intensity(color, p.intensity))
        
    
    def _draw(self) -> list[Point]:
        pass

    def drawSpectre(self, step, cnt, screen : DrawField, color=(0,0,0)):
        s_r = self.r
        i = 0
        while i < cnt:
            self.draw(screen, color)
            self.r += step
            i += 1
        self.r = s_r


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


class BrezenhemCircle(Circle):
    def _draw(self):
        points = []
        c = self.c.copy()
        self.shiftCenter(-c[0], -c[1])

        x = 0
        y = mathRound(self.r)

        points.extend(self.getSymmetricPixels(x, y))

        delta = 2 * (1 - mathRound(self.r))

        while y >= 0:
            if delta < 0 :
                d = 2 * (delta + y) - 1
                x += 1
                if d <= 0:
                    delta += 2 * x - 1
                else:
                    y -= 1
                    delta += 2 * x - y * 2 + 2
                
            elif delta > 0:
                d = 2 * (delta - x) - 1
                y -= 1
                if d <= 0:
                    x += 1
                    delta += 2 * x - y * 2 + 2
                else:
                    delta -= 2 * y + 1
            else:
                x += 1
                y -= 1
                delta += 2 * x - y * 2 + 2
            
            points.extend(self.getSymmetricPixels(x, y))
        for p in points:
            p.shift(mathRound(c[0]), mathRound(c[1]))
        self.shiftCenter(c[0], c[1])
        return points
    
    def __str__(self) -> str:
        return "Брезенхем"


class MidPointCircle(Circle):
    def _draw(self) -> list[Point]:
        points = []
        c = self.c.copy()
        self.shiftCenter(-c[0], -c[1])

        x = int(self.r)
        y = 0
        sqr = mathRound(self.r ** 2)


        while y <= x:
            crit = 2 * ((x ** 2 + y ** 2 - sqr) + 2 * y + 1) - 2 * x + 1
            if crit > 0:
                x -= 1
            y += 1
            points.extend(self.getSymmetricPixels(x, y))


        while x >= 0:
            crit = 2 * (x ** 2 + y ** 2 - sqr - 2 * x + 1) + 2 * y + 1
            if crit < 0:
                y += 1
            x -= 1
            points.extend(self.getSymmetricPixels(x, y))

        for p in points:
            p.shift(int(c[0]), int(c[1]))
        self.shiftCenter(c[0], c[1])
        return points
    
    def __str__(self) -> str:
        return "Средней точки"



class CanonicCircle(Circle):
    def _draw(self) -> list[Point]:
        points = []
        sqr = self.r ** 2
        xc, yc = mathRound(self.c[0]), mathRound(self.c[1])
        rightx = mathRound(xc + self.r / m.sqrt(2))

        for x in range(xc, rightx + 1):
            y = mathRound(yc + m.sqrt(sqr - (x - xc) ** 2))
            points.extend(self.getSymmetricPixels(x, y))
        
        topy = mathRound(yc+ self.r / m.sqrt(2))
        for y in range(yc, topy + 1):
            x = mathRound(xc + m.sqrt(sqr - (y - yc) ** 2))
            points.extend(self.getSymmetricPixels(x, y))

        return points
    
    def __str__(self) -> str:
        return "Канонический"


class ParametricCircle(Circle):
    def _draw(self) -> list[Point]:
        points = []
        step = 1 / self.r
        xc, yc = self.c

        a = 0
        while a <= m.pi / 2:
            x = mathRound(xc + self.r * m.cos(a))
            y = mathRound(yc + self.r * m.sin(a))
            a += step
            points.extend(self.getSymmetricPixels(x, y))

        return points

    def __str__(self) -> str:
        return "Параметрический"

class LibraryCircle(Circle):
    def draw(self, screen : DrawField, color=(0, 0, 0)):
        screen.drawEllipse(self.c, self.r, self.r, color)
    
    def __str__(self) -> str:
        return "Библиотечный"

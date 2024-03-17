from Point import Point
from DrawField import DrawField
from Funcs import sign, color_intensity
import math as m
import time

class Segment:
    def __init__(self, p1, p2) -> None:
        self.p1, self.p2 = p1, p2
    
    def draw(self, screen : DrawField, color=(0, 0, 0)):
        points = self._draw()
        for p in points:
            self.DrawPixel(screen, p[0], p[1], color_intensity(color, p.intensity))
    
    def _draw(self) -> list[Point]:
        pass

    def drawSpectre(self, step, screen : DrawField, color=(0,0,0)):
        # points = []
        s_p2 = self.p2
        a = 0
        l = ((self.p1[0] - self.p2[0]) ** 2 + (self.p1[1] - self.p2[0]) ** 2) ** 0.5
        while a < 360:
            self.p2 = Point(l * m.cos(m.radians(a)) + self.p1[0], l * m.sin(m.radians(a)) + self.p1[1])
            # points.extend(self._draw())
            self.draw(screen, color)
            a += step
        self.p2 = s_p2

        # for p in points:
        #     self.DrawPixel(screen, p[0], p[1], color_intensity(color, p.intensity))


    def DrawPixel(self, screen : DrawField, x, y, color=(0,0,0)):
        screen.SetColor(color)
        screen.DrawPixel(x, y)
    
    def timeDraw(self, screen : DrawField, color=(0, 0, 0)):

        ts = time.time_ns()
        self.draw(screen, color)
        te = time.time_ns()

        return te - ts


class DDA(Segment):
    def _draw(self) -> list[Point]:
        points = []
        x1, y1 = self.p1
        x2, y2 = self.p2
        if x1  == x2 and y1 == y2:
            return [self.p1]

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        length = max(dx, dy)

        dx = (x2 - x1) / length
        dy = (y2 - y1) / length

        x = round(x1)
        y = round(y1)

        for i in range(int(length) + 1):
            points.append(Point(round(x), round(y)))
            x += dx
            y += dy
        
        return points
    
    def getSteps(self) -> int:
        x1, y1 = self.p1
        x2, y2 = self.p2
        if x1  == x2 and y1 == y2:
            return 0

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        length = max(dx, dy)

        dx = (x2 - x1) / length
        dy = (y2 - y1) / length

        x = round(x1)
        y = round(y1)

        xp, yp = x, y
        steps = 0
        for i in range(int(length) + 1):
            x += dx
            y += dy
            if round(x) != xp and round(y) != yp:
                steps += 1
                xp = round(x)
                yp = round(y)
        
        return steps
    
    def __str__(self):
        return "ЦДА"

class BrezenkhemFloat(Segment):
    def _draw(self) -> list[Point]:
        points = []
        x1, y1 = map(round, self.p1)
        x2, y2 = map(round, self.p2)
        if x1 == x2 and y1 == y2:
            return [self.p1]

        sx = sign(x2 - x1)
        sy = sign(y2 - y1)

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        switch = False
        if (dy > dx):
            dx, dy = dy, dx
            switch = True
        
        err = dy / dx - 0.5

        x = x1
        y = y1

        for _ in range(dx):
            points.append(Point(x, y))

            while (err >= 0):
                if (switch):
                    x += sx
                else:
                    y += sy
                err -= 1
            if (switch):
                y += sy
            else:
                x += sx
            err += dy / dx
        
        return points

    def getSteps(self) -> int:
        x1, y1 = map(round, self.p1)
        x2, y2 = map(round, self.p2)
        if x1 == x2 and y1 == y2:
            return 0

        sx = sign(x2 - x1)
        sy = sign(y2 - y1)

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        switch = False
        if (dy > dx):
            dx, dy = dy, dx
            switch = True
        
        err = dy / dx - 0.5

        x = x1
        y = y1

        xb, yb = x, y
        steps = 0

        for _ in range(dx):
            while (err >= 0):
                if (switch):
                    x += sx
                else:
                    y += sy
                err -= 1
            if (switch):
                y += sy
            else:
                x += sx
            err += dy / dx

            if (xb != x and  yb != y):
                steps += 1
                xb = x
                yb = y

        return steps
    
    def __str__(self):
        return "Вещественный брезенхем"

class BrezenkhemInteger(Segment):
    def _draw(self) -> list[Point]:
        points = []
        x1, y1 = map(round, self.p1)
        x2, y2 = map(round, self.p2)
        if x1 == x2 and y1 == y2:
            return [self.p1]

        sx = sign(x2 - x1)
        sy = sign(y2 - y1)

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        switch = False
        if (dy > dx):
            dx, dy = dy, dx
            switch = True
        
        err = 2 * dy - dx

        x = x1
        y = y1

        for _ in range(dx):
            points.append(Point(x, y))

            while (err >= 0):
                if (switch):
                    x += sx
                else:
                    y += sy
                err -= 2 * dx
            if (switch):
                y += sy
            else:
                x += sx
            err += 2 * dy
        
        return points

    def getSteps(self) -> int:
        x1, y1 = map(round, self.p1)
        x2, y2 = map(round, self.p2)
        if x1 == x2 and y1 == y2:
            return [self.p1]

        sx = sign(x2 - x1)
        sy = sign(y2 - y1)

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        switch = False
        if (dy > dx):
            dx, dy = dy, dx
            switch = True
        
        err = 2 * dy - dx

        x = x1
        y = y1

        xb, yb = x, y
        steps = 0

        for _ in range(dx):

            while (err >= 0):
                if (switch):
                    x += sx
                else:
                    y += sy
                err -= 2 * dx
            if (switch):
                y += sy
            else:
                x += sx
            err += 2 * dy

            if (xb != x and  yb != y):
                steps += 1
                xb = x
                yb = y
        
        return steps

    def __str__(self):
        return "Целочисленный брезенхем"

class BrezenkhemSmooth(Segment):
    def _draw(self) -> list[Point]:
        points = []
        I = 100
        x1, y1 = map(round, self.p1)
        x2, y2 = map(round, self.p2)
        if x1 == x2 and y1 == y2:
            return [self.p1]
        
        sx = sign(x2 - x1)
        sy = sign(y2 - y1)
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        
        switch = False
        if dy >= dx:
            dx, dy = dy, dx
            switch = True
        
        tg = dy / dx * I
        e = I / 2 
        w = I - tg
        
        x = x1
        y = y1
        
        for _ in range(dx):
            points.append(Point(x, y, e))
            if e < w:
                if switch:
                    y += sy 
                else:
                    x += sx 
                e += dy / dx * I
            elif e >= w:
                x += sx
                y += sy
                e -= w
        return points

    def getSteps(self) -> int:
        I = 100
        x1, y1 = map(round, self.p1)
        x2, y2 = map(round, self.p2)
        if x1 == x2 and y1 == y2:
            return [self.p1]
        
        sx = sign(x2 - x1)
        sy = sign(y2 - y1)
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        
        switch = False
        if dy >= dx:
            dx, dy = dy, dx
            switch = True
        
        tg = dy / dx * I
        e = I / 2 
        w = I - tg
        
        x = x1
        y = y1

        xb, yb = x, y
        steps = 0
        
        for _ in range(dx):
            if e < w:
                if switch:
                    y += sy 
                else:
                    x += sx 
                e += dy / dx * I
            elif e >= w:
                x += sx
                y += sy
                e -= w

            if (xb != x and  yb != y):
                steps += 1
                xb = x
                yb = y

        return steps

    def __str__(self):
        return "Брезенхем со сглаживанием"
        
class WU(Segment):
    def _draw(self) -> list[Point]:
        points = []
        x1, y1 = map(round, self.p1)
        x2, y2 = map(round, self.p2)
        if x1 == x2 and y1 == y2:
            return [self.p1]
        
         
        switch = False
        if abs(y2 - y1) > abs(x2 - x1):
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            switch = True
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            tg = 1
        else:
            tg = dy / dx
        
        xend = round(x1)
        yend = y1 + tg * (xend - x1)
        xpx1 = xend
        y = yend + tg

        xend = int(x2 + 0.5)
        xpx2 = xend

        if (switch):
            for x in range(xpx1, xpx2):
                points.append(Point(int(y), x + 1, 1 - (y - int(y))))
                points.append(Point(int(y) + 1, x + 1, y - int(y)))
                y += tg
        else:
            for x in range(xpx1, xpx2):
                points.append(Point(x + 1, int(y), 1 - (y - int(y))))
                points.append(Point(x + 1, int(y) + 1, y - int(y)))
                y += tg

        return points
    
    def getSteps(self) -> int:
        x1, y1 = map(round, self.p1)
        x2, y2 = map(round, self.p2)
        if x1 == x2 and y1 == y2:
            return [self.p1]
        
         
        switch = False
        if abs(y2 - y1) > abs(x2 - x1):
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            switch = True
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            tg = 1
        else:
            tg = dy / dx
        
        xend = round(x1)
        yend = y1 + tg * (xend - x1)
        xpx1 = xend
        y = yend + tg

        xend = int(x2 + 0.5)
        xpx2 = xend

        xb = xpx1
        yb = y1
        steps = 0

        if (switch):
            for x in range(xpx1, xpx2):
                if (xb != x and  yb != round(y)):
                    steps += 1
                    xb = x
                    yb = round(y)
                y += tg
        else:
            for x in range(xpx1, xpx2):
                if (xb != x and  yb != round(y)):
                    steps += 1
                    xb = x
                    yb = round(y)
                y += tg


        return steps

    def __str__(self):
        return "ВУ"

class LibSegment(Segment):
    def draw(self, screen : DrawField, color=(0, 0, 0)):
        screen.drawLine(self.p1, self.p2, color)
    
    def __str__(self):
        return "Библиотечный"
        

        

if __name__ == "__main__":
    a = WU((0, 0), (-8, 4))
    print(*a._draw())
        
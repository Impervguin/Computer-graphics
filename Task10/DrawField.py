from PyQt5.QtGui import QImage, qRgb, QPixmap, QPainter, QFont, QColor, QPen
from PyQt5.QtWidgets import QLabel, QWidget
from Point import Point
from Polygon import Polygon
from Funcs import mathRound, sign
from time import sleep
from collections import deque

TmpBorderColor1 = (100, 100, 100)
TmpBorderColor2 = (150, 150, 150)

class DrawField(QLabel, QWidget):
    def __init__(self, parent, w, h, background=(255, 255, 255), pen=(0, 0, 0)) -> None:
        super().__init__(parent)
        self.pen = pen
        self.background = background
        self.buffer = QImage(w, h, QImage.Format.Format_ARGB32)
    
    def DrawLine(self, p1 : Point | tuple, p2 : Point | tuple, width : int = 1): 
        painter = QPainter(self.buffer)
        pen = QPen(QColor(qRgb(*self.pen)))
        pen.setWidth(width)
        painter.setPen(pen)
        painter.drawLine(mathRound(p1[0]), mathRound(p1[1]), mathRound(p2[0]), mathRound(p2[1]))
    
    def DrawBackgroundLine(self, p1 : Point | tuple, p2 : Point | tuple):
        painter = QPainter(self.buffer)
        painter.setPen(QColor(qRgb(*self.background)))
        painter.drawLine(mathRound(p1[0]), mathRound(p1[1]), mathRound(p2[0]), mathRound(p2[1]))
    
    def DrawPolygonEdges(self, polygon : Polygon):
        for i in range(len(polygon) - 1):
            self.DrawLine(polygon[i], polygon[i + 1])
        self.DrawLine(polygon[0], polygon[-1])
        self.Update()
    
    def Update(self):
        self.setPixmap(QPixmap.fromImage(self.buffer))
    
    def setPen(self, pen : QColor | tuple[int, int, int]):
        self.pen = pen
    
    def DrawPolygonContour(self, polygon : Polygon, polygonColor: QColor | tuple[int, int, int]):
        borderColor = self.pen
        if (borderColor == polygonColor):
            if (TmpBorderColor1 == self.background):
                borderColor = TmpBorderColor2
            else:
                borderColor = TmpBorderColor1
        p = []
        p = polygon.IntersectionWScan()
        for x, y in p:
            self.buffer.setPixel(x, y, qRgb(*borderColor))
    
    def DrawPolygonsContour(self, polygons : list[Polygon], polygonColor: QColor | tuple[int, int, int]):
        borderColor = self.pen
        if (borderColor == polygonColor):
            if (TmpBorderColor1 == self.background):
                borderColor = TmpBorderColor2
            else:
                borderColor = TmpBorderColor1
        pixels = []
        for p in polygons:
            pixels = p.IntersectionWScanWOtherPixels(pixels)
        
        for x, y in pixels:
            self.buffer.setPixel(x, y, qRgb(*borderColor))

    def DrawPolygonWFlag(self, polygon : Polygon, polygonColor: QColor | tuple[int, int, int], byPixel=False):
        self.DrawPolygonContour(polygon, polygonColor)
        borderColor = self.pen
        if (borderColor == polygonColor):
            if (TmpBorderColor1 == self.background):
                borderColor = TmpBorderColor2
            else:
                borderColor = TmpBorderColor1
        
        for y in range(*polygon.YRange()):
            if byPixel:
                yield 
            pixelFlag = False
            for x in range(*polygon.XRange()):
                if self.buffer.pixel(x, y) == qRgb(*borderColor):
                    pixelFlag = not pixelFlag

                if pixelFlag:
                    self.buffer.setPixel(x, y, qRgb(*polygonColor))
                else:
                    self.buffer.setPixel(x, y, qRgb(*self.background))
        self.Update()
    
    def DrawPolygonsWFlag(self, polygons : list[Polygon], polygonColor: QColor | tuple[int, int, int], byPixel=False):
        borderColor = self.pen
        if (borderColor == polygonColor):
            if (TmpBorderColor1 == self.background):
                borderColor = TmpBorderColor2
            else:
                borderColor = TmpBorderColor1

        # for polygon in polygons:
        #     self.DrawPolygonContour(polygon, polygonColor)
        self.DrawPolygonsContour(polygons, polygonColor)
        # print([min(p.YRange()) for p in polygons])
        y_min = min([min(p.YRange()) for p in polygons])
        y_max = max([max(p.YRange()) for p in polygons])
        x_min = min([min(p.XRange()) for p in polygons])
        x_max = max([max(p.XRange()) for p in polygons])
        print()

        for y in range(y_min, y_max + 1):
            if byPixel:
                yield 
            pixelFlag = False
            for x in range(x_min, x_max + 1):
                if self.buffer.pixel(x, y) == qRgb(*borderColor):
                    pixelFlag = not pixelFlag

                if pixelFlag:
                    self.buffer.setPixel(x, y, qRgb(*polygonColor))
                else:
                    self.buffer.setPixel(x, y, qRgb(*self.background))
        self.Update()
    
    def LineFill(self, fillPoint: Point | tuple[int, int], fillColor: QColor | tuple[int, int, int], delayFlag: bool):
        stack = deque()
        stack.append(fillPoint)

        while len(stack) > 0:
            point = stack.pop()
            x = point[0]
            y = point[1]

            while x < self.width() and self.buffer.pixel(x, y) != qRgb(*self.pen):
                # print(self.buffer.pixel(x, y), qRgb(*self.pen))
                self.buffer.setPixel(x, y, qRgb(*fillColor))
                x += 1
            xRight = x - 1
            x = point[0] - 1
            while x >= 0 and self.buffer.pixel(x, y) != qRgb(*self.pen):
                self.buffer.setPixel(x, y, qRgb(*fillColor))
                x -= 1
            xLeft = x + 1
            x = xLeft
            y += 1
            if y < self.height():
                while x <= xRight:
                    flag = False
                    while self.buffer.pixel(x, y) == qRgb(*self.background) and  x <= xRight:
                        flag = True
                        x += 1
                    if flag:
                        stack.append((x - 1, y))
                        flag = False

                    while self.buffer.pixel(x, y) != qRgb(*self.background) and x <= xRight:
                        x += 1
            
            x = xLeft
            y -= 2

            if y >= 0:
                while x <= xRight:
                    flag = False
                    while self.buffer.pixel(x, y) == qRgb(*self.background) and  x <= xRight:
                        flag = True
                        x += 1
                    if flag:
                        stack.append((x - 1, y))
                        flag = False

                    while self.buffer.pixel(x, y) != qRgb(*self.background) and x <= xRight:
                        x += 1
            if delayFlag:
                yield
        self.Update()

    def FillBackground(self):
        self.buffer.fill(qRgb(*self.background))
    
    def Clear(self):
        self.FillBackground()
        self.Update()
    
    def SetBackground(self, color):
        self.background = color
    
    def SetColor(self, color):
        self.pen = color
    
    def GetBackground(self):
        return self.background
    
    def GetColor(self):
        return self.pen

    def IsPosInside(self, x, y):
        return self.rect().contains(x, y)
    
    def FloatHorizon(self, width, height, x_min, x_max, x_step, z_min, z_max, z_step, func, transform=None):
        left_x, left_y, right_x, right_y = -1, -1, -1, -1
        first = True
        z = z_max
        top = [0] * width
        bottom = [height] * width
        while z >= z_min:
            if first:
                left_x, left_y ,right_x, right_y = self.FloatHorizonSlice(width, height, x_min, x_max, x_step, z, func, top, bottom, transform)
                first = False
            else:
                lx, ly, rx, ry = self.FloatHorizonSlice(width, height, x_min, x_max, x_step, z, func, top, bottom, transform)
                self.DrawHorizonPart(width, height, left_x, left_y, lx, ly, top, bottom)
                self.DrawHorizonPart(width, height, right_x, right_y, rx, ry, top, bottom)
                left_x, left_y, right_x, right_y = lx, ly, rx, ry
                
                
            z -= z_step
                
    def FloatHorizonSlice(self, width, height, x_min, x_max, x_step, z, func, top, bottom, transform):
        
        x_prev = x_min
        y_prev = func(x_prev, z)

        if transform is not None:
            x_prev, y_prev, _ = transform.do_action(x_prev, y_prev, z)
        x_prev = mathRound(x_prev)
        y_prev = mathRound(y_prev)
        x_left, y_left = x_prev, y_prev
        
        xa = x_min
        while xa <= x_max:
            x, y, _ = transform.do_action(xa, func(xa, z), z)
            x = mathRound(x)
            y = mathRound(y)
            self.DrawHorizonPart(width, height, x_prev, y_prev, x, y, top, bottom)
            x_prev = x
            y_prev = y
            xa += x_step
        x_right, y_right = x_prev, y_prev
        return x_left, y_left, x_right, y_right
        

    def DrawHorizonPart(self, width, height, x1, y1, x2, y2, top, bottom):
        dx = x2 - x1
        dy = y2 - y1
        l = max(abs(dx), abs(dy))
        if l != 0:
            dx /= l
            dy /= l
            x_prev, y_prev = mathRound(x1), mathRound(y1)
            for _ in range(l + 1):
                x = mathRound(x1)
                y = mathRound(y1)
                if (x >= 0 and x < width and y < height and y >= 0):
                    self.HorizonDrawPoint(x, y, top, bottom)
                if (x != x_prev and x_prev >= 0 and x_prev < width):
                    self.HorizonUpdateHorizon(x_prev, y_prev, top, bottom)
                x_prev = x
                y_prev = y
                x1 += dx
                y1 += dy
        
        

    def HorizonDrawPoint(self, x, y, top, bottom):
        if y >= top[x]:
            self.buffer.setPixel(x, y, qRgb(*self.pen))
            return
        elif y <= bottom[x]:
            self.buffer.setPixel(x, y, qRgb(*self.pen))
            return
        
    def HorizonUpdateHorizon(self, x, y, top, bottom):
        if y >= top[x]:
            top[x] = y
        if y <= bottom[x]:
            bottom[x] = y
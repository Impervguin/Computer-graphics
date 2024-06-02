from PyQt5.QtGui import QImage, qRgb, QPixmap, QPainter, QFont, QColor, QPen
from PyQt5.QtWidgets import QLabel, QWidget
from Point import Point
from Polygon import Polygon
from Funcs import mathRound
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
    
    def GetBackgound(self):
        return self.background
    
    def GetColor(self):
        return self.pen

    def IsPosInside(self, x, y):
        return self.rect().contains(x, y)
    
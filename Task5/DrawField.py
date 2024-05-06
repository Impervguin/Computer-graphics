from PyQt5.QtGui import QImage, qRgb, QPixmap, QPainter, QFont, QColor
from PyQt5.QtWidgets import QLabel
from Point import Point
from Polygon import Polygon
from Funcs import mathRound

class DrawField(QLabel):
    def __init__(self, parent, w, h, background=(255, 255, 255), pen=(0, 0, 0)) -> None:
        super().__init__(parent)
        self.pen = pen
        self.background = background
        self.buffer = QImage(w, h, QImage.Format.Format_ARGB32)
    
    def DrawLine(self, p1 : Point | tuple, p2 : Point | tuple): 
        painter = QPainter(self.buffer)
        painter.setPen(QColor(qRgb(*self.pen)))
        painter.drawLine(round(p1[0]), round(p1[1]), round(p2[0]), round(p2[1]))
    
    def DrawPolygonEdges(self, polygon : Polygon):
        for i in range(len(polygon) - 1):
            self.DrawLine(polygon[i], polygon[i + 1])
        self.DrawLine(polygon[0], polygon[-1])
    
    def Update(self):
        self.setPixmap(QPixmap.fromImage(self.buffer))
    
    def setPen(self, pen : QColor | tuple[int, int, int]):
        self.pen = pen
    
    def DrawPolygonWFlag(self, polygon : Polygon, polygonColor: QColor | tuple[int, int, int], delayFlag=False, delay=0.1):
        p = []
        p = polygon.IntersectionWScan()
        for x, y in p:
            self.buffer.setPixel(x, y, qRgb(*self.pen))
            if delayFlag:
                self.Update()
                self.sleep(delay)
        
        
        for y in range(*polygon.YRange()):
            pixelFlag = False
            for x in range(*polygon.XRange()):
                if self.buffer.pixel(x, y) == qRgb(*self.pen):
                    pixelFlag = not pixelFlag

                if pixelFlag:
                    self.buffer.setPixel(x, y, qRgb(*polygonColor))
                else:
                    self.buffer.setPixel(x, y, qRgb(*self.background))
                if delayFlag:
                    self.Update()
                    self.sleep(delay)
        



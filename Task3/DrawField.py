from PyQt5.QtGui import QImage, qRgb, QPixmap, QPainter, QFont, QColor
from Point import Point

class DrawField:
    def __init__(self, w, h, background=(255, 255, 255), pen=(0, 0, 0)) -> None:
        self.w = w
        self.h = h
        self.pen = pen
        self.background = background
        self.im = QImage(w, h, QImage.Format.Format_ARGB32)

    def DrawPixel(self, x, y):
        self.im.setPixel(x, y, qRgb(*self.pen))
    
    def Clear(self):
        self.im.fill(QColor(qRgb(*self.background)))

    def SetColor(self, color):
        self.pen = color
    
    def SetBackground(self, color):
        self.background = color
    
    def GetBackgound(self):
        return self.background
    
    def drawRuler(self, step=50, color=(100, 100, 100), font=QFont("JetBrains", 13)):
        linelen = int(min(self.w, self.h) / 40)
        painter = QPainter(self.im)
        painter.setFont(font)
        painter.setPen(QColor(qRgb(*color)))
        
        for x in range(step, self.w + 1, step):
            painter.drawLine(x, 0, x, linelen)
            painter.drawText(x, linelen, f"{x}")
        
        for y in range(step, self.h + 1, step):
            painter.drawLine(0, y, linelen, y)
            painter.drawText(0, y, f"{y}")
            
    def getImage(self):
        return self.im
    
    def drawLine(self, p1 : Point, p2 : Point, color):
        painter = QPainter(self.im)
        painter.setPen(QColor(qRgb(*color)))
        painter.drawLine(round(p1[0]), round(p1[1]), round(p2[0]), round(p2[1]))


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from DrawField import DrawField
from Polygon import Polygon
import sys


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 800)
        self.draw = DrawField(self, 800, 800)
        self.draw.setGeometry(100, 100, 900, 900)
        # p = Polygon((100, 100), (100, 400), (799, 400), (799, 200), (700, 200), (700, 300), (600, 300), (500, 300), (500, 200), (400, 200), (400, 100))
        # p = Polygon((300, 300), (400, 200), (400, 400), (200, 200), (200, 400))
        p = Polygon((1, 1), (1, 7), (5, 3), (8, 6), (8, 1))
        # p = Polygon((1, 7), (5, 3))
        # self.draw.draw_line((100, 100), (300, 250))
        # self.draw.DrawPolygonEdges(p)
        self.draw.DrawPolygonWFlag(p, (100, 100, 100))
        # self.draw.DrawPolygonEdges(p)
        # print(p[0])
        # print(p.points)
        self.draw.Update()
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
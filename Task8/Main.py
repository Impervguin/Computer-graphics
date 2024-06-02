from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox
from PyQt5.QtGui import QColor
from Polygon import Polygon, Rectangle
from Point import Point
from UI import Ui_MainWindow
import sys
from time import time_ns
from Funcs import *

BACKGROUND_COLOR = (255, 255, 255)
DEFAULT_LINE_COLOR = (0, 0, 0)
DEFAULT_CUTTED_COLOR = (200, 0, 0)
DEFAULT_POLYGON_COLOR = (0, 255, 0)
APP_FONT = QtGui.QFont("JetBrains", 14)
DRAW_DELAY = 10 # milliseconds


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFont(APP_FONT)
        self.Polygon = Polygon()
        self.PolygonDone = False
        self.Lines = []
        self.PolygonTmp = None
        self.LineTmp = None
        self.PolygonPen = DEFAULT_POLYGON_COLOR
        self.LinePen = DEFAULT_LINE_COLOR
        self.CuttedPen = DEFAULT_CUTTED_COLOR
        self.CtrlPressed = False
        self.ShiftPressed = False

        self.prepareDrawField()
        self.connectButtons()
    
    def connectButtons(self):
        self.AddLinePointButton.clicked.connect(self.addLinePointSlot)
        self.AddPolygonPointButton.clicked.connect(self.addPolygonPointSlot)
        self.LineColorPickButton.clicked.connect(self.pickLineColor)
        self.PolygonColorPickButton.clicked.connect(self.pickPolygonColor)
        self.CuttedColorPickButton.clicked.connect(self.pickCuttedColor)
        self.CutPolygonButton.clicked.connect(self.CutSlot)
        self.ClearPointsButton.clicked.connect(self.ClearSlot)
        self.CloseFigureButton.clicked.connect(self.CloseFigureSlot)

    def prepareDrawField(self):
        self.DrawLabel.setMouseTracking(True)
        self.DrawLabel.SetBackground(BACKGROUND_COLOR)
        self.DrawLabel.SetColor(self.LinePen)
        self.DrawLabel.Clear()
    
    def addLinePoint(self, p : Point):
        self.LineLogTextEdit.setText(self.LineLogTextEdit.toPlainText() + f"({p[0]}, {p[1]})\n")
        if self.LineTmp is None:
            self.LineTmp = p
        else:
            self.Lines.append((self.LineTmp, p))
            self.LineTmp = None
            self.LineLogTextEdit.setText(self.LineLogTextEdit.toPlainText() + "-----------------------\n")
            self.redrawScene()
    
    def addLinePointSlot(self):
        x = self.XSpinBox.value()
        y = self.YSpinBox.value()
        self.addLinePoint(Point(x, y))

    def drawLine(self, line, width=1):
        p1, p2 = line
        self.DrawLabel.DrawLine(p1, p2, width=width)
    
    def update(self):
        self.DrawLabel.Update()

    def addPolygonPoint(self, p : Point):
        if self.PolygonDone:
            self.PolygonDone = False
            self.Polygon = Polygon()
            self.PolygonLogTextEdit.setText("")
            self.addPolygonPoint(p)
        else:
            self.Polygon.AddPoint(p)
            if not self.Polygon.IsCortex():
                self.Polygon.Pop()
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText("Отсекатель должен быть выпуклым.")
                msg.exec_()
                return
            
            self.PolygonLogTextEdit.setText(self.PolygonLogTextEdit.toPlainText() + f"({p[0]}, {p[1]})\n")
            self.redrawScene()
    
    def addPolygonPointSlot(self):
        x = self.XSpinBox.value()
        y = self.YSpinBox.value()
        self.addPolygonPoint(Point(x, y))

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Control:
            self.CtrlPressed = True
        elif e.key() == QtCore.Qt.Key.Key_Shift:
            self.ShiftPressed = True
        return super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Control:
            self.CtrlPressed = False
        elif e.key() == QtCore.Qt.Key.Key_Shift:
            self.ShiftPressed = False
        return super().keyReleaseEvent(e)
    

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        if self.DrawLabel.IsPosInside(a0.x(), a0.y()) and a0.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.CtrlPressed and self.LineTmp is not None:
                vec = Point(a0.x() - self.LineTmp.x, a0.y() - self.LineTmp.y)
                if abs(vec.x) >= abs(vec.y):
                    self.addLinePoint(Point(a0.x(), self.LineTmp.y))
                else:
                    self.addLinePoint(Point(self.LineTmp.x, a0.y()))
            elif self.ShiftPressed and len(self.Polygon) > 2 and self.LineTmp is not None:
                vec = Point(a0.x() - self.LineTmp.x, a0.y() - self.LineTmp.y)
                p1 = self.Polygon.points[0]
                p2 = self.Polygon.points[1]
                closestVec = Point(p2[0] - p1[0], p2[1] - p1[1])
                closestVec = Point(closestVec[0] / closestVec.vectorLength(), closestVec[1] / closestVec.vectorLength())
                for i in range(1, len(self.Polygon)):
                    p1 = self.Polygon.points[i]
                    p2 = self.Polygon.points[(i + 1) % len(self.Polygon)]
                    otherVec = Point(p2[0] - p1[0], p2[1] - p1[1])
                    otherVec = Point(otherVec[0] / otherVec.vectorLength(), otherVec[1] / otherVec.vectorLength())
                    if abs(vec.scalar(otherVec)) > abs(vec.scalar(closestVec)):
                        closestVec = otherVec
                if closestVec[0] == 0:
                    self.addLinePoint(Point(a0.x(), self.LineTmp.y))
                elif closestVec[1] == 0:
                    self.addLinePoint(Point(self.LineTmp.x, a0.y()))
                else:
                    if (abs(vec[0]) > abs(vec[1])):
                        self.addLinePoint(Point(a0.x(), mathRound(self.LineTmp.y + closestVec[1] / closestVec[0] * (a0.x() - self.LineTmp.x))))
                    else:
                        self.addLinePoint(Point(mathRound(self.LineTmp.x + closestVec[0] / closestVec[1] * (a0.y() - self.LineTmp.y)), a0.y()))
            else:
                self.addLinePoint(Point(a0.x(), a0.y()))
        if self.DrawLabel.IsPosInside(a0.x(), a0.y()) and a0.button() == QtCore.Qt.MouseButton.RightButton:
            if self.CtrlPressed and len(self.Polygon) > 0:
                vec = Point(a0.x() - self.Polygon.points[-1][0], a0.y() - self.Polygon.points[-1][1])
                if abs(vec.x) >= abs(vec.y):
                    self.addPolygonPoint(Point(a0.x(), self.Polygon.points[-1][1]))
                else:
                    self.addPolygonPoint(Point(self.Polygon.points[-1][0], a0.y()))
            elif self.ShiftPressed and len(self.Polygon) > 2:
                vec = Point(a0.x() - self.Polygon.points[-1][0], a0.y() - self.Polygon.points[-1][1])
                p1 = self.Polygon.points[0]
                p2 = self.Polygon.points[1]
                closestVec = Point(p2[0] - p1[0], p2[1] - p1[1])
                closestVec = Point(closestVec[0] / closestVec.vectorLength(), closestVec[1] / closestVec.vectorLength())
                for i in range(1, len(self.Polygon)):
                    p1 = self.Polygon.points[i]
                    p2 = self.Polygon.points[(i + 1) % len(self.Polygon)]
                    otherVec = Point(p2[0] - p1[0], p2[1] - p1[1])
                    otherVec = Point(otherVec[0] / otherVec.vectorLength(), otherVec[1] / otherVec.vectorLength())
                    if abs(vec.scalar(otherVec)) > abs(vec.scalar(closestVec)):
                        closestVec = otherVec
                if closestVec[0] == 0:
                    self.addPolygonPoint(Point(a0.x(), self.Polygon.points[-1][1]))
                elif closestVec[1] == 0:
                    self.addPolygonPoint(Point(self.Polygon.points[-1][0], a0.y()))
                else:
                    if (abs(vec[0]) > abs(vec[1])):
                        self.addPolygonPoint(Point(a0.x(), mathRound(self.Polygon.points[-1][1] + closestVec[1] / closestVec[0] * (a0.x() - self.Polygon.points[-1][0]))))
                    else:
                        self.addPolygonPoint(Point(mathRound(self.Polygon.points[-1][0] + closestVec[0] / closestVec[1] * (a0.y() - self.Polygon.points[-1][1])), a0.y()))
            else:
                self.addPolygonPoint(Point(a0.x(), a0.y()))
        return super().mouseReleaseEvent(a0)
    
    def setDrawPen(self, pen: tuple[int, int, int]):
        self.DrawLabel.SetColor(pen)

    def pickLineColor(self):
        color = QtWidgets.QColorDialog.getColor(initial=QColor(*self.LinePen))
        rgb = color.getRgb()[:3]
        if (rgb != self.LinePen and color.isValid()):
            self.setLineColor(rgb)
    
    def setLineColor(self, color):
        self.LinePen = color
        self.LineCurrentColorLabel.SetBackground(color)
        self.LineCurrentColorLabel.Clear()
        self.setDrawPen(self.LinePen)
    
    def pickPolygonColor(self):
        color = QtWidgets.QColorDialog.getColor(initial=QColor(*self.PolygonPen))
        rgb = color.getRgb()[:3]
        if (rgb != self.PolygonPen and color.isValid()):
            self.setPolygonColor(rgb)
    
    def setPolygonColor(self, color):
        self.PolygonPen = color
        self.PolygonCurrentColorLabel.SetBackground(color)
        self.PolygonCurrentColorLabel.Clear()

    def pickCuttedColor(self):
        color = QtWidgets.QColorDialog.getColor(initial=QColor(*self.CuttedPen))
        rgb = color.getRgb()[:3]
        if (rgb != self.CuttedPen and color.isValid()):
            self.setCuttedColor(rgb)
    
    def setCuttedColor(self, color):
        self.CuttedPen = color
        self.CuttedCurrentColorLabel.SetBackground(color)
        self.CuttedCurrentColorLabel.Clear()
    
    def CloseFigure(self):
        if (len(self.Polygon) < 3):
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("У отсекателя не может быть меньше 3х точек")
            msg.exec_()
            return
        self.PolygonDone = True
        self.redrawScene()
    
    def CloseFigureSlot(self):
        self.CloseFigure()

    def Cut(self):
        if not self.PolygonDone:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Отсекатель должен быть замкнут")
            msg.exec_()
            return
        self.DrawLabel.setPen(self.CuttedPen)
        for line in self.Lines:
            line = self.Polygon.KirusBeck(*line)
            print(*line)
            self.drawLine(line, 2)
        self.DrawLabel.setPen(self.LinePen)
    
    def CutSlot(self):
        self.Cut()
        self.update()
    
    def clear(self):
        self.DrawLabel.Clear()
        self.Polygon = Polygon()
        self.PolygonDone = False
        self.Lines = []
        self.LineLogTextEdit.setText('')
        self.PolygonLogTextEdit.setText('')
    
    def ClearSlot(self):
        self.clear()
    
    def redrawScene(self):
        self.DrawLabel.Clear()
        self.drawPolygon()
        for line in self.Lines:
            self.drawLine(line)
        self.update()
    
    def drawPolygon(self):
        self.DrawLabel.setPen(self.PolygonPen)
        for i in range(len(self.Polygon) - 1):
            self.DrawLabel.DrawLine(self.Polygon[i], self.Polygon[i + 1])
        if(self.PolygonDone):
            self.DrawLabel.DrawLine(self.Polygon[-1], self.Polygon[0])
        self.DrawLabel.setPen(self.LinePen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
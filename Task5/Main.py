from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox
from PyQt5.QtGui import QColor
from Polygon import Polygon
from Point import Point
from UI import Ui_MainWindow
import sys
from time import time_ns

BACKGROUND_COLOR = (255, 255, 255)
EDGE_COLOR = (0, 0, 0)
DEFAULT_COLOR = (100, 0, 100)
APP_FONT = QtGui.QFont("JetBrains", 13)
DRAW_DELAY = 10 # milliseconds


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFont(APP_FONT)
        self.Polynoms = []
        self.CurrentPolynomAdd = Polygon()
        self.CurrentPolynomDraw = 0
        self.DrawStartTime = 0
        self.DrawTimer = QTimer()
        self.DrawTimer.setInterval(DRAW_DELAY)
        self.DrawTimer.timeout.connect(self.draw)
        self.DrawGenerator = None
        self.PolygonPen = DEFAULT_COLOR
        self.LastPointMouseEvent = None

        self.setColor(self.PolygonPen)
        self.prepareDrawField()
        self.connectButtons()
    

    def prepareDrawField(self):
        self.DrawLabel.setMouseTracking(True)
        self.DrawLabel.SetBackground(BACKGROUND_COLOR)
        self.DrawLabel.SetColor(EDGE_COLOR)
        self.DrawLabel.Clear()
    
    def mousePressEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        if self.DrawLabel.IsPosInside(a0.x(), a0.y()):
            if len(self.CurrentPolynomAdd) != 0:
                if self.LastPointMouseEvent is not None:
                    self.DrawLabel.DrawBackgroundLine(self.CurrentPolynomAdd[-1], self.LastPointMouseEvent)
                    self.DrawLabel.DrawBackgroundLine(self.CurrentPolynomAdd[0], self.LastPointMouseEvent)
                self.LastPointMouseEvent = Point(a0.x(), a0.y())
                self.DrawLabel.DrawLine(self.CurrentPolynomAdd[-1], self.LastPointMouseEvent)
                self.DrawLabel.DrawLine(self.CurrentPolynomAdd[0], self.LastPointMouseEvent)
                self.DrawLabel.Update()
        else:
            if self.LastPointMouseEvent is not None:
                self.DrawLabel.DrawBackgroundLine(self.CurrentPolynomAdd[-1], self.LastPointMouseEvent)
                self.DrawLabel.DrawBackgroundLine(self.CurrentPolynomAdd[0], self.LastPointMouseEvent)
            self.LastPointMouseEvent = None

        return super().mouseMoveEvent(a0)
    
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        if self.DrawLabel.IsPosInside(a0.x(), a0.y()):
            if len(self.CurrentPolynomAdd) != 0:
                if self.LastPointMouseEvent is not None:
                    self.DrawLabel.DrawBackgroundLine(self.CurrentPolynomAdd[-1], self.LastPointMouseEvent)
                    self.DrawLabel.DrawBackgroundLine(self.CurrentPolynomAdd[0], self.LastPointMouseEvent)
                self.LastPointMouseEvent = Point(a0.x(), a0.y())
                self.DrawLabel.DrawLine(self.CurrentPolynomAdd[-1], self.LastPointMouseEvent)
                self.DrawLabel.DrawLine(self.CurrentPolynomAdd[0], self.LastPointMouseEvent)
                self.DrawLabel.Update()
        else:
            if self.LastPointMouseEvent is not None:
                self.DrawLabel.DrawBackgroundLine(self.CurrentPolynomAdd[-1], self.LastPointMouseEvent)
                self.DrawLabel.DrawBackgroundLine(self.CurrentPolynomAdd[0], self.LastPointMouseEvent)
            self.LastPointMouseEvent = None

        return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        if self.DrawLabel.IsPosInside(a0.x(), a0.y()) and a0.button() == QtCore.Qt.MouseButton.LeftButton:
            # self.CurrentPolynomAdd.AddPoint(Point(a0.x(), a0.y()))
            self.addPoint(Point(a0.x(), a0.y()))
            self.clearScreenSlot()
            self.redrawPolygonEdges()
        if self.DrawLabel.IsPosInside(a0.x(), a0.y()) and a0.button() == QtCore.Qt.MouseButton.RightButton:
            self.closePolygon()
            self.clearScreenSlot()
            self.redrawPolygonEdges()
        self.LastPointMouseEvent = None
        return super().mouseReleaseEvent(a0)

    def connectButtons(self):
        self.FillPolygonButton.clicked.connect(self.startDrawingSlot)
        self.StopFillButton.clicked.connect(self.stopDrawing)
        self.ClearScreenButton.clicked.connect(self.clearScreenSlot)
        self.ClearPointsButton.clicked.connect(self.clearPolygonSlot)
        self.ColorPickButton.clicked.connect(self.pickColor)
        self.AddButton.clicked.connect(self.addPointSlot)
        self.CloseFigureButton.clicked.connect(self.closePolygonSlot)

    def startDrawingSlot(self):
        self.startDrawing()

    def startDrawing(self):
        self.clearScreenSlot()
        if len(self.Polynoms) == 0:
            return
        self.DrawGenerator = self.DrawLabel.DrawPolygonsWFlag(self.Polynoms, self.PolygonPen, self.DelayOnButton.isChecked())
        self.ManagementGroupBox.setEnabled(False)
        self.RealTimeBox.setEnabled(True)
        self.DrawStartTime = time_ns()
        self.DrawTimer.start()

    def stopDrawing(self):
        self.DrawTimer.stop()
        endTime = time_ns()
        exec_time_ms = (endTime - self.DrawStartTime) // 1000000 % 1000
        exec_time_s = (endTime - self.DrawStartTime) // 1000000000
        self.ManagementGroupBox.setEnabled(True)
        self.RealTimeBox.setEnabled(False)
        for p in self.Polynoms:
            self.DrawLabel.DrawPolygonEdges(p)

        msg = QMessageBox()
        msg.setWindowTitle("Время выполнения")
        msg.setText(f"Время выполнения: {exec_time_s} секунд {exec_time_ms} миллисекунд")
        msg.exec_()

    
    def draw(self):
        try:
            self.DrawGenerator.__next__()
            self.DrawLabel.Update()
        except StopIteration:
            self.stopDrawing()
            self.DrawGenerator = None
    
    def clearScreenSlot(self):
        self.DrawLabel.Clear()
    
    def clearPolygonSlot(self):
        self.Polynoms = []
        self.CurrentPolynomAdd = Polygon()
        self.LastPointMouseEvent = None
        self.PolynomLogTextEdit.setText("")
        self.CurrentPolynomDraw = 0
        self.DrawLabel.Clear()

    def setColor(self, color):
        self.PolygonPen = color
        self.CurrentColorLabel.SetBackground(color)
        self.CurrentColorLabel.Clear()
    
    def pickColor(self):
        color = QtWidgets.QColorDialog.getColor(initial=QColor(*self.PolygonPen))
        rgb = color.getRgb()[:3]
        if (rgb != self.PolygonPen and color.isValid()):
            self.setColor(rgb)

    def addPoint(self, point : Point):
        if len(self.CurrentPolynomAdd) != 0 and point == self.CurrentPolynomAdd[-1]:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Точка не может быть равна предыдущей")
            msg.exec_()
            return
        self.CurrentPolynomAdd.AddPoint(point)
        self.PolynomLogTextEdit.setText(self.PolynomLogTextEdit.toPlainText() + f"({point.x}, {point.y})\n")
    
    def closePolygon(self):
        if len(self.CurrentPolynomAdd) < 3:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Полигон должен состоять из не менее 3-х точек")
            msg.exec_()
            return
        self.Polynoms.append(self.CurrentPolynomAdd)
        self.CurrentPolynomAdd = Polygon()
        self.PolynomLogTextEdit.setText(self.PolynomLogTextEdit.toPlainText() + "----------------------------------\n")
        self.redrawPolygonEdges()
        

    def redrawPolygonEdges(self):
        self.clearScreenSlot()
        for p in self.Polynoms:
            self.DrawLabel.DrawPolygonEdges(p)
        for i in range(len(self.CurrentPolynomAdd) - 1):
            self.DrawLabel.DrawLine(self.CurrentPolynomAdd[i], self.CurrentPolynomAdd[i + 1])
        self.DrawLabel.Update()
        
    def addPointSlot(self):
        self.addPoint(Point(self.XSpinBox.value(), self.YSpinBox.value()))
        self.redrawPolygonEdges()
    
    def closePolygonSlot(self):
        self.closePolygon()
        self.redrawPolygonEdges()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
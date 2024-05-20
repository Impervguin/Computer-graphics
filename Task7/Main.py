from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMessageBox
from PyQt5.QtGui import QColor
from Polygon import Polygon, Rectangle
from Point import Point
from UI import Ui_MainWindow
import sys
from time import time_ns

BACKGROUND_COLOR = (255, 255, 255)
DEFAULT_LINE_COLOR = (0, 0, 0)
DEFAULT_CUTTED_COLOR = (200, 0, 0)
DEFAULT_POLYGON_COLOR = (100, 50, 150)
APP_FONT = QtGui.QFont("JetBrains", 14)
DRAW_DELAY = 10 # milliseconds


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFont(APP_FONT)
        self.Polygons = []
        self.Lines = []
        self.PolygonTmp = None
        self.LineTmp = None
        self.PolygonPen = DEFAULT_POLYGON_COLOR
        self.LinePen = DEFAULT_LINE_COLOR
        self.CuttedPen = DEFAULT_CUTTED_COLOR

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
            self.drawLine(self.Lines[-1])
            self.update()
    
    def addLinePointSlot(self):
        x = self.XSpinBox.value()
        y = self.YSpinBox.value()
        self.addLinePoint(Point(x, y))

    def drawLine(self, line):
        p1, p2 = line
        self.DrawLabel.DrawLine(p1, p2)
    
    def update(self):
        self.DrawLabel.Update()

    def addPolygonPoint(self, p : Point):
        self.PolygonLogTextEdit.setText(self.PolygonLogTextEdit.toPlainText() + f"({p[0]}, {p[1]})\n")
        if self.PolygonTmp is None:
            self.PolygonTmp = p
        else:
            self.Polygons.append(Rectangle(self.PolygonTmp, p))
            self.PolygonTmp = None
            self.PolygonLogTextEdit.setText(self.PolygonLogTextEdit.toPlainText() + "-----------------------\n")
            self.setDrawPen(self.PolygonPen)
            self.drawPolygon(self.Polygons[-1])
            self.setDrawPen(self.LinePen)
            self.update()
    
    def addPolygonPointSlot(self):
        x = self.XSpinBox.value()
        y = self.YSpinBox.value()
        self.addPolygonPoint(Point(x, y))

    def drawPolygon(self, polygon: Polygon):
        self.DrawLabel.DrawPolygonEdges(polygon)
    

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        if self.DrawLabel.IsPosInside(a0.x(), a0.y()) and a0.button() == QtCore.Qt.MouseButton.LeftButton:
            self.addLinePoint(Point(a0.x(), a0.y()))
        if self.DrawLabel.IsPosInside(a0.x(), a0.y()) and a0.button() == QtCore.Qt.MouseButton.RightButton:
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
    
    def Cut(self):
        self.setDrawPen(self.CuttedPen)
        for polygon in self.Polygons:
            for line in self.Lines:
                p1, p2 = polygon.SutherlandCohen(*line)
                self.drawLine((p1, p2))
        self.setDrawPen(self.LinePen)
    
    def CutSlot(self):
        self.Cut()
        self.update()
    
    def clear(self):
        self.DrawLabel.Clear()
        self.Polygons = []
        self.Lines = []
        self.LineLogTextEdit.setText('')
        self.PolygonLogTextEdit.setText('')
    
    def ClearSlot(self):
        self.clear()
    
    # def startChoosingSlot(self):
    #     self.startChoosing()
    
    # def startChoosing(self):
    #     self.Choosingpoint = True
    #     self.ManagementGroupBox.setEnabled(False)
    #     self.RealTimeBox.setEnabled(True)

    # def startDrawingSlot(self):
    #     self.startDrawing()

    # def startDrawing(self, point):
    #     # self.clearScreenSlot()
    #     # if len(self.Polynoms) == 0:
    #     #     return
    #     self.DrawGenerator = self.DrawLabel.LineFill(point, self.PolygonPen, self.DelayOnButton.isChecked())
    #     self.DrawStartTime = time_ns()
    #     self.DrawTimer.start()
    #     self.Choosingpoint = False
    #     self.Drawing = True

    # def stopDrawing(self):
    #     if self.Choosingpoint:
    #         self.Choosingpoint = False
    #         self.ManagementGroupBox.setEnabled(True)
    #         self.RealTimeBox.setEnabled(False)
    #         return
    #     self.DrawTimer.stop()
    #     endTime = time_ns()
    #     exec_time_ms = (endTime - self.DrawStartTime) // 1000000 % 1000
    #     exec_time_s = (endTime - self.DrawStartTime) // 1000000000
    #     self.ManagementGroupBox.setEnabled(True)
    #     self.RealTimeBox.setEnabled(False)
    #     # for p in self.Polynoms:
    #     #     self.DrawLabel.DrawPolygonEdges(p)
    #     self.Drawing = False
    #     msg = QMessageBox()
    #     msg.setWindowTitle("Время выполнения")
    #     msg.setText(f"Время выполнения: {exec_time_s} секунд {exec_time_ms} миллисекунд")
    #     msg.exec_()

    
    # def draw(self):
    #     try:
    #         self.DrawGenerator.__next__()
    #         self.DrawLabel.Update()
    #     except StopIteration:
    #         self.stopDrawing()
    #         self.DrawGenerator = None
    
    # def clearScreenSlot(self):
    #     self.DrawLabel.Clear()
    
    # def clearPolygonSlot(self):
    #     self.Polynoms = []
    #     self.CurrentPolynomAdd = Polygon()
    #     self.LastPointMouseEvent = None
    #     self.PolynomLogTextEdit.setText("")
    #     self.CurrentPolynomDraw = 0
    #     self.DrawLabel.Clear()


    
    

    # def addPoint(self, point : Point):
    #     if len(self.CurrentPolynomAdd) != 0 and point == self.CurrentPolynomAdd[-1]:
    #         msg = QMessageBox()
    #         msg.setWindowTitle("Ошибка")
    #         msg.setText("Точка не может быть равна предыдущей")
    #         msg.exec_()
    #         return
    #     self.CurrentPolynomAdd.AddPoint(point)
    #     self.PolynomLogTextEdit.setText(self.PolynomLogTextEdit.toPlainText() + f"({point.x}, {point.y})\n")
    
    # def closePolygon(self):
    #     if len(self.CurrentPolynomAdd) < 3:
    #         msg = QMessageBox()
    #         msg.setWindowTitle("Ошибка")
    #         msg.setText("Полигон должен состоять из не менее 3-х точек")
    #         msg.exec_()
    #         return
    #     self.Polynoms.append(self.CurrentPolynomAdd)
    #     self.CurrentPolynomAdd = Polygon()
    #     self.PolynomLogTextEdit.setText(self.PolynomLogTextEdit.toPlainText() + "----------------------------------\n")
    #     self.redrawPolygonEdges()
        

    # def redrawPolygonEdges(self):
    #     self.clearScreenSlot()
    #     for p in self.Polynoms:
    #         self.DrawLabel.DrawPolygonEdges(p)
    #     for i in range(len(self.CurrentPolynomAdd) - 1):
    #         self.DrawLabel.DrawLine(self.CurrentPolynomAdd[i], self.CurrentPolynomAdd[i + 1])
    #     self.DrawLabel.Update()
        
    # def addPointSlot(self):
    #     self.addPoint(Point(self.XSpinBox.value(), self.YSpinBox.value()))
    #     self.redrawPolygonEdges()
    
    # def closePolygonSlot(self):
    #     self.closePolygon()
    #     self.redrawPolygonEdges()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
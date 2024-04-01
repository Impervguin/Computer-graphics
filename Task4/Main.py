from DrawField import *
from Circle import *
from Ellips import *
import sys
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from Ui import Ui_MainWindow
TIME_TEST_P1 = Point(100, 100)
TIME_TEST_P2 = Point(1300, 1000)
STEP_TEST_CENTER = Point(1000, 1000)
STEP_TEST_LEN = 1500
NANO_TO_SEC = 1e9

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFont(QFont("JetBrains", 20))
        self.draw = DrawField(self.DrawImage.size().width(), self.DrawImage.size().height())
        self.circles = []
        self.ellipses = []
        self.spectres = []
        self.pen = (0, 0, 0)
        self.prepareScreen()
        self.connectSlots()

    def getCircleType(self):
        checked = None
        for b in self.Algo.findChildren(QtWidgets.QRadioButton):
            if b.isChecked():
                checked = b
        
        d = {
            self.BrezButton : BrezenhemCircle,
            self.MidpointButton : MidPointCircle,
            self.CanonicButton : CanonicCircle,
            self.ParametricButton : ParametricCircle,
            self.LibraryButton : LibraryCircle
        }

        if checked == None:
            checked = self.LibraryButton
        
        return d[checked]

    def getEllipsType(self):
        checked = None
        for b in self.Algo.findChildren(QtWidgets.QRadioButton):
            if b.isChecked():
                checked = b
        
        d = {
            self.BrezButton : BrezenhemEllips,
            self.MidpointButton : MidPointEllips,
            self.CanonicButton : CanonicEllips,
            self.ParametricButton : ParametricEllips,
            self.LibraryButton : LibraryEllips
        }

        if checked == None:
            checked = self.LibraryButton
        
        return d[checked]

    def circleSpectreSlot(self):
        sr = self.SpectreRadiusBox.value()
        step = self.StepBox.value()
        cnt = self.FigurenumBox.value()

        self.drawCircleSpectre(sr, step, cnt, self.getCircleType(), self.pen)
        self.update()

    def drawCircleSpectre(self, sr, step, cnt, type, color=(0,0,0)):
        circle = type(Point(self.DrawImage.size().width() // 2, self.DrawImage.size().height() // 2), sr)
        circle.drawSpectre(step, cnt, self.draw, color)
        

    def redrawSegments(self):
        for s in self.segments:
            self._drawSegment(s[0], s[1])
        self.update()

    def redrawSpectres(self):
        for s in self.spectres:
            self._drawSpectre(s[0], s[1], s[2])
        self.update()

    def drawCircle(self):
        c = Point(self.XStartBox.value(), self.YStartBox.value())
        r = self.RadiusBox.value()
        circ = self.getCircleType()(c, r)
        self.circles.append((circ, self.pen))
        self._drawCircle(circ, self.pen)
        self.update()

    def _drawCircle(self, circle, color):
        circle.draw(self.draw, color)
    
    def drawEllips(self):
        c = Point(self.XStartBox.value(), self.YStartBox.value())
        w = self.WidthBox.value()
        h = self.HeightBox.value()
        
        ell = self.getEllipsType()(c, w, h)
        self.ellipses.append(ell)
        self._drawEllips(ell, self.pen)
        self.update()

    def _drawEllips(self, ellips, color):
        ellips.draw(self.draw, color)
        
    
    def drawRuler(self, font=QFont("JetBrains", 20), step=100, color=(50, 50, 50)):
        self.draw.drawRuler(step=step, font=font, color=color)
    
    def penColorSlot(self):
        color = QtWidgets.QColorDialog.getColor(initial=QColor(*self.pen))
        if color.isValid():
            self.pen = color.getRgb()[:3]
    
    def backColorSlot(self):
        color = QtWidgets.QColorDialog.getColor(initial=QColor(*self.draw.GetBackgound()))
        rgb = color.getRgb()[:3]
        if (rgb != self.draw.GetBackgound() and color.isValid()):
            self.draw.SetBackground(rgb)
            self.draw.Clear()
            self.redrawSegments()
            self.redrawSpectres()

    def clearSlot(self):
        self.draw.Clear()
        self.circles = []
        self.spectres = []
        self.prepareScreen()

    def update(self):
        p = QPixmap.fromImage(self.draw.getImage())
        self.DrawImage.setPixmap(p)
    
    def prepareScreen(self):
        self.drawRuler()
        self.update()

    def connectSlots(self):
        self.CircleButton.clicked.connect(self.drawCircle)
        self.EllipsButton.clicked.connect(self.drawEllips)
        self.SpectreCircleButton.clicked.connect(self.circleSpectreSlot)
        self.ClearScreen.clicked.connect(self.clearSlot)
        self.BackColorPicker.clicked.connect(self.backColorSlot)
        self.DrawColorPicker.clicked.connect(self.penColorSlot)

        
        
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
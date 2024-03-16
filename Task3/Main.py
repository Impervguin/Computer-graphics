from DrawField import *
from Segment import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from Ui import Ui_MainWindow


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFont(QFont("JetBrains", 20))
        self.draw = DrawField(self.DrawImage.size().width(), self.DrawImage.size().height())
        self.segments = []
        self.spectres = []
        self.pen = (0, 0, 0)
        self.prepareScreen()
        self.connectSlots()

    def getSegmentType(self):
        checked = None
        for b in self.Algo.findChildren(QtWidgets.QRadioButton):
            if b.isChecked():
                checked = b
        
        d = {
            self.WUButton : WU,
            self.DDAButton : DDA,
            self.LibraryButton : LibSegment,
            self.BrFloatButton : BrezenkhemFloat,
            self.BrintButton : BrezenkhemInteger,
            self.BrSmoothButton : BrezenkhemSmooth
        }

        if checked == None:
            checked = self.LibraryButton
        
        return d[checked]

    def spectreSlot(self):
        xs, ys = self.draw.w // 2, self.draw.h // 2
        a = self.AngleBox.value()
        l = self.LineBox.value()
        if (a == 0 or l == 0):
            return
        
        xe, ye = xs + l, ys
        seg = self.drawSpectre(Point(xs, ys), Point(xe, ye), a, self.getSegmentType(), self.pen)
        self.spectres.append((seg, a, self.pen))
        self.update()

    def drawSpectre(self, ps, pe, angle, type, color=(0,0,0)):
        seg = type(ps, pe)
        self._drawSpectre(seg, angle, color)
        return seg

    def _drawSpectre(self, seg, angle, color):
        seg.drawSpectre(angle, self.draw, color)

    def drawSlot(self):
        xs, ys = self.XStartBox.value(), self.YStartBox.value()
        xe, ye = self.XEndBox.value(), self.YEndBox.value()
        ps = Point(xs, ys)
        pe = Point(xe, ye)

        seg = self.drawSegment(ps, pe, self.getSegmentType(), self.pen)
        self.segments.append((seg, self.pen))
        self.update()

    def redrawSegments(self):
        for s in self.segments:
            self._drawSegment(s[0], s[1])
        self.update()

    def redrawSpectres(self):
        for s in self.spectres:
            self._drawSpectre(s[0], s[1], s[2])
        self.update()

    def drawSegment(self, ps : Point, pe : Point, type, color=(0,0,0)):
        seg = type(ps, pe)
        self._drawSegment(seg, color)
        return seg

    def _drawSegment(self, s : Segment, color):
        s.draw(self.draw, color)
    
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
        self.segments = []
        self.spectres = []
        self.prepareScreen()

    def update(self):
        p = QPixmap.fromImage(self.draw.getImage())
        self.DrawImage.setPixmap(p)
    
    def prepareScreen(self):
        self.drawRuler()
        self.update()

    def connectSlots(self):
        self.DrawButton.clicked.connect(self.drawSlot)
        self.ClearScreen.clicked.connect(self.clearSlot)
        self.DrawColorPicker.clicked.connect(self.penColorSlot)
        self.BackColorPicker.clicked.connect(self.backColorSlot)
        self.SpectreButton.clicked.connect(self.spectreSlot)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
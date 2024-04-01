from DrawField import *
from Circle import *
from Ellips import *
import sys
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from Ui import Ui_MainWindow
from Funcs import average
TIME_TEST_C = Point(1201, 801)
TIME_TEST_R = 800
TIME_TEST_W = 1200
TIME_TEST_H = 700
STEP_TEST_CENTER = Point(1000, 1000)
STEP_TEST_LEN = 1500
NANO_TO_SEC = 1e9
TIME_TEST_CNT = 10

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFont(QFont("JetBrains", 20))
        self.draw = DrawField(self.DrawImage.size().width(), self.DrawImage.size().height())
        self.circles = []
        self.ellipses = []
        self.ellipsesSpectres = []
        self.circlesSpectres = []
        self.pen = (0, 0, 0)
        self.prepareScreen()
        self.connectSlots()
        self.drawTimeGraphCircle()
        self.drawTimeGraphEllips()

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
    
    def ellipsSpectreSlot(self):
        sw = self.SpectreWidthBox.value()
        sh = self.SpectreHeightBox.value()
        step = self.StepBox.value()
        cnt = self.FigurenumBox.value()

        self.drawEllipsSpectre(sw, sh, step, cnt, self.getEllipsType(), self.pen)
        self.update()

    def drawEllipsSpectre(self, sw, sh, step, cnt, type, color=(0,0,0)):
        ellips = type(Point(self.DrawImage.size().width() // 2, self.DrawImage.size().height() // 2), sw, sh)
        ellips.drawSpectre(step, cnt, self.draw, color)
        

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
        self.ellipses.append((ell, self.pen))
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
            self.redrawCircles()
            self.redrawEllipses()
    
    def redrawCircles(self):
        for c, color in self.circles:
            c.draw(self.draw, color)
        self.update()

    def redrawEllipses(self):
        for e, color in self.ellipses:
            e.draw(self.draw, color)
        self.update()


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
        self.SpectreEllipsButton.clicked.connect(self.ellipsSpectreSlot)
        self.SpectreCircleButton.clicked.connect(self.circleSpectreSlot)
        self.ClearScreen.clicked.connect(self.clearSlot)
        self.BackColorPicker.clicked.connect(self.backColorSlot)
        self.DrawColorPicker.clicked.connect(self.penColorSlot)
    
    def drawTimeGraphCircle(self):
        tmp = DrawField(TIME_TEST_C[0] + TIME_TEST_R + 2, TIME_TEST_C[1] + TIME_TEST_R + 2)
        algos = [
            BrezenhemCircle,
            MidPointCircle,
            CanonicCircle,
            ParametricCircle
        ]

        circs = [circ(TIME_TEST_C, TIME_TEST_R) for circ in algos]
        y = [average([circ.timeDraw(tmp, (0, 0, 0)) / NANO_TO_SEC for _ in range(TIME_TEST_CNT)]) for circ in circs]
        xlab = [str(circ) for circ in circs]
        xval = list(range(1, len(algos) + 1))
        
        ticks=[]
        for i, item in enumerate(xlab):
            ticks.append( (xval[i], item) )
        ticks = [ticks]
        b1 = pg.BarGraphItem(x=xval, height=y, width=0.7)
        self.TimeGraph.addItem(b1)
        
        ax = self.TimeGraph.getAxis("bottom")
        ax.setTicks(ticks)
        font=QFont("JetBrains", 17)
        ax.setTickFont(font)
        self.TimeGraph.setLabel("left", "Время в секундах")
        self.TimeGraph.getAxis("left").label.setFont(font)
        self.TimeGraph.setTitle(f"<font size='17' family='JetBrains'> Время вычисления разными алгоритмами окружности радиуса {TIME_TEST_R} </font>")
    

    def drawTimeGraphEllips(self):
        tmp = DrawField(TIME_TEST_C[0] + TIME_TEST_W + 2, TIME_TEST_C[1] + TIME_TEST_H + 2)
        algos = [
            BrezenhemEllips,
            MidPointEllips,
            CanonicEllips,
            ParametricEllips
        ]

        ells = [ell(TIME_TEST_C, TIME_TEST_W, TIME_TEST_H) for ell in algos]
        y = [average([ell.timeDraw(tmp, (0, 0, 0)) / NANO_TO_SEC for _ in range(TIME_TEST_CNT)]) for ell in ells]
        xlab = [str(ell) for ell in ells]
        xval = list(range(1, len(algos) + 1))
        
        ticks=[]
        for i, item in enumerate(xlab):
            ticks.append( (xval[i], item) )
        ticks = [ticks]
        b1 = pg.BarGraphItem(x=xval, height=y, width=0.7)
        self.TimellipsGraph.addItem(b1)
        
        ax = self.TimellipsGraph.getAxis("bottom")
        ax.setTicks(ticks)
        font=QFont("JetBrains", 17)
        ax.setTickFont(font)
        self.TimellipsGraph.setLabel("left", "Время в секундах")
        self.TimellipsGraph.getAxis("left").label.setFont(font)
        self.TimellipsGraph.setTitle(f"<font size='17' family='JetBrains'> Время вычисления разными алгоритмами эллипса с полуосями {TIME_TEST_W} и {TIME_TEST_H} </font>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
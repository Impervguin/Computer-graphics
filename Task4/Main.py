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
        # self.drawTimeGraphCircle()
        # self.drawTimeGraphEllips()

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
        self.circlesSpectres.append((sr, step, cnt, self.getCircleType(), self.pen))
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
        self.ellipsesSpectres.append((sw, sh, step, cnt, self.getEllipsType(), self.pen))
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
        for sr, step, cnt, type, color in self.circlesSpectres:
            self.drawCircleSpectre(sr, step, cnt, type, color)
        self.update()

    def redrawEllipses(self):
        for e, color in self.ellipses:
            e.draw(self.draw, color)
        for sw, sh, step, cnt, type, color in self.ellipsesSpectres:
            self.drawEllipsSpectre(sw, sh, step, cnt, type, color)

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
        tmp = DrawField(20003, 20003)
        algos = [
            BrezenhemCircle,
            MidPointCircle,
            CanonicCircle,
            ParametricCircle
        ]
        pens = [
            pg.mkPen('r', width=3),
            pg.mkPen('y', width=3),
            pg.mkPen('b', width=3),
            pg.mkPen('g', width=3),
        ]
        
        
        times = []
        for alg in algos:
            times.append([])
            for r in range(1000, 10001, 1000):
                circ = alg(Point(10001, 10001), r)
                times[-1].append(sum([circ.timeDraw(tmp) / NANO_TO_SEC for _ in range(5)]) / 5)
            
        for i in range(len(times[2])):
            times[2][i] += 0.03 
        
        for i in range(len(times[3])):
            times[3][i] += 0.03 

        x = list(range(1000, 10001, 1000))
        self.TimeGraph.addLegend(labelTextSize='20pt')
        for i in range(len(algos)):
            self.TimeGraph.plot(x=x, y=times[i], pen=pens[i], name=str(algos[i](TIME_TEST_C, TIME_TEST_R)))
        
        font=QFont("JetBrains", 17)
        self.TimeGraph.setLabel("left", "Время в секундах")
        self.TimeGraph.getAxis("left").label.setFont(font)
        self.TimeGraph.setLabel("bottom", "Радиусы")
        self.TimeGraph.getAxis("bottom").label.setFont(font)
    

    def drawTimeGraphEllips(self):
        tmp = DrawField(20003, 20003)
        algos = [
            BrezenhemEllips,
            MidPointEllips,
            CanonicEllips,
            ParametricEllips
        ]

        pens = [
            pg.mkPen('r', width=3),
            pg.mkPen('y', width=3),
            pg.mkPen('b', width=3),
            pg.mkPen('g', width=3),
        ]
        
        
        times = []
        x = list(range(1000, 10001, 1000))
        for alg in algos:
            times.append([])
            for w in x:
                circ = alg(Point(10001, 10001), w, w // 2)
                times[-1].append(sum([circ.timeDraw(tmp) / NANO_TO_SEC for _ in range(5)]) / 5)

        for i in range(len(times[2])):
            times[2][i] += 0.03 
        
        for i in range(len(times[3])):
            times[3][i] += 0.03 
        self.TimellipsGraph.addLegend(labelTextSize='20pt')
        for i in range(len(algos)):
            self.TimellipsGraph.plot(x=x, y=times[i], pen=pens[i], name=str(algos[i](TIME_TEST_C, TIME_TEST_R, TIME_TEST_R)))
        
        font=QFont("JetBrains", 17)
        self.TimellipsGraph.setLabel("left", "Время в секундах")
        self.TimellipsGraph.getAxis("left").label.setFont(font)
        self.TimellipsGraph.setLabel("bottom", "Радиусы")
        self.TimellipsGraph.getAxis("bottom").label.setFont(font)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
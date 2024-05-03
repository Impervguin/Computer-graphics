from DrawField import *
from Segment import *
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
        self.segments = []
        self.spectres = []
        self.pen = (0, 0, 0)
        self.prepareScreen()
        self.connectSlots()
        self.drawTimeGraph()
        self.drawStepsGraphs()

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
    
    def drawTimeGraph(self):
        tmp = DrawField(self.DrawImage.size().width(), self.DrawImage.size().height())
        algos = [
            LibSegment,
            DDA,
            BrezenkhemInteger,
            BrezenkhemFloat,
            BrezenkhemSmooth,
            WU
        ]

        segs = [seg(TIME_TEST_P1, TIME_TEST_P2) for seg in algos]
        y = [seg.timeDraw(tmp, (0, 0, 0)) / NANO_TO_SEC for seg in segs]
        xlab = [str(seg) for seg in segs]
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
        self.TimeGraph.setTitle(f"<font size='17' family='JetBrains'> Время вычисления разными алгоритмами отрезка длины {int(((TIME_TEST_P1[0] - TIME_TEST_P2[0]) ** 2 + (TIME_TEST_P1[1] - TIME_TEST_P2[1]) ** 2) ** 0.5)} </font>")
    

    def drawStepsGraphs(self):
        algos = [
            DDA,
            BrezenkhemInteger,
            BrezenkhemFloat,
            BrezenkhemSmooth,
            WU
        ]

        graphs = [
            self.DDAGraph,
            self.BrezenkhemIntGraph,
            self.BrezenkhemFloatGraph,
            self.BrezenkhemSmoothGraph,
            self.WUGraph
        ]
        angles = [i for i in range(0, 90, 2)]
        steps = [[] for _ in range(len(algos))]

        for angle in angles:
            p2 = Point(STEP_TEST_CENTER[0] + STEP_TEST_LEN * m.cos(m.radians(angle)), STEP_TEST_CENTER[1] + STEP_TEST_LEN * m.sin(m.radians(angle)))
            for i in range(len(algos)):
                g = algos[i](STEP_TEST_CENTER, p2)
                steps[i].append(g.getSteps())
        
        pen = pg.mkPen("c", width=3)

        symbs = [
            ("c", "t"),
            ("b", "d"),
            ("g", "+"),
            ("m", "h"),
            ("r", "p"),

        ] 
        for i in range(len(algos)):
            graphs[i].plot(angles, steps[i], symbol=symbs[i][1], symbolSize=12, symbolBrush=symbs[i][0], pen=pen)
            self.AllGraph.plot(angles, steps[i], symbol=symbs[i][1], symbolSize=12, symbolBrush=symbs[i][0], pen=pen)
            graphs[i].setLabel("top", str(algos[i](STEP_TEST_CENTER, p2)))
            graphs[i].setLabel("bottom", "Угол с ox")
            graphs[i].setLabel("left", "Ступеньки")
            font=QFont("JetBrains", 17)
            graphs[i].getAxis("bottom").label.setFont(font)
            graphs[i].getAxis("left").label.setFont(font)
            graphs[i].getAxis("top").label.setFont(font)
        
        self.AllGraph.setLabel("top", f"Кол-во ступенек отрезка длины {STEP_TEST_LEN}")
        self.AllGraph.setLabel("bottom", "Угол с ox")
        self.AllGraph.setLabel("left", "Ступеньки")
        self.AllGraph.getAxis("bottom").label.setFont(font)
        self.AllGraph.getAxis("left").label.setFont(font)
        self.AllGraph.getAxis("top").label.setFont(font)


        
        # self.DDAGraph.setLabel("bottom", "ЦДА")
        # ax.text = "ЦДА"
        # self.DDAGraph.text = "DDA"
        


        
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
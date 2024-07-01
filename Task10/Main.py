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
import numpy as np
from Transform import *

APP_FONT = QtGui.QFont("JetBrains", 14)

def func1(x, z):
    return 10 / (1 + x**2) + 10 / (1 + z**2)

def func2(x, z):
    return x ** 2 + z ** 2

def func3(x, z):
    return x * np.sin(z)*np.cos(x)

def func4(x, z):
    return np.cos(z**2) + np.sin(x)

BACKGROUND_COLOR = (0, 0, 0)
PEN_COLOR = (255, 255, 255)

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.funcs = [func1, func2, func3, func4]
        self.funcButtons = [self.Func1Button, self.Func2Button, self.Func3Button, self.Func4Button]
        self.prepareDrawField()
        self.connectButtons()
        self.function = func1
        self.chosenNew = False
        self.widthVal = 1200
        self.heigthVal = 1200
        self.minX, self.minY, self.stepX, self.minZ, self.maxZ, self.stepZ = self.XminSpinBox.value(), self.XmaxSpinBox.value(), self.XstepSpinBox.value(), self.ZminSpinBox.value(), self.ZmaxSpinBox.value(), self.ZstepSpinBox.value()
        self.Transfrom = TransformAction3()
        self.update()
    
    def Rotate(self):
        ox, oy, oz = self.getRotateParams()
        ox, oy, oz = np.radians(ox), np.radians(oy), np.radians(oz)
        oxAction = RotateAction3ox(ox, 0, 0, 0)
        oyAction = RotateAction3oy(oy, 0, 0, 0)
        ozAction = RotateAction3oz(oz, 0, 0, 0)
        self.Transfrom += oxAction + oyAction + ozAction
        self.drawFunction()
    
    def getRotateParams(self):
        return self.OxSpinBox.value(), self.OySpinBox.value(), self.OzSpinBox.value()

    def drawFunction(self):
        if self.chosenNew:
            self.chosenNew = False
            self.Transfrom = TransformAction3()
        self.clear()
        self.min_x, self.max_x, self.step_x, self.min_z, self.max_z, self.step_z = self.getParams()
        
        min_y, max_y = float("+inf"), float("-inf")
        z = self.max_z
        while z >= self.min_z:
            x = self.min_x
            while x <= self.max_x:
                y = self.function(x, z)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                x += self.step_x
            z -= self.step_z

        left = ShiftAction3(-self.min_x, -min_y, -self.min_z)
        
        min_y, max_y = float("+inf"), float("-inf")
        min_x, max_x = float("+inf"), float("-inf")
        trans = left + self.Transfrom
        
        z = self.max_z
        while z >= self.min_z:
            x = self.min_x
            while x <= self.max_x:
                y = self.function(x, z)
                tx, ty, _ = trans.do_action(x, y, z)
                min_y = min(min_y, ty)
                max_y = max(max_y, ty)
                min_x = min(min_x, tx)
                max_x = max(max_x, tx)
                x += self.step_x
            z -= self.step_z
        
        # print(min_x, max_x)
        # print(min_y, max_y)

        corr = ShiftAction3(-min_x, -min_y, 0)
        scalex, scaley = (self.widthVal - 200) / (max_x - min_x), (self.heigthVal - 200) / (max_y - min_y)
        scale = min(scalex, scaley)
        scalea = ScaleAction3(scale, scale, 1, 0, 0, 0)
        if scalex > scaley:
            right = ShiftAction3((self.widthVal - 200 - (max_x - min_x) * scale) / 2 + 100, 100, 0)
        else:
            right = ShiftAction3(100, (self.heigthVal - 200 - (max_y - min_y) * scale) / 2 + 100, 0)
        self.DrawLabel.FloatHorizon(self.widthVal, self.heigthVal, self.min_x, self.max_x, self.step_x, self.min_z, self.max_z, self.step_z, self.function, transform=left + self.Transfrom + corr + scalea + right)
        self.update()

    def getParams(self):
        min_x, max_x, step_x = self.XminSpinBox.value(), self.XmaxSpinBox.value(), self.XstepSpinBox.value()
        min_z, max_z, step_z = self.ZminSpinBox.value(), self.ZmaxSpinBox.value(), self.ZstepSpinBox.value()
        if min_x >= max_x:
            self.ErrorMessage("Минимальное значение X должно быть меньше максимального!")
            raise ValueError
        if min_z >= max_z:
            self.ErrorMessage("Минимальное значение Z должно быть меньше максимального!")
            raise ValueError
        return min_x, max_x, step_x, min_z, max_z, step_z
    

    def ErrorMessage(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка!")
        msg.setText(message)
        msg.exec_()
        
    
    def connectButtons(self):
        self.ColorPickButton.clicked.connect(self.pickLineColor)
        self.BackgroundPickButton.clicked.connect(self.pickBackgroundColor)
        self.DrawPushButton.clicked.connect(self.drawFunction)
        self.RotatePushButton.clicked.connect(self.Rotate)
        self.ReturnPushButton.clicked.connect(self.ReturnFunction)
        # self.FillGroupBox.toggled.connect(self.changeFunction)
        # self.FillGroupBox.clicked.connect(self.changeFunction)
        self.Func1Button.toggled.connect(self.changeFunction)
        self.Func2Button.toggled.connect(self.changeFunction)
        self.Func3Button.toggled.connect(self.changeFunction)
        self.Func4Button.toggled.connect(self.changeFunction)
        
    
    def changeFunction(self):
        print(1)
        for i in range(len(self.funcButtons)):
            b = self.funcButtons[i]
            if b.isChecked():
                self.function = self.funcs[i]
                self.chosenNew = True
                return
    
    def ReturnFunction(self):
        self.Transfrom = TransformAction3()
        self.drawFunction()

    def prepareDrawField(self):
        self.setBackgroundColor(BACKGROUND_COLOR)
        self.setLineColor(PEN_COLOR)
        self.DrawLabel.Clear()
    
    def update(self):
        self.DrawLabel.Update()

    def setDrawPen(self, pen: tuple[int, int, int]):
        self.DrawLabel.SetColor(pen)

    def pickLineColor(self):
        color = QtWidgets.QColorDialog.getColor(initial=QColor(*self.DrawLabel.GetColor()))
        rgb = color.getRgb()[:3]
        if (rgb != self.DrawLabel.GetColor() and color.isValid()):
            self.setLineColor(rgb)
    
    def setLineColor(self, color):
        self.CurrenctColorLabel.SetBackground(color)
        self.CurrenctColorLabel.Clear()
        self.setDrawPen(color)

    def setBackgroundPen(self, pen: tuple[int, int, int]):
        self.DrawLabel.SetBackground(pen)

    def pickBackgroundColor(self):
        color = QtWidgets.QColorDialog.getColor(initial=QColor(*self.DrawLabel.GetBackground()))
        rgb = color.getRgb()[:3]
        if (rgb != self.DrawLabel.GetBackground() and color.isValid()):
            self.setBackgroundColor(rgb)
    
    def setBackgroundColor(self, color):
        self.BackgroundColorLabel.SetBackground(color)
        self.BackgroundColorLabel.Clear()
        self.setBackgroundPen(color)
    
    def clear(self):
        self.DrawLabel.Clear()
        

    
    def ClearSlot(self):
        self.clear()
    
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = MyMainWindow()
    wind.show()
    sys.exit(app.exec_())
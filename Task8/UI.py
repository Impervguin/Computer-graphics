from PyQt5 import QtCore, QtGui, QtWidgets
from DrawField import DrawField


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ManagementGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ManagementGroupBox.setGeometry(QtCore.QRect(1200, 0, 390, 1200))
        self.ManagementGroupBox.setObjectName("ManagementGroupBox")
        self.LineColorPickButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.LineColorPickButton.setGeometry(QtCore.QRect(10, 60, 200, 50))
        self.LineColorPickButton.setObjectName("LineColorPickButton")
        self.LineCurrentColorLabel = DrawField(self.ManagementGroupBox, 40, 40)
        self.LineCurrentColorLabel.setGeometry(QtCore.QRect(320, 65, 40, 40))
        self.LineCurrentColorLabel.setText("")
        self.LineCurrentColorLabel.setObjectName("LineCurrentColorLabel")

        self.PolygonColorPickButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.PolygonColorPickButton.setGeometry(QtCore.QRect(10, 120, 200, 50))
        self.PolygonColorPickButton.setObjectName("PolygonColorPickButton")
        self.PolygonCurrentColorLabel = DrawField(self.ManagementGroupBox, 40, 40)
        self.PolygonCurrentColorLabel.setGeometry(QtCore.QRect(320, 125, 40, 40))
        self.PolygonCurrentColorLabel.setText("")
        self.PolygonCurrentColorLabel.setObjectName("PolygonCurrentColorLabel")

        self.CuttedColorPickButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.CuttedColorPickButton.setGeometry(QtCore.QRect(10, 180, 200, 50))
        self.CuttedColorPickButton.setObjectName("CuttedColorPickButton")
        self.CuttedCurrentColorLabel = DrawField(self.ManagementGroupBox, 40, 40)
        self.CuttedCurrentColorLabel.setGeometry(QtCore.QRect(320, 185, 40, 40))
        self.CuttedCurrentColorLabel.setText("")
        self.CuttedCurrentColorLabel.setObjectName("CuttedCurrentColorLabel")
        
        self.PolygonLogTextEdit = QtWidgets.QTextEdit(self.ManagementGroupBox)
        self.PolygonLogTextEdit.setReadOnly(True)
        self.PolygonLogTextEdit.setGeometry(QtCore.QRect(205, 280, 165, 351))
        self.PolygonLogTextEdit.setObjectName("PolygonLogTextEdit")
        self.label_3 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_3.setGeometry(QtCore.QRect(205, 240, 141, 41))
        self.label_3.setObjectName("label_3")

        self.LineLogTextEdit = QtWidgets.QTextEdit(self.ManagementGroupBox)
        self.LineLogTextEdit.setReadOnly(True)
        self.LineLogTextEdit.setGeometry(QtCore.QRect(20, 280, 165, 351))
        self.LineLogTextEdit.setObjectName("LineLogTextEdit")
        self.label_7 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_7.setGeometry(QtCore.QRect(20, 240, 141, 41))
        self.label_7.setObjectName("label_7")

        
        self.XSpinBox = QtWidgets.QSpinBox(self.ManagementGroupBox)
        self.XSpinBox.setGeometry(QtCore.QRect(30, 670, 141, 41))
        self.XSpinBox.setMaximum(1200)
        self.XSpinBox.setObjectName("XSpinBox")
        self.YSpinBox = QtWidgets.QSpinBox(self.ManagementGroupBox)
        self.YSpinBox.setGeometry(QtCore.QRect(220, 670, 141, 41))
        self.YSpinBox.setMaximum(1200)
        self.YSpinBox.setObjectName("YSpinBox")
        self.label_4 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 650, 141, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_5.setGeometry(QtCore.QRect(220, 650, 141, 21))
        self.label_5.setObjectName("label_5")
        self.AddLinePointButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.AddLinePointButton.setGeometry(QtCore.QRect(10, 730, 180, 41))
        self.AddLinePointButton.setObjectName("AddLinePointButton")
        self.AddPolygonPointButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.AddPolygonPointButton.setGeometry(QtCore.QRect(200, 730, 180, 41))
        self.AddPolygonPointButton.setObjectName("AddPolygonPointButton")


        self.label_6 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_6.setGeometry(QtCore.QRect(30, 940, 321, 100))
        self.label_6.setObjectName("label_6")
        self.CutPolygonButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.CutPolygonButton.setGeometry(QtCore.QRect(30, 840, 331, 31))
        self.CutPolygonButton.setObjectName("CutPolygonButton")
        self.ClearPointsButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.ClearPointsButton.setGeometry(QtCore.QRect(30, 790, 331, 31))
        self.ClearPointsButton.setObjectName("ClearPointsButton")

        self.CloseFigureButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.CloseFigureButton.setGeometry(QtCore.QRect(30, 890, 330, 41))
        self.CloseFigureButton.setObjectName("CloseFigureButton")
        
        self.DrawLabel = DrawField(self.centralwidget, 1200, 1200)
        self.DrawLabel.setGeometry(QtCore.QRect(0, 0, 1200, 1200))
        self.DrawLabel.setText("")
        self.DrawLabel.setObjectName("DrawLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ManagementGroupBox.setTitle(_translate("MainWindow", "Управление"))
        self.LineColorPickButton.setText(_translate("MainWindow", "Цвет отрезка"))
        self.PolygonColorPickButton.setText(_translate("MainWindow", "Цвет отсекателя"))
        self.CuttedColorPickButton.setText(_translate("MainWindow", "Цвет отсечённого"))
        self.label_3.setText(_translate("MainWindow", "Отсекатели"))
        self.label_7.setText(_translate("MainWindow", "Отрезки"))
        self.label_4.setText(_translate("MainWindow", "X"))
        self.label_5.setText(_translate("MainWindow", "Y"))
        self.AddLinePointButton.setText(_translate("MainWindow", "Точка в отрезок"))
        self.AddPolygonPointButton.setText(_translate("MainWindow", "Точка в отсекатель"))
        self.label_6.setText(_translate("MainWindow", "Управление мышкой\n"
" ЛКМ - поставить точку отрезка\n"
" ПКМ - поставить точку отсекателя"))
        self.CutPolygonButton.setText(_translate("MainWindow", "Отсечь"))
        self.ClearPointsButton.setText(_translate("MainWindow", "Очистить экран"))
        self.CloseFigureButton.setText(_translate("MainWindow", "Замкнуть отсекатель"))

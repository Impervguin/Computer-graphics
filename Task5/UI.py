# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from DrawField import DrawField


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ManagementGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ManagementGroupBox.setGeometry(QtCore.QRect(1200, 0, 390, 1000))
        self.ManagementGroupBox.setObjectName("ManagementGroupBox")
        self.ColorPickButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.ColorPickButton.setGeometry(QtCore.QRect(10, 60, 160, 50))
        self.ColorPickButton.setObjectName("ColorPickButton")
        self.CurrentColorLabel = DrawField(self.ManagementGroupBox, 40, 40)
        self.CurrentColorLabel.setGeometry(QtCore.QRect(320, 65, 40, 40))
        self.CurrentColorLabel.setText("")
        self.CurrentColorLabel.setObjectName("CurrenctColorLabel")
        self.label_2 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_2.setGeometry(QtCore.QRect(170, 75, 141, 20))
        self.label_2.setObjectName("label_2")
        self.FillGroupBox = QtWidgets.QGroupBox(self.ManagementGroupBox)
        self.FillGroupBox.setGeometry(QtCore.QRect(10, 130, 370, 80))
        self.FillGroupBox.setObjectName("FillGroupBox")
        self.DelayOnButton = QtWidgets.QRadioButton(self.FillGroupBox)
        self.DelayOnButton.setGeometry(QtCore.QRect(20, 40, 150, 25))
        self.DelayOnButton.setObjectName("DelayOnButton")
        self.DelayOffButton = QtWidgets.QRadioButton(self.FillGroupBox)
        self.DelayOffButton.setGeometry(QtCore.QRect(190, 40, 170, 25))
        self.DelayOffButton.setChecked(True)
        self.DelayOffButton.setObjectName("DelayOffButton")
        self.PolynomLogTextEdit = QtWidgets.QTextEdit(self.ManagementGroupBox)
        self.PolynomLogTextEdit.setReadOnly(True)
        self.PolynomLogTextEdit.setGeometry(QtCore.QRect(20, 260, 350, 351))
        self.PolynomLogTextEdit.setObjectName("PolynomLogTextEdit")
        self.label_3 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_3.setGeometry(QtCore.QRect(30, 220, 141, 41))
        self.label_3.setObjectName("label_3")
        self.XSpinBox = QtWidgets.QSpinBox(self.ManagementGroupBox)
        self.XSpinBox.setGeometry(QtCore.QRect(30, 650, 141, 41))
        self.XSpinBox.setMaximum(1200)
        self.XSpinBox.setObjectName("XSpinBox")
        self.YSpinBox = QtWidgets.QSpinBox(self.ManagementGroupBox)
        self.YSpinBox.setGeometry(QtCore.QRect(220, 650, 141, 41))
        self.YSpinBox.setMaximum(1200)
        self.YSpinBox.setObjectName("YSpinBox")
        self.label_4 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 630, 141, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_5.setGeometry(QtCore.QRect(220, 630, 141, 21))
        self.label_5.setObjectName("label_5")
        self.AddButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.AddButton.setGeometry(QtCore.QRect(10, 710, 180, 41))
        self.AddButton.setObjectName("AddButton")
        self.CloseFigureButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.CloseFigureButton.setGeometry(QtCore.QRect(200, 710, 180, 41))
        self.CloseFigureButton.setObjectName("CloseFigureButton")
        self.label_6 = QtWidgets.QLabel(self.ManagementGroupBox)
        self.label_6.setGeometry(QtCore.QRect(30, 870, 321, 100))
        self.label_6.setObjectName("label_6")
        self.FillPolygonButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.FillPolygonButton.setGeometry(QtCore.QRect(30, 820, 331, 31))
        self.FillPolygonButton.setObjectName("FillPolygonButton")
        self.ClearPointsButton = QtWidgets.QPushButton(self.ManagementGroupBox)
        self.ClearPointsButton.setGeometry(QtCore.QRect(30, 770, 331, 31))
        self.ClearPointsButton.setObjectName("ClearPointsButton")
        self.DrawLabel = DrawField(self.centralwidget, 1200, 1200)
        self.DrawLabel.setGeometry(QtCore.QRect(0, 0, 1200, 1200))
        self.DrawLabel.setText("")
        self.DrawLabel.setObjectName("DrawLabel")
        self.RealTimeBox = QtWidgets.QGroupBox(self.centralwidget)
        self.RealTimeBox.setEnabled(False)
        self.RealTimeBox.setGeometry(QtCore.QRect(1200, 1000, 391, 191))
        self.RealTimeBox.setObjectName("RealTimeBox")
        self.StopFillButton = QtWidgets.QPushButton(self.RealTimeBox)
        self.StopFillButton.setGeometry(QtCore.QRect(30, 90, 331, 31))
        self.StopFillButton.setObjectName("StopFillButton")
        MainWindow.setCentralWidget(self.centralwidget)
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ManagementGroupBox.setTitle(_translate("MainWindow", "Управление"))
        self.ColorPickButton.setText(_translate("MainWindow", "Выбрать цвет"))
        self.label_2.setText(_translate("MainWindow", "Текущий цвет:"))
        self.FillGroupBox.setTitle(_translate("MainWindow", "Заполнение"))
        self.DelayOnButton.setText(_translate("MainWindow", "С задержкой"))
        self.DelayOffButton.setText(_translate("MainWindow", "Без задержки"))
        self.label_3.setText(_translate("MainWindow", "Полигоны"))
        self.label_4.setText(_translate("MainWindow", "X"))
        self.label_5.setText(_translate("MainWindow", "Y"))
        self.AddButton.setText(_translate("MainWindow", "Добавить точку"))
        self.CloseFigureButton.setText(_translate("MainWindow", "Замкнуть фигуру"))
        self.label_6.setText(_translate("MainWindow", "Управление мышкой\n"
" ЛКМ - поставить точку\n"
"ПКМ - Замкнуть фигуру"))
        self.FillPolygonButton.setText(_translate("MainWindow", "Закрасить полигоны"))
        self.ClearPointsButton.setText(_translate("MainWindow", "Очистить точки"))
        self.RealTimeBox.setTitle(_translate("MainWindow", "Управление во время закраски"))
        self.StopFillButton.setText(_translate("MainWindow", "Остановить закраску"))

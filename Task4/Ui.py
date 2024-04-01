# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2200, 1500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.Tabs.setGeometry(QtCore.QRect(0, 0, 2200, 1500))
        self.Tabs.setTabsClosable(False)
        self.Tabs.setObjectName("Tabs")
        self.Modeling = QtWidgets.QWidget()
        self.Modeling.setObjectName("Modeling")
        self.DrawImage = QtWidgets.QLabel(self.Modeling)
        self.DrawImage.setGeometry(QtCore.QRect(10, 10, 1480, 1420))
        self.DrawImage.setText("")
        self.DrawImage.setObjectName("DrawImage")
        self.Gr = QtWidgets.QGroupBox(self.Modeling)
        self.Gr.setGeometry(QtCore.QRect(1510, 10, 680, 1420))
        self.Gr.setObjectName("Gr")
        self.Algo = QtWidgets.QGroupBox(self.Gr)
        self.Algo.setGeometry(QtCore.QRect(10, 50, 651, 301))
        self.Algo.setObjectName("Algo")
        self.LibraryButton = QtWidgets.QRadioButton(self.Algo)
        self.LibraryButton.setGeometry(QtCore.QRect(10, 50, 621, 40))
        self.LibraryButton.setChecked(True)
        self.LibraryButton.setObjectName("LibraryButton")
        self.CanonicButton = QtWidgets.QRadioButton(self.Algo)
        self.CanonicButton.setGeometry(QtCore.QRect(10, 100, 621, 40))
        self.CanonicButton.setObjectName("CanonicButton")
        self.ParametricButton = QtWidgets.QRadioButton(self.Algo)
        self.ParametricButton.setGeometry(QtCore.QRect(10, 150, 621, 40))
        self.ParametricButton.setObjectName("ParametricButton")
        self.BrezButton = QtWidgets.QRadioButton(self.Algo)
        self.BrezButton.setGeometry(QtCore.QRect(10, 200, 621, 40))
        self.BrezButton.setObjectName("BrezButton")
        self.MidpointButton = QtWidgets.QRadioButton(self.Algo)
        self.MidpointButton.setGeometry(QtCore.QRect(10, 250, 621, 40))
        self.MidpointButton.setObjectName("MidpointButton")
        self.XStartBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.XStartBox.setGeometry(QtCore.QRect(40, 400, 231, 71))
        self.XStartBox.setMaximum(2000.0)
        self.XStartBox.setProperty("value", 1000.0)
        self.XStartBox.setObjectName("XStartBox")
        self.RadiusBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.RadiusBox.setGeometry(QtCore.QRect(40, 530, 231, 71))
        self.RadiusBox.setMaximum(2000.0)
        self.RadiusBox.setProperty("value", 200.0)
        self.RadiusBox.setObjectName("RadiusBox")
        self.YStartBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.YStartBox.setGeometry(QtCore.QRect(410, 400, 231, 71))
        self.YStartBox.setMaximum(2000.0)
        self.YStartBox.setProperty("value", 1000.0)
        self.YStartBox.setObjectName("YStartBox")
        self.CircleButton = QtWidgets.QPushButton(self.Gr)
        self.CircleButton.setGeometry(QtCore.QRect(40, 720, 231, 61))
        self.CircleButton.setObjectName("CircleButton")
        self.StepBox = QtWidgets.QSpinBox(self.Gr)
        self.StepBox.setGeometry(QtCore.QRect(40, 810, 231, 71))
        self.StepBox.setMaximum(360)
        self.StepBox.setProperty("value", 5)
        self.StepBox.setObjectName("StepBox")
        self.SpectreCircleButton = QtWidgets.QPushButton(self.Gr)
        self.SpectreCircleButton.setGeometry(QtCore.QRect(40, 1100, 291, 71))
        self.SpectreCircleButton.setObjectName("SpectreCircleButton")
        self.SpectreRadiusBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.SpectreRadiusBox.setGeometry(QtCore.QRect(40, 910, 241, 71))
        self.SpectreRadiusBox.setMaximum(1000.0)
        self.SpectreRadiusBox.setProperty("value", 300.0)
        self.SpectreRadiusBox.setObjectName("SpectreRadiusBox")
        self.ClearScreen = QtWidgets.QPushButton(self.Gr)
        self.ClearScreen.setGeometry(QtCore.QRect(130, 1350, 421, 51))
        self.ClearScreen.setObjectName("ClearScreen")
        self.BackColorPicker = QtWidgets.QPushButton(self.Gr)
        self.BackColorPicker.setGeometry(QtCore.QRect(20, 1200, 311, 131))
        self.BackColorPicker.setObjectName("BackColorPicker")
        self.DrawColorPicker = QtWidgets.QPushButton(self.Gr)
        self.DrawColorPicker.setGeometry(QtCore.QRect(350, 1200, 311, 131))
        self.DrawColorPicker.setObjectName("DrawColorPicker")
        self.label_3 = QtWidgets.QLabel(self.Gr)
        self.label_3.setGeometry(QtCore.QRect(40, 360, 231, 34))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.Gr)
        self.label_4.setGeometry(QtCore.QRect(410, 360, 231, 34))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.Gr)
        self.label_5.setGeometry(QtCore.QRect(40, 780, 231, 34))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.Gr)
        self.label_6.setGeometry(QtCore.QRect(40, 880, 261, 34))
        self.label_6.setObjectName("label_6")
        self.EllipsButton = QtWidgets.QPushButton(self.Gr)
        self.EllipsButton.setGeometry(QtCore.QRect(410, 720, 231, 61))
        self.EllipsButton.setObjectName("EllipsButton")
        self.WidthBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.WidthBox.setGeometry(QtCore.QRect(410, 530, 231, 71))
        self.WidthBox.setMaximum(2000.0)
        self.WidthBox.setProperty("value", 200.0)
        self.WidthBox.setObjectName("WidthBox")
        self.label_2 = QtWidgets.QLabel(self.Gr)
        self.label_2.setGeometry(QtCore.QRect(410, 490, 231, 34))
        self.label_2.setObjectName("label_2")
        self.HeightBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.HeightBox.setGeometry(QtCore.QRect(410, 640, 231, 71))
        self.HeightBox.setMaximum(2000.0)
        self.HeightBox.setProperty("value", 200.0)
        self.HeightBox.setObjectName("HeightBox")
        self.label_9 = QtWidgets.QLabel(self.Gr)
        self.label_9.setGeometry(QtCore.QRect(410, 600, 231, 34))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.Gr)
        self.label_10.setGeometry(QtCore.QRect(410, 780, 221, 34))
        self.label_10.setObjectName("label_10")
        self.FigurenumBox = QtWidgets.QSpinBox(self.Gr)
        self.FigurenumBox.setGeometry(QtCore.QRect(410, 810, 231, 71))
        self.FigurenumBox.setMaximum(360)
        self.FigurenumBox.setProperty("value", 5)
        self.FigurenumBox.setObjectName("FigurenumBox")
        self.label_7 = QtWidgets.QLabel(self.Gr)
        self.label_7.setGeometry(QtCore.QRect(40, 490, 231, 34))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.Gr)
        self.label_8.setGeometry(QtCore.QRect(410, 880, 261, 34))
        self.label_8.setObjectName("label_8")
        self.SpectreWidthBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.SpectreWidthBox.setGeometry(QtCore.QRect(410, 910, 241, 71))
        self.SpectreWidthBox.setMaximum(1000.0)
        self.SpectreWidthBox.setProperty("value", 300.0)
        self.SpectreWidthBox.setObjectName("SpectreWidthBox")
        self.label_11 = QtWidgets.QLabel(self.Gr)
        self.label_11.setGeometry(QtCore.QRect(410, 980, 261, 34))
        self.label_11.setObjectName("label_11")
        self.SpectreHeightBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.SpectreHeightBox.setGeometry(QtCore.QRect(410, 1010, 241, 71))
        self.SpectreHeightBox.setMaximum(1000.0)
        self.SpectreHeightBox.setProperty("value", 300.0)
        self.SpectreHeightBox.setObjectName("SpectreHeightBox")
        self.SpectreEllipsButton = QtWidgets.QPushButton(self.Gr)
        self.SpectreEllipsButton.setGeometry(QtCore.QRect(350, 1100, 301, 71))
        self.SpectreEllipsButton.setObjectName("SpectreEllipsButton")
        self.Tabs.addTab(self.Modeling, "")
        self.Time = QtWidgets.QWidget()
        self.Time.setObjectName("Time")
        self.Tabs.addTab(self.Time, "")
        self.Timellips = QtWidgets.QWidget()
        self.Timellips.setObjectName("Timellips")
        self.Tabs.addTab(self.Timellips, "")

        pyqtgraph.setConfigOption("background", pyqtgraph.mkColor(255, 255, 255))
        pyqtgraph.setConfigOption("foreground", pyqtgraph.mkColor(0, 0, 0))

        self.TimeGraph = pyqtgraph.PlotWidget(self.Time)
        self.TimeGraph.setGeometry(10, 10, 2180, 1420)
        
        self.TimellipsGraph = pyqtgraph.PlotWidget(self.Timellips)
        self.TimellipsGraph.setGeometry(10, 10, 2180, 1420)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.Tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Gr.setTitle(_translate("MainWindow", "Управление"))
        self.Algo.setTitle(_translate("MainWindow", "Алгоритмы"))
        self.LibraryButton.setText(_translate("MainWindow", "Библиотечный алгоритм"))
        self.CanonicButton.setText(_translate("MainWindow", "Канонический алгоритм"))
        self.ParametricButton.setText(_translate("MainWindow", "Параметрический алгоритм"))
        self.BrezButton.setText(_translate("MainWindow", "Алгоритм Брезенхема"))
        self.MidpointButton.setText(_translate("MainWindow", "Алгоритм средней точки"))
        self.CircleButton.setText(_translate("MainWindow", "Окружность"))
        self.SpectreCircleButton.setText(_translate("MainWindow", "Спектр окружностей"))
        self.ClearScreen.setText(_translate("MainWindow", "Очистить экран"))
        self.BackColorPicker.setText(_translate("MainWindow", "Выбрать цвет фона"))
        self.DrawColorPicker.setText(_translate("MainWindow", "Выбрать цвет отрезка"))
        self.label_3.setText(_translate("MainWindow", "Х центра"))
        self.label_4.setText(_translate("MainWindow", "Y центра"))
        self.label_5.setText(_translate("MainWindow", "Шаг длины"))
        self.label_6.setText(_translate("MainWindow", "Начальный радиус"))
        self.EllipsButton.setText(_translate("MainWindow", "Эллипс"))
        self.label_2.setText(_translate("MainWindow", "Ширина"))
        self.label_9.setText(_translate("MainWindow", "Высота"))
        self.label_10.setText(_translate("MainWindow", "Кол-во фигур"))
        self.label_7.setText(_translate("MainWindow", "Радиус"))
        self.label_8.setText(_translate("MainWindow", "Начальная ширина"))
        self.label_11.setText(_translate("MainWindow", "Начальная высота"))
        self.SpectreEllipsButton.setText(_translate("MainWindow", "Спектр эллипсов"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Modeling), _translate("MainWindow", "Моделирование"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Time), _translate("MainWindow", "Замеры окружность"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.TimellipsGraph), _translate("MainWindow", "Замеры эллипс"))

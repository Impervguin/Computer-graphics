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
        self.Algo.setGeometry(QtCore.QRect(10, 50, 651, 361))
        self.Algo.setObjectName("Algo")
        self.LibraryButton = QtWidgets.QRadioButton(self.Algo)
        self.LibraryButton.setGeometry(QtCore.QRect(10, 50, 621, 40))
        self.LibraryButton.setChecked(True)
        self.LibraryButton.setObjectName("LibraryButton")
        self.BrFloatButton = QtWidgets.QRadioButton(self.Algo)
        self.BrFloatButton.setGeometry(QtCore.QRect(10, 100, 621, 40))
        self.BrFloatButton.setObjectName("BrFloatButton")
        self.BrintButton = QtWidgets.QRadioButton(self.Algo)
        self.BrintButton.setGeometry(QtCore.QRect(10, 150, 621, 40))
        self.BrintButton.setObjectName("BrintButton")
        self.BrSmoothButton = QtWidgets.QRadioButton(self.Algo)
        self.BrSmoothButton.setGeometry(QtCore.QRect(10, 200, 621, 40))
        self.BrSmoothButton.setObjectName("BrSmoothButton")
        self.WUButton = QtWidgets.QRadioButton(self.Algo)
        self.WUButton.setGeometry(QtCore.QRect(10, 250, 621, 40))
        self.WUButton.setObjectName("WUButton")
        self.DDAButton = QtWidgets.QRadioButton(self.Algo)
        self.DDAButton.setGeometry(QtCore.QRect(10, 300, 621, 40))
        self.DDAButton.setObjectName("DDAButton")
        self.XStartBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.XStartBox.setGeometry(QtCore.QRect(20, 470, 231, 71))
        self.XStartBox.setMaximum(2000.0)
        self.XStartBox.setProperty("value", 100.0)
        self.XStartBox.setObjectName("XStartBox")
        self.XEndBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.XEndBox.setGeometry(QtCore.QRect(430, 470, 231, 71))
        self.XEndBox.setMaximum(2000.0)
        self.XEndBox.setProperty("value", 1400.0)
        self.XEndBox.setObjectName("XEndBox")
        self.YStartBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.YStartBox.setGeometry(QtCore.QRect(20, 590, 231, 71))
        self.YStartBox.setMaximum(2000.0)
        self.YStartBox.setProperty("value", 100.0)
        self.YStartBox.setObjectName("YStartBox")
        self.YEndBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.YEndBox.setGeometry(QtCore.QRect(430, 590, 231, 71))
        self.YEndBox.setMaximum(2000.0)
        self.YEndBox.setProperty("value", 1400.0)
        self.YEndBox.setObjectName("YEndBox")
        self.DrawButton = QtWidgets.QPushButton(self.Gr)
        self.DrawButton.setGeometry(QtCore.QRect(130, 670, 421, 51))
        self.DrawButton.setObjectName("DrawButton")
        self.AngleBox = QtWidgets.QSpinBox(self.Gr)
        self.AngleBox.setGeometry(QtCore.QRect(20, 770, 231, 71))
        self.AngleBox.setMaximum(360)
        self.AngleBox.setProperty("value", 5)
        self.AngleBox.setObjectName("AngleBox")
        self.SpectreButton = QtWidgets.QPushButton(self.Gr)
        self.SpectreButton.setGeometry(QtCore.QRect(130, 850, 421, 51))
        self.SpectreButton.setObjectName("SpectreButton")
        self.LineBox = QtWidgets.QDoubleSpinBox(self.Gr)
        self.LineBox.setGeometry(QtCore.QRect(420, 770, 241, 71))
        self.LineBox.setMaximum(1000.0)
        self.LineBox.setProperty("value", 300.0)
        self.LineBox.setObjectName("LineBox")
        self.ClearScreen = QtWidgets.QPushButton(self.Gr)
        self.ClearScreen.setGeometry(QtCore.QRect(130, 1300, 421, 51))
        self.ClearScreen.setObjectName("ClearScreen")
        self.BackColorPicker = QtWidgets.QPushButton(self.Gr)
        self.BackColorPicker.setGeometry(QtCore.QRect(20, 990, 311, 131))
        self.BackColorPicker.setObjectName("BackColorPicker")
        self.DrawColorPicker = QtWidgets.QPushButton(self.Gr)
        self.DrawColorPicker.setGeometry(QtCore.QRect(350, 990, 311, 131))
        self.DrawColorPicker.setObjectName("DrawColorPicker")
        self.label = QtWidgets.QLabel(self.Gr)
        self.label.setGeometry(QtCore.QRect(430, 430, 231, 34))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Gr)
        self.label_2.setGeometry(QtCore.QRect(430, 550, 231, 34))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.Gr)
        self.label_3.setGeometry(QtCore.QRect(20, 430, 231, 34))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.Gr)
        self.label_4.setGeometry(QtCore.QRect(20, 550, 231, 34))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.Gr)
        self.label_5.setGeometry(QtCore.QRect(20, 730, 231, 34))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.Gr)
        self.label_6.setGeometry(QtCore.QRect(420, 730, 231, 34))
        self.label_6.setObjectName("label_6")
        self.Tabs.addTab(self.Modeling, "")
        self.Time = QtWidgets.QWidget()
        self.Time.setObjectName("Time")
        self.Tabs.addTab(self.Time, "")
        self.Steps = QtWidgets.QWidget()
        self.Steps.setObjectName("Steps")
        self.Tabs.addTab(self.Steps, "")

        pyqtgraph.setConfigOption("background", pyqtgraph.mkColor(255, 255, 255))
        pyqtgraph.setConfigOption("foreground", pyqtgraph.mkColor(0, 0, 0))

        self.TimeGraph = pyqtgraph.PlotWidget(self.Time)
        self.TimeGraph.setGeometry(10, 10, 2180, 1420)

        self.GraphGroup = QtWidgets.QGridLayout()
        # self.GraphGroup.setGeometry(10, 10, 2180, 1420)
        self.Steps.setLayout(self.GraphGroup)

        self.AllGraph = pyqtgraph.PlotWidget(self.Steps)
        self.GraphGroup.addWidget(self.AllGraph, 0, 0)

        self.DDAGraph = pyqtgraph.PlotWidget(self.Steps)
        self.GraphGroup.addWidget(self.DDAGraph, 0, 1)

        self.WUGraph = pyqtgraph.PlotWidget(self.Steps)
        self.GraphGroup.addWidget(self.WUGraph, 0, 2)

        self.BrezenkhemFloatGraph = pyqtgraph.PlotWidget(self.Steps)
        self.GraphGroup.addWidget(self.BrezenkhemFloatGraph, 1, 0)

        self.BrezenkhemIntGraph = pyqtgraph.PlotWidget(self.Steps)
        self.GraphGroup.addWidget(self.BrezenkhemIntGraph, 1, 1)

        self.BrezenkhemSmoothGraph = pyqtgraph.PlotWidget(self.Steps)
        self.GraphGroup.addWidget(self.BrezenkhemSmoothGraph, 1, 2)

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
        self.BrFloatButton.setText(_translate("MainWindow", "Вещественный алгоритм Брезенхема"))
        self.BrintButton.setText(_translate("MainWindow", "Целочисленный алгоритм Брезенхема"))
        self.BrSmoothButton.setText(_translate("MainWindow", "Алгоритм Брезенхема сглаживания"))
        self.WUButton.setText(_translate("MainWindow", "Алгоритм ВУ"))
        self.DDAButton.setText(_translate("MainWindow", "Алгоритм ЦДА"))
        self.DrawButton.setText(_translate("MainWindow", "Начертить"))
        self.SpectreButton.setText(_translate("MainWindow", "Спектр"))
        self.ClearScreen.setText(_translate("MainWindow", "Очистить экран"))
        self.BackColorPicker.setText(_translate("MainWindow", "Выбрать цвет фона"))
        self.DrawColorPicker.setText(_translate("MainWindow", "Выбрать цвет отрезка"))
        self.label.setText(_translate("MainWindow", "Х конца"))
        self.label_2.setText(_translate("MainWindow", "Y конца"))
        self.label_3.setText(_translate("MainWindow", "Х начала"))
        self.label_4.setText(_translate("MainWindow", "Y начала"))
        self.label_5.setText(_translate("MainWindow", "Шаг угла"))
        self.label_6.setText(_translate("MainWindow", "Длина отрезка"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Modeling), _translate("MainWindow", "Моделирование"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Time), _translate("MainWindow", "Замеры"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Steps), _translate("MainWindow", "Ступеньки"))

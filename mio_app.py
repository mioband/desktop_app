# Form implementation generated from reading ui file 'mio_app.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 330)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LeftBandGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.LeftBandGroupBox.setEnabled(True)
        self.LeftBandGroupBox.setGeometry(QtCore.QRect(10, 30, 240, 161))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.LeftBandGroupBox.setFont(font)
        self.LeftBandGroupBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LeftBandGroupBox.setObjectName("LeftBandGroupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.LeftBandGroupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 221, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.LeftBandVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.LeftBandVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.LeftBandVerticalLayout.setObjectName("LeftBandVerticalLayout")
        self.LeftBandFormLayout = QtWidgets.QFormLayout()
        self.LeftBandFormLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LeftBandFormLayout.setObjectName("LeftBandFormLayout")
        self.LeftBandModeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.LeftBandModeLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.LeftBandModeLabel.setFont(font)
        self.LeftBandModeLabel.setObjectName("LeftBandModeLabel")
        self.LeftBandFormLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.LeftBandModeLabel)
        self.LeftBandModeComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.LeftBandModeComboBox.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.LeftBandModeComboBox.setFont(font)
        self.LeftBandModeComboBox.setObjectName("LeftBandModeComboBox")
        self.LeftBandModeComboBox.addItem("")
        self.LeftBandModeComboBox.addItem("")
        self.LeftBandFormLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.LeftBandModeComboBox)
        self.LeftBandEnabled = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.LeftBandEnabled.setObjectName("LeftBandEnabled")
        self.LeftBandFormLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.LeftBandEnabled)
        self.LeftBandConfigButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.LeftBandConfigButton.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.LeftBandConfigButton.setFont(font)
        self.LeftBandConfigButton.setObjectName("LeftBandConfigButton")
        self.LeftBandFormLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.LeftBandConfigButton)
        self.LeftBandVerticalLayout.addLayout(self.LeftBandFormLayout)
        self.RightBandGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.RightBandGroupBox.setEnabled(True)
        self.RightBandGroupBox.setGeometry(QtCore.QRect(300, 30, 240, 161))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.RightBandGroupBox.setFont(font)
        self.RightBandGroupBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RightBandGroupBox.setObjectName("RightBandGroupBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.RightBandGroupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 221, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.RightBandVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.RightBandVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.RightBandVerticalLayout.setObjectName("RightBandVerticalLayout")
        self.RightBandFormLayout = QtWidgets.QFormLayout()
        self.RightBandFormLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RightBandFormLayout.setObjectName("RightBandFormLayout")
        self.RightBandModeLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.RightBandModeLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.RightBandModeLabel.setFont(font)
        self.RightBandModeLabel.setObjectName("RightBandModeLabel")
        self.RightBandFormLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.RightBandModeLabel)
        self.RightBandModeComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.RightBandModeComboBox.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.RightBandModeComboBox.setFont(font)
        self.RightBandModeComboBox.setObjectName("RightBandModeComboBox")
        self.RightBandModeComboBox.addItem("")
        self.RightBandModeComboBox.addItem("")
        self.RightBandFormLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.RightBandModeComboBox)
        self.RightBandEnabled = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.RightBandEnabled.setObjectName("RightBandEnabled")
        self.RightBandFormLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.RightBandEnabled)
        self.RightBandConfigButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.RightBandConfigButton.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.RightBandConfigButton.setFont(font)
        self.RightBandConfigButton.setObjectName("RightBandConfigButton")
        self.RightBandFormLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.RightBandConfigButton)
        self.RightBandVerticalLayout.addLayout(self.RightBandFormLayout)
        self.SwapBandsButton = QtWidgets.QPushButton(self.centralwidget)
        self.SwapBandsButton.setGeometry(QtCore.QRect(260, 110, 31, 31))
        self.SwapBandsButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("swap.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.SwapBandsButton.setIcon(icon)
        self.SwapBandsButton.setObjectName("SwapBandsButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.MenuBar = QtWidgets.QMenuBar(MainWindow)
        self.MenuBar.setEnabled(True)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 549, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(False)
        self.MenuBar.setFont(font)
        self.MenuBar.setNativeMenuBar(False)
        self.MenuBar.setObjectName("MenuBar")
        self.FileMenu = QtWidgets.QMenu(self.MenuBar)
        self.FileMenu.setObjectName("FileMenu")
        MainWindow.setMenuBar(self.MenuBar)
        self.FileMenuImportConfig = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.FileMenuImportConfig.setFont(font)
        self.FileMenuImportConfig.setObjectName("FileMenuImportConfig")
        self.FileMenuExportConfig = QtGui.QAction(MainWindow)
        self.FileMenuExportConfig.setObjectName("FileMenuExportConfig")
        self.FileMenu.addAction(self.FileMenuImportConfig)
        self.FileMenu.addAction(self.FileMenuExportConfig)
        self.MenuBar.addAction(self.FileMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mioband 0.6"))
        self.LeftBandGroupBox.setTitle(_translate("MainWindow", "Браслет 1 (левая рука)"))
        self.LeftBandModeLabel.setText(_translate("MainWindow", "Режим"))
        self.LeftBandModeComboBox.setItemText(0, _translate("MainWindow", "Мышь"))
        self.LeftBandModeComboBox.setItemText(1, _translate("MainWindow", "Клавиатура"))
        self.LeftBandEnabled.setText(_translate("MainWindow", "Задействовано"))
        self.LeftBandConfigButton.setText(_translate("MainWindow", "Параметры..."))
        self.RightBandGroupBox.setTitle(_translate("MainWindow", "Браслет 2 (правая рука)"))
        self.RightBandModeLabel.setText(_translate("MainWindow", "Режим"))
        self.RightBandModeComboBox.setItemText(0, _translate("MainWindow", "Мышь"))
        self.RightBandModeComboBox.setItemText(1, _translate("MainWindow", "Клавиатура"))
        self.RightBandEnabled.setText(_translate("MainWindow", "Задействовано"))
        self.RightBandConfigButton.setText(_translate("MainWindow", "Параметры..."))
        self.FileMenu.setTitle(_translate("MainWindow", "Файл..."))
        self.FileMenuImportConfig.setText(_translate("MainWindow", "Импорт конфигурации"))
        self.FileMenuExportConfig.setText(_translate("MainWindow", "Экспорт конфигурации"))

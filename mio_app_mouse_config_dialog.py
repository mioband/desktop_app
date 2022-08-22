# Form implementation generated from reading ui file 'mio_app_mouse_config_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MouseConfigDialog(object):
    def setupUi(self, MouseConfigDialog):
        MouseConfigDialog.setObjectName("MouseConfigDialog")
        MouseConfigDialog.resize(230, 200)
        self.gridLayoutWidget = QtWidgets.QWidget(MouseConfigDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 10, 221, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.MouseConfigGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.MouseConfigGridLayout.setContentsMargins(0, 0, 0, 0)
        self.MouseConfigGridLayout.setHorizontalSpacing(4)
        self.MouseConfigGridLayout.setVerticalSpacing(0)
        self.MouseConfigGridLayout.setObjectName("MouseConfigGridLayout")
        self.MouseSensitivityLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        # font = QtGui.QFont()
        # font.setPointSize(9)
        # self.MouseSensitivityLabel.setFont(font)
        self.MouseSensitivityLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.MouseSensitivityLabel.setObjectName("MouseSensitivityLabel")
        self.MouseConfigGridLayout.addWidget(self.MouseSensitivityLabel, 2, 0, 1, 1)
        self.MouseGestureActionComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.MouseGestureActionComboBox.setObjectName("MouseGestureActionComboBox")
        self.MouseGestureActionComboBox.addItem("")
        self.MouseGestureActionComboBox.addItem("")
        self.MouseConfigGridLayout.addWidget(self.MouseGestureActionComboBox, 0, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.MouseGestureLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        # font = QtGui.QFont()
        # font.setPointSize(9)
        # self.MouseGestureLabel.setFont(font)
        self.MouseGestureLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.MouseGestureLabel.setObjectName("MouseGestureLabel")
        self.MouseConfigGridLayout.addWidget(self.MouseGestureLabel, 0, 0, 1, 1)
        self.MouseSensitivitySlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.MouseSensitivitySlider.setMinimumSize(QtCore.QSize(80, 22))
        self.MouseSensitivitySlider.setMaximumSize(QtCore.QSize(80, 22))
        self.MouseSensitivitySlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.MouseSensitivitySlider.setObjectName("MouseSensitivitySlider")
        self.MouseConfigGridLayout.addWidget(self.MouseSensitivitySlider, 2, 1, 1, 1)
        self.InvertMouseLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        # font = QtGui.QFont()
        # font.setPointSize(9)
        # self.InvertMouseLabel.setFont(font)
        self.InvertMouseLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.InvertMouseLabel.setObjectName("InvertMouseLabel")
        self.MouseConfigGridLayout.addWidget(self.InvertMouseLabel, 1, 0, 1, 1)
        self.InvertMouseCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.InvertMouseCheckBox.setText("")
        self.InvertMouseCheckBox.setObjectName("InvertMouseCheckBox")
        self.MouseConfigGridLayout.addWidget(self.InvertMouseCheckBox, 1, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.MouseConfigCancelButton = QtWidgets.QPushButton(MouseConfigDialog)
        self.MouseConfigCancelButton.setGeometry(QtCore.QRect(20, 150, 93, 28))
        self.MouseConfigCancelButton.setObjectName("MouseConfigCancelButton")
        self.MouseConfigApplyButton = QtWidgets.QPushButton(MouseConfigDialog)
        self.MouseConfigApplyButton.setGeometry(QtCore.QRect(120, 150, 93, 28))
        self.MouseConfigApplyButton.setObjectName("MouseConfigApplyButton")

        self.retranslateUi(MouseConfigDialog)
        QtCore.QMetaObject.connectSlotsByName(MouseConfigDialog)

    def retranslateUi(self, MouseConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        MouseConfigDialog.setWindowTitle(_translate("MouseConfigDialog", "Параметры"))
        self.MouseSensitivityLabel.setText(_translate("MouseConfigDialog", "Чувствительность"))
        self.MouseGestureActionComboBox.setItemText(0, _translate("MouseConfigDialog", "ЛКМ"))
        self.MouseGestureActionComboBox.setItemText(1, _translate("MouseConfigDialog", "ПКМ"))
        self.MouseGestureLabel.setText(_translate("MouseConfigDialog", "Жест 1 (сжатый кулак)"))
        self.InvertMouseLabel.setText(_translate("MouseConfigDialog", "Инвертировать"))
        self.MouseConfigCancelButton.setText(_translate("MouseConfigDialog", "Отмена"))
        self.MouseConfigApplyButton.setText(_translate("MouseConfigDialog", "Применить"))

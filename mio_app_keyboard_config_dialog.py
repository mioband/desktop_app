# Form implementation generated from reading ui file 'mio_app_keyboard_config_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_KeyboardConfigDialog(object):
    def setupUi(self, KeyboardConfigDialog):
        KeyboardConfigDialog.setObjectName("KeyboardConfigDialog")
        KeyboardConfigDialog.resize(247, 188)
        self.KeyboardConfigCancelButton = QtWidgets.QPushButton(KeyboardConfigDialog)
        self.KeyboardConfigCancelButton.setGeometry(QtCore.QRect(30, 150, 93, 28))
        self.KeyboardConfigCancelButton.setObjectName("KeyboardConfigCancelButton")
        self.KeyboardConfigApplyButton = QtWidgets.QPushButton(KeyboardConfigDialog)
        self.KeyboardConfigApplyButton.setGeometry(QtCore.QRect(130, 150, 93, 28))
        self.KeyboardConfigApplyButton.setObjectName("KeyboardConfigApplyButton")
        self.gridLayoutWidget = QtWidgets.QWidget(KeyboardConfigDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 233, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.KeyboardConfigGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.KeyboardConfigGridLayout.setContentsMargins(0, 0, 0, 0)
        self.KeyboardConfigGridLayout.setHorizontalSpacing(4)
        self.KeyboardConfigGridLayout.setVerticalSpacing(0)
        self.KeyboardConfigGridLayout.setObjectName("KeyboardConfigGridLayout")
        self.TiltForwardComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.TiltForwardComboBox.setMinimumSize(QtCore.QSize(60, 20))
        self.TiltForwardComboBox.setMaximumSize(QtCore.QSize(120, 20))
        self.TiltForwardComboBox.setObjectName("TiltForwardComboBox")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.TiltForwardComboBox.addItem("")
        self.KeyboardConfigGridLayout.addWidget(self.TiltForwardComboBox, 0, 1, 1, 1)
        self.TiltLeftLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.TiltLeftLabel.setFont(font)
        self.TiltLeftLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.TiltLeftLabel.setObjectName("TiltLeftLabel")
        self.KeyboardConfigGridLayout.addWidget(self.TiltLeftLabel, 2, 0, 1, 1)
        self.TiltBackwardLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.TiltBackwardLabel.setFont(font)
        self.TiltBackwardLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.TiltBackwardLabel.setObjectName("TiltBackwardLabel")
        self.KeyboardConfigGridLayout.addWidget(self.TiltBackwardLabel, 1, 0, 1, 1)
        self.TiltForwardLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.TiltForwardLabel.setFont(font)
        self.TiltForwardLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.TiltForwardLabel.setObjectName("TiltForwardLabel")
        self.KeyboardConfigGridLayout.addWidget(self.TiltForwardLabel, 0, 0, 1, 1)
        self.TiltRightLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.TiltRightLabel.setFont(font)
        self.TiltRightLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.TiltRightLabel.setObjectName("TiltRightLabel")
        self.KeyboardConfigGridLayout.addWidget(self.TiltRightLabel, 3, 0, 1, 1)
        self.KeyboardGestureActionLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        # font = QtGui.QFont()
        # font.setPointSize(9)
        # font.setBold(False)
        # font.setWeight(50)
        self.KeyboardGestureActionLabel.setFont(font)
        self.KeyboardGestureActionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.KeyboardGestureActionLabel.setObjectName("KeyboardGestureActionLabel")
        self.KeyboardConfigGridLayout.addWidget(self.KeyboardGestureActionLabel, 4, 0, 1, 1)
        self.TiltBackwardComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.TiltBackwardComboBox.setMinimumSize(QtCore.QSize(60, 20))
        self.TiltBackwardComboBox.setMaximumSize(QtCore.QSize(120, 20))
        self.TiltBackwardComboBox.setObjectName("TiltBackwardComboBox")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.TiltBackwardComboBox.addItem("")
        self.KeyboardConfigGridLayout.addWidget(self.TiltBackwardComboBox, 1, 1, 1, 1)
        self.TiltLeftComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.TiltLeftComboBox.setMinimumSize(QtCore.QSize(60, 20))
        self.TiltLeftComboBox.setMaximumSize(QtCore.QSize(120, 20))
        self.TiltLeftComboBox.setObjectName("TiltLeftComboBox")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.TiltLeftComboBox.addItem("")
        self.KeyboardConfigGridLayout.addWidget(self.TiltLeftComboBox, 2, 1, 1, 1)
        self.TiltRightComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.TiltRightComboBox.setMinimumSize(QtCore.QSize(60, 20))
        self.TiltRightComboBox.setMaximumSize(QtCore.QSize(120, 20))
        self.TiltRightComboBox.setObjectName("TiltRightComboBox")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.TiltRightComboBox.addItem("")
        self.KeyboardConfigGridLayout.addWidget(self.TiltRightComboBox, 3, 1, 1, 1)
        self.KeyboardGestureActionComboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.KeyboardGestureActionComboBox.setMinimumSize(QtCore.QSize(60, 20))
        self.KeyboardGestureActionComboBox.setMaximumSize(QtCore.QSize(120, 20))
        self.KeyboardGestureActionComboBox.setObjectName("KeyboardGestureActionComboBox")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardGestureActionComboBox.addItem("")
        self.KeyboardConfigGridLayout.addWidget(self.KeyboardGestureActionComboBox, 4, 1, 1, 1)

        self.retranslateUi(KeyboardConfigDialog)
        QtCore.QMetaObject.connectSlotsByName(KeyboardConfigDialog)

    def retranslateUi(self, KeyboardConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        KeyboardConfigDialog.setWindowTitle(_translate("KeyboardConfigDialog", "??????????????????"))
        self.KeyboardConfigCancelButton.setText(_translate("KeyboardConfigDialog", "????????????"))
        self.KeyboardConfigApplyButton.setText(_translate("KeyboardConfigDialog", "??????????????????"))
        self.TiltForwardComboBox.setItemText(0, _translate("KeyboardConfigDialog", "W"))
        self.TiltForwardComboBox.setItemText(1, _translate("KeyboardConfigDialog", "A"))
        self.TiltForwardComboBox.setItemText(2, _translate("KeyboardConfigDialog", "S"))
        self.TiltForwardComboBox.setItemText(3, _translate("KeyboardConfigDialog", "D"))
        self.TiltForwardComboBox.setItemText(4, _translate("KeyboardConfigDialog", "E"))
        self.TiltForwardComboBox.setItemText(5, _translate("KeyboardConfigDialog", "????????????"))
        self.TiltForwardComboBox.setItemText(6, _translate("KeyboardConfigDialog", "Shift"))
        self.TiltForwardComboBox.setItemText(7, _translate("KeyboardConfigDialog", "??????"))
        self.TiltForwardComboBox.setItemText(8, _translate("KeyboardConfigDialog", "??????"))
        self.TiltForwardComboBox.setItemText(9, _translate("KeyboardConfigDialog", "???????????? ????????"))
        self.TiltForwardComboBox.setItemText(10, _translate("KeyboardConfigDialog", "???????????? ??????????"))
        self.TiltLeftLabel.setText(_translate("KeyboardConfigDialog", "???????????? ??????????"))
        self.TiltBackwardLabel.setText(_translate("KeyboardConfigDialog", "???????????? ??????????"))
        self.TiltForwardLabel.setText(_translate("KeyboardConfigDialog", "???????????? ????????????"))
        self.TiltRightLabel.setText(_translate("KeyboardConfigDialog", "???????????? ????????????"))
        self.KeyboardGestureActionLabel.setText(_translate("KeyboardConfigDialog", "???????? 1 (???????????? ??????????)"))
        self.TiltBackwardComboBox.setItemText(0, _translate("KeyboardConfigDialog", "W"))
        self.TiltBackwardComboBox.setItemText(1, _translate("KeyboardConfigDialog", "A"))
        self.TiltBackwardComboBox.setItemText(2, _translate("KeyboardConfigDialog", "S"))
        self.TiltBackwardComboBox.setItemText(3, _translate("KeyboardConfigDialog", "D"))
        self.TiltBackwardComboBox.setItemText(4, _translate("KeyboardConfigDialog", "E"))
        self.TiltBackwardComboBox.setItemText(5, _translate("KeyboardConfigDialog", "????????????"))
        self.TiltBackwardComboBox.setItemText(6, _translate("KeyboardConfigDialog", "Shift"))
        self.TiltBackwardComboBox.setItemText(7, _translate("KeyboardConfigDialog", "??????"))
        self.TiltBackwardComboBox.setItemText(8, _translate("KeyboardConfigDialog", "??????"))
        self.TiltBackwardComboBox.setItemText(9, _translate("KeyboardConfigDialog", "???????????? ????????"))
        self.TiltBackwardComboBox.setItemText(10, _translate("KeyboardConfigDialog", "???????????? ??????????"))
        self.TiltLeftComboBox.setItemText(0, _translate("KeyboardConfigDialog", "W"))
        self.TiltLeftComboBox.setItemText(1, _translate("KeyboardConfigDialog", "A"))
        self.TiltLeftComboBox.setItemText(2, _translate("KeyboardConfigDialog", "S"))
        self.TiltLeftComboBox.setItemText(3, _translate("KeyboardConfigDialog", "D"))
        self.TiltLeftComboBox.setItemText(4, _translate("KeyboardConfigDialog", "E"))
        self.TiltLeftComboBox.setItemText(5, _translate("KeyboardConfigDialog", "????????????"))
        self.TiltLeftComboBox.setItemText(6, _translate("KeyboardConfigDialog", "Shift"))
        self.TiltLeftComboBox.setItemText(7, _translate("KeyboardConfigDialog", "??????"))
        self.TiltLeftComboBox.setItemText(8, _translate("KeyboardConfigDialog", "??????"))
        self.TiltLeftComboBox.setItemText(9, _translate("KeyboardConfigDialog", "???????????? ????????"))
        self.TiltLeftComboBox.setItemText(10, _translate("KeyboardConfigDialog", "???????????? ??????????"))
        self.TiltRightComboBox.setItemText(0, _translate("KeyboardConfigDialog", "W"))
        self.TiltRightComboBox.setItemText(1, _translate("KeyboardConfigDialog", "A"))
        self.TiltRightComboBox.setItemText(2, _translate("KeyboardConfigDialog", "S"))
        self.TiltRightComboBox.setItemText(3, _translate("KeyboardConfigDialog", "D"))
        self.TiltRightComboBox.setItemText(4, _translate("KeyboardConfigDialog", "E"))
        self.TiltRightComboBox.setItemText(5, _translate("KeyboardConfigDialog", "????????????"))
        self.TiltRightComboBox.setItemText(6, _translate("KeyboardConfigDialog", "Shift"))
        self.TiltRightComboBox.setItemText(7, _translate("KeyboardConfigDialog", "??????"))
        self.TiltRightComboBox.setItemText(8, _translate("KeyboardConfigDialog", "??????"))
        self.TiltRightComboBox.setItemText(9, _translate("KeyboardConfigDialog", "???????????? ????????"))
        self.TiltRightComboBox.setItemText(10, _translate("KeyboardConfigDialog", "???????????? ??????????"))
        self.KeyboardGestureActionComboBox.setItemText(0, _translate("KeyboardConfigDialog", "W"))
        self.KeyboardGestureActionComboBox.setItemText(1, _translate("KeyboardConfigDialog", "A"))
        self.KeyboardGestureActionComboBox.setItemText(2, _translate("KeyboardConfigDialog", "S"))
        self.KeyboardGestureActionComboBox.setItemText(3, _translate("KeyboardConfigDialog", "D"))
        self.KeyboardGestureActionComboBox.setItemText(4, _translate("KeyboardConfigDialog", "E"))
        self.KeyboardGestureActionComboBox.setItemText(5, _translate("KeyboardConfigDialog", "????????????"))
        self.KeyboardGestureActionComboBox.setItemText(6, _translate("KeyboardConfigDialog", "Shift"))
        self.KeyboardGestureActionComboBox.setItemText(7, _translate("KeyboardConfigDialog", "??????"))
        self.KeyboardGestureActionComboBox.setItemText(8, _translate("KeyboardConfigDialog", "??????"))
        self.KeyboardGestureActionComboBox.setItemText(9, _translate("KeyboardConfigDialog", "???????????? ????????"))
        self.KeyboardGestureActionComboBox.setItemText(10, _translate("KeyboardConfigDialog", "???????????? ??????????"))

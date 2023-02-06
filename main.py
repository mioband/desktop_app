import sys
import json

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt6.QtCore import QThreadPool

from utils import Config, get_serial_ports

# from mio_app import Ui_MainWindow
from mio_app_new import Ui_MainWindow
from mio_app_mouse_config_dialog import Ui_MouseConfigDialog
from mio_app_keyboard_config_dialog import Ui_KeyboardConfigDialog

from mio_app_backend import Mio_API_get_data, Mio_API_control

import json
from constants import *


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.all_serial_ports = get_serial_ports()
        self.config = Config(PATH_TO_DEFAULT_CONFIG)  # Load config

        self.ui.UsbDeviceComportComboBox.clear()
        self.ui.UsbDeviceComportComboBox.addItems(self.all_serial_ports)
        self.fill_main_window()  # Fill main window according to config

        self.ui.LeftBandEnabled.toggled.connect(lambda: self.on_band_toggled("Left"))
        self.ui.LeftBandModeComboBox.currentIndexChanged.connect(self.on_band_mode_changed)
        self.ui.LeftBandConfigButton.clicked.connect(lambda: self.on_band_config_btn_clicked("Left"))
        self.ui.LeftBandConnectButton.clicked.connect(lambda: self.connect_to_band("Left"))

        self.ui.RightBandEnabled.toggled.connect(lambda: self.on_band_toggled("Right"))
        self.ui.RightBandModeComboBox.currentIndexChanged.connect(self.on_band_mode_changed)
        self.ui.RightBandConfigButton.clicked.connect(lambda: self.on_band_config_btn_clicked("Right"))
        self.ui.RightBandConnectButton.clicked.connect(lambda: self.connect_to_band("Right"))

        self.ui.LeftBandStatusIndicator.setStyleSheet("color: red;")
        self.ui.LeftBandStatusIndicator.setText('N/A')

        self.ui.RightBandStatusIndicator.setStyleSheet("color: red;")
        self.ui.RightBandStatusIndicator.setText('N/A')

        self.ui.UsbDeviceComportComboBox.currentIndexChanged.connect(self.on_comport_changed)

        self._working_with_arm = -1

        self.mouse_config_dialog = MouseConfigDialog(self)
        self.keyboard_config_dialog = KeyboardConfigDialog(self)

        # Initialize backend
        self.backend_controls = Mio_API_control()
        self.backend_controls.config = self.config
        self.backend = Mio_API_get_data(self.backend_controls)
        # self.backend.signals.usb_device_status.connect(self.on_usb_device_status_changed)
        # self.backend.signals.band_status.connect(self.on_band_status_changed)
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.threadpool.start(self.backend)

    def on_band_toggled(self, hand):
        if hand == "Left":
            if self.ui.LeftBandEnabled.isChecked():
                self.ui.LeftBandModeLabel.setEnabled(True)
                self.ui.LeftBandModeComboBox.setEnabled(True)
                self.ui.LeftBandConfigButton.setEnabled(True)
                self.config.left_band.enabled = True
                self.config.write(PATH_TO_DEFAULT_CONFIG)
                self.send_config_to_process()
            else:
                self.ui.LeftBandModeLabel.setDisabled(True)
                self.ui.LeftBandModeComboBox.setDisabled(True)
                self.ui.LeftBandConfigButton.setDisabled(True)
                self.config.left_band.enabled = False
                self.config.write(PATH_TO_DEFAULT_CONFIG)
                self.send_config_to_process()
        elif hand == "Right":
            if self.ui.RightBandEnabled.isChecked():
                self.ui.RightBandModeLabel.setEnabled(True)
                self.ui.RightBandModeComboBox.setEnabled(True)
                self.ui.RightBandConfigButton.setEnabled(True)
                self.config.right_band.enabled = True
                self.config.write(PATH_TO_DEFAULT_CONFIG)
                self.send_config_to_process()
            else:
                self.ui.RightBandModeLabel.setDisabled(True)
                self.ui.RightBandModeComboBox.setDisabled(True)
                self.ui.RightBandConfigButton.setDisabled(True)
                self.config.right_band.enabled = False
                self.config.write(PATH_TO_DEFAULT_CONFIG)
                self.send_config_to_process()

    def on_band_config_btn_clicked(self, hand):
        if hand == 'Left':
            self._working_with_arm = 0
            armband = self.config.left_band
        elif hand == 'Right':
            self._working_with_arm = 1
            armband = self.config.right_band
        if armband.mode == "mouse":
            mcd = self.mouse_config_dialog
            index = self.config.available_bindings.index(armband.bindings['gesture_1'])
            mcd.ui.MouseGestureActionComboBox.setCurrentIndex(index)
            mcd.exec()
        elif armband.mode == "hotkeys":
            kcd = self.keyboard_config_dialog
            config_names_to_ui_elements = {
                'tilt_forward': kcd.ui.TiltForwardComboBox,
                'tilt_backward': kcd.ui.TiltBackwardComboBox,
                'tilt_left': kcd.ui.TiltLeftComboBox,
                'tilt_right': kcd.ui.TiltRightComboBox,
                'gesture_1': kcd.ui.KeyboardGestureActionComboBox
            }
            config_binding_names_in_index_order = self.config.available_bindings
            for binding in config_names_to_ui_elements.keys():
                current_ui_element = config_names_to_ui_elements[binding]
                current_ui_element.setCurrentIndex(
                    config_binding_names_in_index_order.index(armband.bindings[binding]))
            kcd.exec()

    def on_band_mode_changed(self):
        idx_to_mode = {0: 'mouse', 1: 'hotkeys'}
        try:
            self.config.left_band.mode = idx_to_mode[self.ui.LeftBandModeComboBox.currentIndex()]
            self.config.right_band.mode = idx_to_mode[self.ui.RightBandModeComboBox.currentIndex()]
            for armband in [self.config.left_band, self.config.right_band]:
                if armband.mode == 'mouse':
                    armband.bindings = {'gesture_1': 'left_click', 'gesture_2': 'left_click'}
                elif armband.mode == 'hotkeys':
                    armband.bindings = {'tilt_forward': 'w', 'tilt_backward': 's', 'tilt_left': 'a', 'tilt_right': 'd',
                                        'gesture_1': 'left_click', 'gesture_2': 'shift'}
            self.config.write(PATH_TO_DEFAULT_CONFIG)
            self.send_config_to_process()
        except KeyError:
            print("Invalid mode selected")
            pass

    def on_comport_changed(self):
        serial_port = self.all_serial_ports[self.ui.UsbDeviceComportComboBox.currentIndex()]
        print(f'Comport was changed to {serial_port}')
        self.config.usb_device['serial_port'] = serial_port
        self.config.write(PATH_TO_DEFAULT_CONFIG)
        self.send_config_to_process()

    def on_usb_device_status_changed(self, status):
        if status:
            print('USB device status changed to True')
            self.ui.UsbDeviceStatusIndicator.setStyleSheet("color: green;")
            self.ui.UsbDeviceStatusIndicator.setText('OK')
        else:
            print('USB device status changed to False')
            self.ui.UsbDeviceStatusIndicator.setStyleSheet("color: red;")
            self.ui.UsbDeviceStatusIndicator.setText('N/A')

    def on_band_status_changed(self, status):
        if status['band'] == 'left':
            if status['status']:
                print('Left band status changed to True')
                self.ui.LeftBandStatusIndicator.setStyleSheet("color: green;")
                self.ui.LeftBandStatusIndicator.setText('OK')
            else:
                print('Left band status changed to False')
                self.ui.LeftBandStatusIndicator.setStyleSheet("color: red;")
                self.ui.LeftBandStatusIndicator.setText('N/A')
        elif status['band'] == 'right':
            if status['status']:
                print('Right band status changed to True')
                self.ui.RightBandStatusIndicator.setStyleSheet("color: green;")
                self.ui.RightBandStatusIndicator.setText('OK')
            else:
                print('Right band status changed to False')
                self.ui.RightBandStatusIndicator.setStyleSheet("color: red;")
                self.ui.RightBandStatusIndicator.setText('N/A')

    def fill_main_window(self):
        # Left
        self.ui.LeftBandNameLineEdit.setText(self.config.left_band.name)
        if self.config.left_band.enabled:
            self.ui.LeftBandEnabled.setChecked(True)
            self.ui.LeftBandModeLabel.setEnabled(True)
            self.ui.LeftBandModeComboBox.setEnabled(True)
            self.ui.LeftBandConfigButton.setEnabled(True)
        if self.config.left_band.mode == 'hotkeys':
            self.ui.LeftBandModeComboBox.setCurrentIndex(1)
        elif self.config.left_band.mode == 'mouse':
            self.ui.LeftBandModeComboBox.setCurrentIndex(0)
        # Right
        self.ui.RightBandNameLineEdit.setText(self.config.right_band.name)
        if self.config.right_band.enabled:
            self.ui.RightBandEnabled.setChecked(True)
            self.ui.RightBandModeLabel.setEnabled(True)
            self.ui.RightBandModeComboBox.setEnabled(True)
            self.ui.RightBandConfigButton.setEnabled(True)
        if self.config.right_band.mode == 'hotkeys':
            self.ui.RightBandModeComboBox.setCurrentIndex(1)
        elif self.config.right_band.mode == 'mouse':
            self.ui.RightBandModeComboBox.setCurrentIndex(0)
        try:
            self.ui.UsbDeviceComportComboBox.setCurrentIndex(
                self.all_serial_ports.index(self.config.usb_device['serial_port']))
        except:
            self.ui.UsbDeviceComportComboBox.setCurrentIndex(0)

    def send_config_to_process(self):
        self.backend.config = self.config
        # self.backend.config_changed = True
        print("PLACEHOLDER: SENDING CONFIG TO PROCESS")  # TODO

    def closeEvent(self, *args, **kwargs):
        self.backend.stop_requested = True
        self.backend_controls.stop_requested = True

    def connect_to_band(self, hand):
        if hand == "Left":
            band_name = self.ui.LeftBandNameLineEdit.text()
        elif hand == "Right":
            band_name = self.ui.RightBandNameLineEdit.text()
        self.backend.connect_to_band(band_name, hand)  # TODO


class MouseConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_MouseConfigDialog()
        self.ui.setupUi(self)
        self.ui.MouseGestureActionComboBox.clear()
        self.ui.MouseGestureActionComboBox.addItems(self.parent.config.available_bindings)
        self.ui.MouseConfigCancelButton.clicked.connect(self.close)
        self.ui.MouseConfigApplyButton.clicked.connect(self.apply)

    def apply(self):
        if self.parent._working_with_arm == 0:  # Left
            armband = self.parent.config.left_band
        elif self.parent._working_with_arm == 1:  # Right
            armband = self.parent.config.right_band
        else:
            armband = None
        armband.bindings['gesture_1'] = self.parent.config.available_bindings[
            self.ui.MouseGestureActionComboBox.currentIndex()]
        self.parent.config.write(PATH_TO_DEFAULT_CONFIG)
        self.parent.send_config_to_process()
        self.parent._working_with_arm = -1
        self.close()


class KeyboardConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_KeyboardConfigDialog()
        self.ui.setupUi(self)
        combo_boxes = [self.ui.TiltRightComboBox, self.ui.TiltLeftComboBox, self.ui.TiltForwardComboBox,
                       self.ui.TiltBackwardComboBox, self.ui.KeyboardGestureActionComboBox]
        for combo_box in combo_boxes:
            combo_box.clear()
            combo_box.addItems(self.parent.config.available_bindings)

        self.ui.KeyboardConfigCancelButton.clicked.connect(self.close)
        self.ui.KeyboardConfigApplyButton.clicked.connect(self.apply)

    def apply(self):
        config_names_to_ui_elements = {
            'tilt_forward': self.ui.TiltForwardComboBox,
            'tilt_backward': self.ui.TiltBackwardComboBox,
            'tilt_left': self.ui.TiltLeftComboBox,
            'tilt_right': self.ui.TiltRightComboBox,
            'gesture_1': self.ui.KeyboardGestureActionComboBox
        }
        if self.parent._working_with_arm == 0:  # Left
            armband = self.parent.config.left_band
        elif self.parent._working_with_arm == 1:  # Right
            armband = self.parent.config.right_band
        else:
            armband = None
        for config_gesture, ui_element in config_names_to_ui_elements.items():
            armband.bindings[config_gesture] = self.parent.config.available_bindings[ui_element.currentIndex()]
        self.parent.config.write(PATH_TO_DEFAULT_CONFIG)
        self.parent.send_config_to_process()
        self.parent._working_with_arm = -1
        self.close()


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = MainWindow()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())

import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt6.QtCore import QThreadPool

from mio_app import Ui_MainWindow
from mio_app_mouse_config_dialog import Ui_MouseConfigDialog
from mio_app_keyboard_config_dialog import Ui_KeyboardConfigDialog

from Mio_API_v02 import Mio_API
from Mio_API_v04 import Mio_API_get_data, Mio_API_control

import json

from constants import *


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mouse_config_dialog = MouseConfigDialog(self)
        self.keyboard_config_dialog = KeyboardConfigDialog(self)

        self.full_config = self.load_current_config(PATH_TO_DEFAULT_CONFIG)
        self._working_with_arm = -1

        self.ui.LeftBandEnabled.toggled.connect(self.on_left_band_toggled)
        self.ui.LeftBandModeComboBox.currentIndexChanged.connect(self.on_band_mode_changed)
        self.ui.LeftBandConfigButton.clicked.connect(self.on_left_band_config_btn_clicked)

        self.ui.RightBandEnabled.toggled.connect(self.on_right_band_toggled)
        self.ui.RightBandModeComboBox.currentIndexChanged.connect(self.on_band_mode_changed)
        self.ui.RightBandConfigButton.clicked.connect(self.on_right_band_config_btn_clicked)

        # self.worker = Mio_API()
        self.worker = Mio_API_control()
        self.worker_get_data = Mio_API_get_data(self.worker)
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.threadpool.start(self.worker_get_data)

    def on_left_band_toggled(self):
        if self.ui.LeftBandEnabled.isChecked():
            self.ui.LeftBandModeLabel.setEnabled(True)
            self.ui.LeftBandModeComboBox.setEnabled(True)
            self.ui.LeftBandConfigButton.setEnabled(True)
            self.full_config['armbands'][0]['enabled'] = True
            self.save_current_config()
            self.send_config_to_process()
        else:
            self.ui.LeftBandModeLabel.setDisabled(True)
            self.ui.LeftBandModeComboBox.setDisabled(True)
            self.ui.LeftBandConfigButton.setDisabled(True)
            self.full_config['armbands'][0]['enabled'] = False
            self.save_current_config()
            self.send_config_to_process()

    def on_left_band_config_btn_clicked(self):
        self._working_with_arm = 0
        if self.ui.LeftBandModeComboBox.currentIndex() == 0:
            mcd = self.mouse_config_dialog
            armband = self.full_config['armbands'][0]
            if armband['bindings']['gesture_1'] == 'left_click':
                mcd.ui.MouseGestureActionComboBox.setCurrentIndex(0)
            elif armband['bindings']['gesture_1'] == 'right_click':
                mcd.ui.MouseGestureActionComboBox.setCurrentIndex(1)
            mcd.exec()

        elif self.ui.LeftBandModeComboBox.currentIndex() == 1:
            kcd = self.keyboard_config_dialog
            config_names_to_ui_elements = {
                'tilt_forward': kcd.ui.TiltForwardComboBox,
                'tilt_backward': kcd.ui.TiltBackwardComboBox,
                'tilt_left': kcd.ui.TiltLeftComboBox,
                'tilt_right': kcd.ui.TiltRightComboBox,
                'gesture_1': kcd.ui.KeyboardGestureActionComboBox
            }
            config_binding_names_in_index_order = ['w', 'a', 's', 'd', 'e', 'space', 'shift', 'left_click',
                                                   'right_click', 'mousewheel_down', 'mousewheel_up']
            armband = self.full_config['armbands'][0]
            for binding in config_names_to_ui_elements.keys():
                current_ui_element = config_names_to_ui_elements[binding]
                current_ui_element.setCurrentIndex(
                    config_binding_names_in_index_order.index(armband['bindings'][binding]))
            kcd.exec()

    def on_right_band_toggled(self):
        if self.ui.RightBandEnabled.isChecked():
            self.ui.RightBandModeLabel.setEnabled(True)
            self.ui.RightBandModeComboBox.setEnabled(True)
            self.ui.RightBandConfigButton.setEnabled(True)
            self.full_config['armbands'][1]['enabled'] = True
            self.save_current_config()
            self.send_config_to_process()
        else:
            self.ui.RightBandModeLabel.setDisabled(True)
            self.ui.RightBandModeComboBox.setDisabled(True)
            self.ui.RightBandConfigButton.setDisabled(True)
            self.full_config['armbands'][1]['enabled'] = False
            self.save_current_config()
            self.send_config_to_process()

    def on_right_band_config_btn_clicked(self):
        self._working_with_arm = 1
        if self.ui.RightBandModeComboBox.currentIndex() == 0:
            mcd = self.mouse_config_dialog
            armband = self.full_config['armbands'][1]
            if armband['bindings']['gesture_1'] == 'left_click':
                mcd.ui.MouseGestureActionComboBox.setCurrentIndex(0)
            elif armband['bindings']['gesture_1'] == 'right_click':
                mcd.ui.MouseGestureActionComboBox.setCurrentIndex(1)
            mcd.exec()

        elif self.ui.RightBandModeComboBox.currentIndex() == 1:
            kcd = self.keyboard_config_dialog
            config_names_to_ui_elements = {
                'tilt_forward': kcd.ui.TiltForwardComboBox,
                'tilt_backward': kcd.ui.TiltBackwardComboBox,
                'tilt_left': kcd.ui.TiltLeftComboBox,
                'tilt_right': kcd.ui.TiltRightComboBox,
                'gesture_1': kcd.ui.KeyboardGestureActionComboBox
            }
            config_binding_names_in_index_order = ['w', 'a', 's', 'd', 'e', 'space', 'shift', 'left_click',
                                                   'right_click', 'mousewheel_down', 'mousewheel_up']
            armband = self.full_config['armbands'][1]
            for binding in config_names_to_ui_elements.keys():
                current_ui_element = config_names_to_ui_elements[binding]
                current_ui_element.setCurrentIndex(
                    config_binding_names_in_index_order.index(armband['bindings'][binding]))
            kcd.exec()

    def on_band_mode_changed(self):
        for (ui_element, armband) in zip([self.ui.LeftBandModeComboBox, self.ui.RightBandModeComboBox],
                                         self.full_config['armbands']):
            armband['mode'] = self.full_config['common_settings']['armband_modes'][ui_element.currentIndex()]
            if armband['mode'] == 'mouse':
                armband['bindings'] = {'gesture_1': 'left_click', 'gesture_2': 'left_click'}
            elif armband['mode'] == 'hotkeys':
                armband['bindings'] = {'tilt_forward': 'w', 'tilt_backward': 's', 'tilt_left': 'a', 'tilt_right': 'd',
                                       'gesture_1': 'left_click', 'gesture_2': 'shift'}
        self.save_current_config()
        self.send_config_to_process()

    def save_current_config(self):
        with open(PATH_TO_DEFAULT_CONFIG, 'w') as fp:
            json.dump(self.full_config, fp, indent=2)

    def load_current_config(self, path_to_default_config):
        with open(path_to_default_config) as json_file:
            config = json.load(json_file)
        for armband in config["armbands"]:
            if armband['arm'] == 'left':
                if armband['enabled']:
                    self.ui.LeftBandEnabled.setChecked(True)
                    self.ui.LeftBandModeLabel.setEnabled(True)
                    self.ui.LeftBandModeComboBox.setEnabled(True)
                    self.ui.LeftBandConfigButton.setEnabled(True)
                if armband['mode'] == 'hotkeys':
                    self.ui.LeftBandModeComboBox.setCurrentIndex(1)
                elif armband['mode'] == 'mouse':
                    self.ui.LeftBandModeComboBox.setCurrentIndex(0)
            elif armband['arm'] == 'right':
                if armband['enabled']:
                    self.ui.RightBandEnabled.setChecked(True)
                    self.ui.RightBandModeLabel.setEnabled(True)
                    self.ui.RightBandModeComboBox.setEnabled(True)
                    self.ui.RightBandConfigButton.setEnabled(True)
                if armband['mode'] == 'hotkeys':
                    self.ui.RightBandModeComboBox.setCurrentIndex(1)
                elif armband['mode'] == 'mouse':
                    self.ui.RightBandModeComboBox.setCurrentIndex(0)
        return config

    def send_config_to_process(self):
        self.worker.config_changed = True

    def closeEvent(self, *args, **kwargs):
        self.worker.stop_requested = True


class MouseConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MouseConfigDialog()
        self.ui.setupUi(self)

        self.ui.MouseConfigCancelButton.clicked.connect(self.close)
        self.ui.MouseConfigApplyButton.clicked.connect(self.apply)

    def apply(self):
        self.parent().full_config['armbands'][self.parent()._working_with_arm]['bindings']['gesture_1'] = \
            ['left_click', 'right_click'][self.ui.MouseGestureActionComboBox.currentIndex()]
        self.parent().save_current_config()
        self.parent().send_config_to_process()
        self.close()


class KeyboardConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_KeyboardConfigDialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

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
        config_binding_names_in_index_order = ['w', 'a', 's', 'd', 'e', 'space', 'shift', 'left_click',
                                               'right_click', 'mousewheel_down', 'mousewheel_up']
        armband = self.parent().full_config['armbands'][self.parent()._working_with_arm]
        for config_gesture in config_names_to_ui_elements.keys():
            ui_element = config_names_to_ui_elements[config_gesture]
            armband['bindings'][config_gesture] = config_binding_names_in_index_order[ui_element.currentIndex()]
        self.parent().full_config['armbands'][self.parent()._working_with_arm] = armband
        self.parent().save_current_config()
        self.parent().send_config_to_process()
        self.close()


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = MainWindow()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())

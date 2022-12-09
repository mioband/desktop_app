import json
import sys
import time
from threading import Thread

from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal
from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as Controller2
from pynput.keyboard import Key
import serial

from constants import SERIAL_PORT, PATH_TO_DEFAULT_CONFIG
from win32api import GetSystemMetrics

MAX_MOUSE_SPEED = 40
WIDTH_INCREASE = GetSystemMetrics(0) / GetSystemMetrics(1)
HEIGHT_INCREASE = 1.5
DIFF_INCREASE = 1
XY_LIMIT = 3


class Mio_API_control(Thread):
    def __init__(self):
        super(Mio_API_control, self).__init__()
        self.s = False
        self.duration = 0.01
        self.y_speed = 0
        self.x_speed = 0
        self.mouse = Controller()
        self.keyboard = Controller2()
        self.button_mouse_headers = {'left_click': Button.left, 'right_click': Button.right}
        self.button_keyboard_headers = {'w': 'w', 'a': 'a', 's': 's', 'd': 'd', 'e': 'e', 'shift': Key.shift,
                                        'ctrl': Key.ctrl, 'space': Key.space}
        self.pre_button_states = {'w': False, 'a': False, 's': False, 'd': False, 'e': False, 'shift': False,
                                  'ctrl': False, 'space': False, 'left_click': False, 'right_click': False}
        self.pre_button_states = {'w': False, 'a': False, 's': False, 'd': False, 'e': False, 'shift': False,
                                  'ctrl': False, 'space': False, 'left_click': False, 'right_click': False}
        self.json_data_with_config = dict()
        self.my_json_config = dict()
        self.stop_requested = False

    # @pyqtSlot()
    def run(self):
        while not self.stop_requested:
            for band_id in self.my_json_config:
                self.controller_band_with_config(band_id)

            self.mouse.move(self.x_speed, self.y_speed)
            # self.button_check(self.s, 'left_click')
            time.sleep(self.duration)
        sys.exit()  # ?

    def rotation_by_speed(self, x, y):
        if (x != 0) or (y != 0):
            self.duration = 1 / (MAX_MOUSE_SPEED * max(abs(x), abs(y)))
            if x == 0:
                self.x_speed = 0
                self.y_speed = y / abs(y)
            elif y == 0:
                self.x_speed = x / abs(x)
                self.y_speed = 0
            else:
                self.x_speed = x / min(abs(x), abs(y))
                self.y_speed = y / min(abs(x), abs(y))

        else:
            self.duration = 0.1
            self.x_speed = 0
            self.y_speed = 0

        self.x_speed *= abs(x) * DIFF_INCREASE * WIDTH_INCREASE
        self.y_speed *= abs(y) * DIFF_INCREASE * HEIGHT_INCREASE

    def controller_band_with_config(self, band_id):
        if self.my_json_config[band_id]["enabled"]:
            msg_l0 = self.json_data_with_config[band_id]
            if self.my_json_config[band_id]["mode"] == "mouse":
                # print(msg_l0)
                rotation_x = msg_l0['x'] if abs(msg_l0['x']) > 2 else 0
                rotation_y = msg_l0['y'] if abs(msg_l0['y']) > 2 else 0
                self.rotation_by_speed(rotation_x, rotation_y)
                if msg_l0['s'] == 1:
                    self.press_button(self.my_json_config[band_id]["bindings"]["gesture_1"],
                                      self.my_json_config[band_id]["mode"])
                else:
                    self.release_button(self.my_json_config[band_id]["bindings"]["gesture_1"],
                                        self.my_json_config[band_id]["mode"])
            elif self.my_json_config[band_id]["mode"] == "hotkeys":
                if msg_l0['x'] > XY_LIMIT:  # BAND TILTED RIGHT
                    self.release_button(self.my_json_config[band_id]["bindings"]["tilt_left"],
                                        self.my_json_config[band_id]["mode"])
                    self.press_button(self.my_json_config[band_id]["bindings"]["tilt_right"],
                                      self.my_json_config[band_id]["mode"])
                elif msg_l0['x'] < -XY_LIMIT:  # BAND TILTED LEFT
                    self.release_button(self.my_json_config[band_id]["bindings"]["tilt_right"],
                                        self.my_json_config[band_id]["mode"])
                    self.press_button(self.my_json_config[band_id]["bindings"]["tilt_left"],
                                      self.my_json_config[band_id]["mode"])
                else:  # BAND IS STRAIGHT (NOR FORWARD NOR BACKWARD)
                    self.release_button(self.my_json_config[band_id]["bindings"]["tilt_right"],
                                        self.my_json_config[band_id]["mode"])
                    self.release_button(self.my_json_config[band_id]["bindings"]["tilt_left"],
                                        self.my_json_config[band_id]["mode"])
                if msg_l0['y'] > XY_LIMIT:  # BAND TILTED FORWARD
                    self.release_button(self.my_json_config[band_id]["bindings"]["tilt_backward"],
                                        self.my_json_config[band_id]["mode"])
                    self.press_button(self.my_json_config[band_id]["bindings"]["tilt_forward"],
                                      self.my_json_config[band_id]["mode"])
                elif msg_l0['y'] < -XY_LIMIT:  # BAND TILTED BACKWARD
                    self.release_button(self.my_json_config[band_id]["bindings"]["tilt_forward"],
                                        self.my_json_config[band_id]["mode"])
                    self.press_button(self.my_json_config[band_id]["bindings"]["tilt_backward"],
                                      self.my_json_config[band_id]["mode"])
                else:  # BAND IS STRAIGHT (NOR FORWARD NOR BACKWARD)
                    self.release_button(self.my_json_config[band_id]["bindings"]["tilt_forward"],
                                        self.my_json_config[band_id]["mode"])
                    self.release_button(self.my_json_config[band_id]["bindings"]["tilt_backward"],
                                        self.my_json_config[band_id]["mode"])
                if msg_l0['s'] == 1:
                    self.press_button(self.my_json_config[band_id]["bindings"]["gesture_1"],
                                      self.my_json_config[band_id]["mode"])
                else:
                    self.release_button(self.my_json_config[band_id]["bindings"]["gesture_1"],
                                        self.my_json_config[band_id]["mode"])

    def release_button(self, button, mode):
        if mode == "mouse":
            if self.pre_button_states[button]:
                self.mouse.release(self.button_mouse_headers[button])
                print(f'{button} released')
        elif mode == "hotkeys":
            try:
                if self.pre_button_states[button]:
                    self.keyboard.release(self.button_keyboard_headers[button])
                    print(f'{button} released')
            except:
                if self.pre_button_states[button]:
                    self.mouse.release(self.button_mouse_headers[button])
                    print(f'{button} released')
        self.pre_button_states[button] = False

    def press_button(self, button, mode):
        if mode == "mouse":
            if not self.pre_button_states[button]:
                self.mouse.press(self.button_mouse_headers[button])
                print(f'{button} pressed')
        elif mode == "hotkeys":
            try:
                if not self.pre_button_states[button]:
                    self.keyboard.press(self.button_keyboard_headers[button])
                print(f'{button} pressed')
            except:
                if not self.pre_button_states[button]:
                    self.mouse.press(self.button_mouse_headers[button])
                print(f'{button} pressed')
        self.pre_button_states[button] = True


class MioAPISignals(QObject):
    band_status = pyqtSignal(object)
    usb_device_status = pyqtSignal(object)


class Mio_API_get_data(QRunnable):
    def __init__(self, band_control=None):
        super(Mio_API_get_data, self).__init__()
        self.decode_message = {'x': 0, 'y': 0, 's': 0}
        self.config_changed = False
        self.stop_requested = False
        self.band_control = band_control
        self.json_data_with_config = dict()
        self.my_json_config = dict()
        self.signals = MioAPISignals()
        self.ser = serial.Serial()
        self.init_json()
        self.ser.port = self.serial_port
        self.ser.baudrate = 115200
        self.ser.timeout = 2
        self.band_control.start()  # TODO
        self.last_right_emit = time.time()
        self.last_left_emit = time.time()

    def set_band_json_data(self, json_d):
        self.band_control.json_data_with_config = json_d

    def set_band_my_json_config(self, json_d):
        self.band_control.my_json_config = json_d

    @pyqtSlot()
    def run(self):
        self.signals.band_status.emit({'band': 'right', 'status': False})
        self.signals.band_status.emit({'band': 'left', 'status': False})
        self.signals.usb_device_status.emit(False)
        self.open_serial()
        # self.test_data()
        sys.exit()

    def emit_detect(self, band_id):
        if self.my_json_config[band_id]["arm"] == "right":
            self.signals.band_status.emit({'band': 'right', 'status': True})
            self.last_right_emit = time.time()
        elif self.my_json_config[band_id]["arm"] == "left":
            self.signals.band_status.emit({'band': 'left', 'status': True})
            self.last_left_emit = time.time()

    def emit_close(self):
        time_now = time.time()
        if (time_now - self.last_right_emit) > 3:
            self.signals.band_status.emit({'band': 'right', 'status': False})
        if (time_now - self.last_left_emit) > 3:
            self.signals.band_status.emit({'band': 'left', 'status': False})

    def string_to_json(self, line):
        decode_line = line.decode()
        s_list = decode_line.split(',')[:-1]
        i_list = []
        for i in s_list:
            try:
                i_list.append(int(i))
            except:
                pass
        if i_list[0] == 48 or i_list[0] == 144 or i_list[0] == 80:
            band_n = 2
            if i_list[0] == 48:
                self.decode_message['x'] = i_list[1]
                self.decode_message['y'] = i_list[2]
            elif i_list[0] == 144:
                print(i_list)
                self.decode_message['s'] = 1 if i_list[1] > 3 else 0
            elif i_list[0] == 80:
                print(f'Заряд:{i_list[1]}%')
        else:
            band_n = 3
            if i_list[0] == 49:
                self.decode_message['x'] = i_list[1]
                self.decode_message['y'] = i_list[2]
            elif i_list[0] == 145:
                print(i_list)
                self.decode_message['s'] = 1 if i_list[1] > 3 else 0
            elif i_list[0] == 81:
                print(f'Заряд:{i_list[1]}%')

        return self.decode_message, band_n

    def open_serial(self):
        while not self.stop_requested:
            try:
                self.check_config()
                print('check conf')
                print(f'Trying to open port {self.ser.port}')
                self.ser.open()
                self.signals.usb_device_status.emit(True)
                line = self.ser.readline()
                print(f'Data: {line}')
                while not self.stop_requested:
                    self.check_config()
                    line = self.ser.readline()
                    print(f'Data: {line}')
                    try:
                        json_message, band_id = self.string_to_json(line)
                        self.json_data_with_config[band_id] = json_message
                        self.set_band_json_data(self.json_data_with_config)
                    except:
                        for armband in self.armbands:
                            self.json_data_with_config[armband["id"]] = {'x': 0, 'y': 0, 's': 0}
                            self.set_band_json_data(self.json_data_with_config)
                        self.emit_close()
            except:
                time.sleep(3)
                self.ser.close()

    def check_config(self):
        if self.config_changed:  # Теперь проверка на то был ли изменен конфиг
            print('Config changed, obtaining config again')
            self.init_json()
            self.config_changed = False  # ОБЯЗАТЕЛЬНО ПЕРЕКЛЮЧИТЬ ОБРАТНО!
            print(self.my_json_config)

    def init_json(self):
        with open(PATH_TO_DEFAULT_CONFIG, mode='r') as f:
            self.json_config = json.load(f)
        # print(self.json_config)
        self.armbands = self.json_config['armbands']
        for armband in self.armbands:
            self.json_data_with_config[armband["id"]] = {'x': 0, 'y': 0, 's': 0}
            self.set_band_json_data(self.json_data_with_config)
            self.my_json_config[armband["id"]] = armband
        self.set_band_my_json_config(self.my_json_config)
        self.serial_port = self.json_config["usb_device"]["serial_port"]
        self.ser.port = self.serial_port


if __name__ == '__main__':
    mio_control = Mio_API_control()
    get_data = Mio_API_get_data(mio_control)
    # get_data.start()
    # mio_control.start()

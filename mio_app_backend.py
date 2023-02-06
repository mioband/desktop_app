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

from utils import Config

MAX_MOUSE_SPEED = 40
WIDTH_INCREASE = 1.5
HEIGHT_INCREASE = 1.5
DIFF_INCREASE = 0.01
XY_LIMIT = 500


class Mio_API_control(Thread):
    def __init__(self):
        super().__init__()
        self.duration = 0.01
        self.y_speed = 0
        self.x_speed = 0
        self.mouse = Controller()
        self.keyboard = Controller2()
        # self.button_mouse_headers = {'left_click': Button.left, 'right_click': Button.right}
        self.button_headers = {'w': 'w', 'a': 'a', 's': 's', 'd': 'd', 'e': 'e', 'shift': Key.shift,
                                        'ctrl': Key.ctrl, 'space': Key.space, 'z': 'z', 'x': 'x', 'c': 'c',
                                        'left_click': Button.left, 'right_click': Button.right}
        self.button_headers = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i',
                               'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r',
                               's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z',
                               'shift': Key.shift, 'ctrl': Key.ctrl, 'space': Key.space,
                               'left_click': Button.left, 'right_click': Button.right,
                               }
        self.pre_button_states = {'w': False, 'a': False, 's': False, 'd': False, 'e': False, 'shift': False,
                                  'ctrl': False, 'space': False, 'left_click': False, 'right_click': False,
                                  'z': False, 'x': False, 'c': False}
        self.config = Config("config/config.json")
        self.stop_requested = False

    def run(self):
        while not self.stop_requested:
            self.controller_bands(self.config.left_band)
            self.controller_bands(self.config.right_band)
            # print(self.x_speed, self.y_speed)
            self.mouse.move(self.x_speed, self.y_speed)
            # self.button_check(self.s, 'left_click')
            time.sleep(self.duration)
        sys.exit()

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

    def controller_bands(self, band_side):
        if band_side.enabled:
            if band_side.mode == "mouse":
                rotation_x = band_side.message['x'] if abs(band_side.message['x']) > 200 else 0
                rotation_y = band_side.message['y'] if abs(band_side.message['y']) > 200 else 0
                self.rotation_by_speed(rotation_x, rotation_y)
                if band_side.message['s'] == 1:
                    self.press_button(band_side.bindings['gesture_1'], band_side.mode)
                else:
                    self.release_button(band_side.bindings['gesture_1'], band_side.mode)
            if band_side.mode == "hotkeys":
                if band_side.message['x'] > XY_LIMIT:# BAND TILTED RIGHT
                    self.release_button(band_side.bindings['tilt_left'], band_side.mode)
                    self.press_button(band_side.bindings['tilt_right'], band_side.mode)
                elif band_side.message['x'] < -XY_LIMIT: # BAND TILTED LEFT
                    self.release_button(band_side.bindings['tilt_right'], band_side.mode)
                    self.press_button(band_side.bindings['tilt_left'], band_side.mode)
                else:  # BAND IS STRAIGHT (NOR FORWARD NOR BACKWARD)
                    self.release_button(band_side.bindings['tilt_right'], band_side.mode)
                    self.release_button(band_side.bindings['tilt_left'], band_side.mode)
                if band_side.message['y'] > XY_LIMIT:# BAND TILTED RIGHT
                    self.release_button(band_side.bindings['tilt_backward'], band_side.mode)
                    self.press_button(band_side.bindings['tilt_forward'], band_side.mode)
                elif band_side.message['y'] < -XY_LIMIT: # BAND TILTED LEFT
                    self.release_button(band_side.bindings['tilt_forward'], band_side.mode)
                    self.press_button(band_side.bindings['tilt_backward'], band_side.mode)
                else:  # BAND IS STRAIGHT (NOR FORWARD NOR BACKWARD)
                    self.release_button(band_side.bindings['tilt_forward'], band_side.mode)
                    self.release_button(band_side.bindings['tilt_backward'], band_side.mode)

    def release_button(self, button, mode):
        if mode == "mouse":
            if self.pre_button_states[button]:
                self.mouse.release(self.button_headers[button])
                print(f'{button} released')
        elif mode == "hotkeys":
            if self.pre_button_states[button]:
                self.keyboard.release(self.button_headers[button])
                print(f'{button} released')

        self.pre_button_states[button] = False

    def press_button(self, button, mode):
        if mode == "mouse":
            if self.pre_button_states[button]:
                self.mouse.press(self.button_headers[button])
                print(f'{button} released')
        elif mode == "hotkeys":
            if self.pre_button_states[button]:
                self.keyboard.press(self.button_headers[button])
                print(f'{button} released')
        self.pre_button_states[button] = True


class MioAPISignals(QObject):
    band_status = pyqtSignal(dict)  # Сигнал о статусе USB устройства, отправляется при открытии или закрытии порта
    usb_device_status = pyqtSignal(bool)  # Сигнал о статусе браслета, отправляется при подключении или отключении
    connect_status = pyqtSignal(bool)  # Сигнал об успешности или неуспешности подключения браслета к ответке
    battery_percent = pyqtSignal(int)  # Сигнал о заряде аккумулятора в процентах, отправляется значение


class Mio_API_get_data(QRunnable):
    def __init__(self, band_control=None):
        super(Mio_API_get_data, self).__init__()
        self.config_changed = False
        self.stop_requested = False
        self.band_control = band_control
        self.signals = MioAPISignals()
        self.ser = serial.Serial()
        self.ser.port = self.band_control.config.usb_device['serial_port']
        self.ser.baudrate = 115200
        self.ser.timeout = 2
        self.band_control.start()
        self.last_right_emit = time.time()
        self.last_left_emit = time.time()
    @pyqtSlot()
    def run(self):
        self.signals.band_status.emit({'band': 'right', 'status': False})
        self.signals.band_status.emit({'band': 'left', 'status': False})
        self.signals.usb_device_status.emit(False)
        self.open_serial()
        # self.test_data()
        sys.exit()

    def open_serial(self):
        while not self.stop_requested:
            try:
                self.ser.port = self.band_control.config.usb_device['serial_port']
                print('check conf')
                print(f'Trying to open port {self.ser.port}')
                self.ser.open()
                print('Port opened')
                # self.signals.usb_device_status.emit(True)
                line = self.ser.readline()
                print(f'Data: {line}')
                while not self.stop_requested:
                    # self.check_config()
                    self.ser.port = self.band_control.config.usb_device['serial_port']
                    line = self.ser.readline()
                    print(f'Data: {line}')
                    try:
                        self.serial_msg_read(line)
                        print(self.band_control.config.right_band.message)
                        # self.json_data_with_config[str(band_id)] = json_message  # TODO
                        # self.set_band_json_data(self.json_data_with_config)
                    except:
                        self.emit_close()
            except:
                time.sleep(3)
                self.ser.close()

    def check_config(self):
        if self.config_changed:  # Теперь проверка на то был ли изменен конфиг
            print('Config changed, obtaining config again')
            self.band_control.config.read("config/config.json")
            self.ser.port = self.band_control.config.usb_device['serial_port']
            self.config_changed = False  # ОБЯЗАТЕЛЬНО ПЕРЕКЛЮЧИТЬ ОБРАТНО!

    def serial_msg_read(self, line):
        decode_line = line.decode()
        s_list = decode_line.split(',')[:-1]
        i_list = []
        for i in s_list:
            try:
                i_list.append(int(i))
            except:
                pass
        if i_list[0] == 48 or i_list[0] == 144 or i_list[0] == 80:
            band_n = 0
            if self.band_control.config.left_band.id == band_n:
                if i_list[0] == 48:
                    self.band_control.config.left_band.message['y'] = i_list[1]
                    self.band_control.config.left_band.message['x'] = i_list[2]
                elif i_list[0] == 144:
                    print(i_list)
                    self.band_control.config.left_band.message['s'] =\
                        1 if i_list[1] > 3 else 0
                elif i_list[0] == 80:
                    self.band_control.config.left_band.power = i_list[1]
                    print(f'Заряд:{i_list[1]}%')
                decode_message = \
                    self.band_control.config.left_band.message
            else:
                if i_list[0] == 48:
                    self.band_control.config.right_band.message['y'] = i_list[1]
                    self.band_control.config.right_band.message['x'] = i_list[2]
                elif i_list[0] == 144:
                    print(i_list)
                    self.band_control.config.right_band.message['s'] =\
                        1 if i_list[1] > 3 else 0
                elif i_list[0] == 80:
                    self.band_control.config.right_band.power = i_list[1]
                    print(f'Заряд:{i_list[1]}%')
                decode_message = \
                    self.band_control.config.right_band.message
        else:
            band_n = 1
            if self.band_control.config.left_band.id == band_n:
                if i_list[0] == 49:
                    self.band_control.config.left_band.message['y'] = i_list[1]
                    self.band_control.config.left_band.message['x'] = i_list[2]
                elif i_list[0] == 145:
                    print(i_list)
                    self.band_control.config.left_band.message['s'] =\
                        1 if i_list[1] > 3 else 0
                elif i_list[0] == 81:
                    self.band_control.config.left_band.power = i_list[1]
                    print(f'Заряд:{i_list[1]}%')
                decode_message = \
                    self.band_control.config.left_band.message
            else:
                if i_list[0] == 49:
                    self.band_control.config.right_band.message['y'] = i_list[1]
                    self.band_control.config.right_band.message['x'] = i_list[2]
                elif i_list[0] == 145:
                    print(i_list)
                    self.band_control.config.right_band.message['s'] =\
                        1 if i_list[1] > 3 else 0
                elif i_list[0] == 81:
                    self.band_control.config.right_band.power = i_list[1]
                    print(f'Заряд:{i_list[1]}%')
                decode_message = \
                    self.band_control.config.right_band.message
        return decode_message, band_n

    def connect_to_band(self, band_name, hand):
        cmd = bytearray(('~' + 'G' + band_name).encode('utf-8'))
        self.ser.write(cmd)
        tmp = ''
        while tmp != b'GOK\r\n':
            tmp = self.ser.readline()
        if hand == 'right':
            band_id = 0
            self.band_control.config.right_band.id = band_id
        elif hand == 'left':
            band_id = 1
            self.band_control.config.left_band.id = band_id
        self.band_control.config.write()

    def emit_close(self):
        time_now = time.time()
        if (time_now - self.last_right_emit) > 3:
            self.signals.band_status.emit({'band': 'right', 'status': False})
        if (time_now - self.last_left_emit) > 3:
            self.signals.band_status.emit({'band': 'left', 'status': False})

if __name__ == '__main__':
    mio_control = Mio_API_control()
    get_data = Mio_API_get_data(mio_control)
    get_data.start()
    time.sleep(3)
    # get_data.connect_to_band('Bracelet_2', '')






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
        # self.button_headers = {'w': 'w', 'a': 'a', 's': 's', 'd': 'd', 'e': 'e', 'shift': Key.shift,
        #                                 'ctrl': Key.ctrl, 'space': Key.space, 'z': 'z', 'x': 'x', 'c': 'c',
        #                                 'left_click': Button.left, 'right_click': Button.right}
        self.button_headers = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i',
                               'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r',
                               's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z',
                               'shift': Key.shift, 'ctrl': Key.ctrl, 'space': Key.space,
                               'left_click': Button.left, 'right_click': Button.right,
                               }
        self.pre_button_states = {k: False for k in self.button_headers}
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
                if band_side.message['x'] > XY_LIMIT:  # BAND TILTED RIGHT
                    self.release_button(band_side.bindings['tilt_left'], band_side.mode)
                    self.press_button(band_side.bindings['tilt_right'], band_side.mode)
                elif band_side.message['x'] < -XY_LIMIT:  # BAND TILTED LEFT
                    self.release_button(band_side.bindings['tilt_right'], band_side.mode)
                    self.press_button(band_side.bindings['tilt_left'], band_side.mode)
                else:  # BAND IS STRAIGHT (NOR FORWARD NOR BACKWARD)
                    self.release_button(band_side.bindings['tilt_right'], band_side.mode)
                    self.release_button(band_side.bindings['tilt_left'], band_side.mode)
                if band_side.message['y'] > XY_LIMIT:  # BAND TILTED RIGHT
                    self.release_button(band_side.bindings['tilt_backward'], band_side.mode)
                    self.press_button(band_side.bindings['tilt_forward'], band_side.mode)
                elif band_side.message['y'] < -XY_LIMIT:  # BAND TILTED LEFT
                    self.release_button(band_side.bindings['tilt_forward'], band_side.mode)
                    self.press_button(band_side.bindings['tilt_backward'], band_side.mode)
                else:  # BAND IS STRAIGHT (NOR FORWARD NOR BACKWARD)
                    self.release_button(band_side.bindings['tilt_forward'], band_side.mode)
                    self.release_button(band_side.bindings['tilt_backward'], band_side.mode)
                if band_side.message['s'] == 1:
                    self.press_button(band_side.bindings['gesture_1'], band_side.mode)
                else:
                    self.release_button(band_side.bindings['gesture_1'], band_side.mode)

    def release_button(self, button, mode):
        if mode == "mouse":
            if self.pre_button_states[button]:
                try:
                    self.mouse.release(self.button_headers[button])
                except:
                    self.keyboard.release(self.button_headers[button])
                print(f'{button} released')
        elif mode == "hotkeys":
            if self.pre_button_states[button]:
                try:
                    self.keyboard.release(self.button_headers[button])
                except:
                    self.mouse.release(self.button_headers[button])
                print(f'{button} released')

        self.pre_button_states[button] = False

    def press_button(self, button, mode):
        if mode == "mouse":
            if not self.pre_button_states[button]:
                try:
                    self.mouse.press(self.button_headers[button])
                except:
                    self.keyboard.press(self.button_headers[button])
                print(f'{button} pressed')
        elif mode == "hotkeys":
            if not self.pre_button_states[button]:
                try:
                    self.mouse.press(self.button_headers[button])
                except:
                    self.keyboard.press(self.button_headers[button])
                print(f'{button} pressed')
        self.pre_button_states[button] = True


class MioAPISignals(QObject):
    band_status = pyqtSignal(dict)  # Сигнал о статусе USB устройства, отправляется при открытии или закрытии порта
    usb_device_status = pyqtSignal(bool)  # Сигнал о статусе браслета, отправляется при подключении или отключении
    connect_status = pyqtSignal(bool)  # Сигнал об успешности или неуспешности подключения браслета к ответке
    battery_percent = pyqtSignal(dict)  # Сигнал о заряде аккумулятора в процентах, отправляется значение


class Mio_API_get_data(QRunnable):
# class Mio_API_get_data(Thread):
    def __init__(self, band_control=None):
        super(Mio_API_get_data, self).__init__()
        self.need_write = False
        self.emit_time = int(time.time())
        self.config_changed = False
        self.stop_requested = False
        self.band_control = band_control
        self.signals = MioAPISignals()
        self.ser = serial.Serial()
        self.ser.port = self.band_control.config.usb_device['serial_port']
        self.ser.baudrate = 115200
        self.ser.timeout = 2
        self.band_control.start()
        self.last_right_emit = 0
        self.last_left_emit = 0

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
                # self.signals.usb_device_status.emit(False)
                print(f'Trying to open port {self.ser.port}')
                self.ser.open()
                print('Port opened')
                self.signals.usb_device_status.emit(True)
                line = self.ser.readline()
                print(f'Data: {line}')
                while not self.stop_requested:
                    # self.check_config()
                    self.ser.port = self.band_control.config.usb_device['serial_port']
                    if self.need_write:
                        self.ser.write(self.cmd)
                        tmp = ''
                        while tmp != b'GOK\r\n':
                            tmp = self.ser.readline()
                        self.need_write = False
                    line = self.ser.readline()
                    print(f'Data: {line}')
                    try:
                        self.serial_msg_read(line)
                        # print(self.band_control.config.right_band.message)
                        # self.json_data_with_config[str(band_id)] = json_message  # TODOssdddwwwwwwwdwdwawww
                        # self.set_band_json_data(self.json_data_with_config)
                        self.emit_close()
                    except:
                        print('message except')
                        self.emit_close()
            except:
                print('port except')
                self.emit_close()
                time.sleep(3)
                self.signals.usb_device_status.emit(False)
                self.ser.close()

    # def check_config(self):
    #     if self.config_changed:  # Теперь проверка на то был ли изменен конфиг
    #         print('Config changed, obtaining config again')
    #         self.band_control.config.read("config/config.json")
    #         self.ser.port = self.band_control.config.usb_device['serial_port']
    #         self.config_changed = False  # ОБЯЗАТЕЛЬНО ПЕРЕКЛЮЧИТЬ ОБРАТНО!

    def serial_msg_read(self, line):
        decode_line = line.decode()
        s_list = decode_line.split(',')[:-1]
        i_list = []
        for i in s_list:
            try:
                i_list.append(int(i))
            except:
                pass
        if i_list[1] == 0:
            self.last_left_emit = time.time()
            if i_list[0] == 48:
                self.band_control.config.left_band.message['y'] = i_list[2]
                self.band_control.config.left_band.message['x'] = i_list[3]
            elif i_list[0] == 144:
                print(line)
                print(i_list)
                print(self.band_control.config.left_band.message['s'])
                print(i_list[4])
                self.band_control.config.left_band.message['s'] = i_list[4]
            elif i_list[0] == 80:
                self.band_control.config.left_band.power = i_list[2]
                print(f'Заряд:{i_list[2]}%')

        else:
            self.last_right_emit = time.time()
            if i_list[0] == 48:
                self.band_control.config.right_band.message['y'] = i_list[2]
                self.band_control.config.right_band.message['x'] = i_list[3]
            elif i_list[0] == 144:
                print(i_list)
                print(i_list[4])
                print(self.band_control.config.right_band.message['s'])
                self.band_control.config.right_band.message['s'] = i_list[4]
            elif i_list[0] == 80:
                self.band_control.config.right_band.power = i_list[2]
                print(f'Заряд:{i_list[2]}%')

    def connect_to_band(self, band_name, hand):
        self.cmd = bytearray(('~' + 'G' + band_name + '$' + hand + '\n').encode('utf-8'))
        print(f'Connecting to band {band_name} on hand {hand}:')
        # print(self.cmd)
        self.need_write = True

    def emit_close(self):
        time_now = time.time()
        if not int(time.time()) % 3 and self.emit_time != int(time.time()):
            self.emit_time = int(time.time())
            if (time_now - self.last_right_emit) > 3:
                self.signals.band_status.emit({'band': 'right', 'status': False})
            else:
                self.signals.band_status.emit({'band': 'right', 'status': True})
            if (time_now - self.last_left_emit) > 3:
                print('left status False')
                self.signals.band_status.emit({'band': 'left', 'status': False})
            else:
                print('left status True')
                self.signals.band_status.emit({'band': 'left', 'status': True})


if __name__ == '__main__':
    mio_control = Mio_API_control()
    get_data = Mio_API_get_data(mio_control)
    # print(get_data.band_control.config)
    get_data.start()
    # time.sleep(3)
    # get_data.connect_to_band('LARS_Bracelet', 'L')

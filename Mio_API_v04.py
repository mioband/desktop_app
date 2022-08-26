import json
import sys
import time
from threading import Thread

from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal
from pynput.mouse import Button, Controller
import serial

from constants import SERIAL_PORT, PATH_TO_DEFAULT_CONFIG

MAX_MOUSE_SPEED = 50


class Mio_API_control(Thread):
    def __init__(self):
        super(Mio_API_control, self).__init__()
        self.s = False
        self.duration = 1
        self.y_speed = 0
        self.x_speed = 0
        self.mouse = Controller()
        self.button_mouse_headers = {'left_click': Button.left, 'right_click': Button.right}
        self.button_states = {'left_click': False, 'right_click': False}
        self.pre_button_states = {'left_click': False, 'right_click': False}
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
        sys.exit()#?

    # def button_check(self, s, button_name):
    #     if s:
    #         if not self.pre_button_states[button_name]:
    #             self.mouse.press(self.button_mouse_headers[button_name])
    #             self.pre_button_states[button_name] = True
    #     else:
    #         if self.pre_button_states[button_name]:
    #             self.mouse.release(self.button_mouse_headers[button_name])
    #             self.pre_button_states[button_name] = False

    def rotationbyspeed(self, x, y):
        # print('rotation')
        # print(x, y)
        if x != 0 and y != 0:
            min_speed = min(abs(x), abs(y))
        elif x != 0:
            min_speed = abs(x)
        elif y != 0:
            min_speed = abs(y)
        else:
            min_speed = 1
        self.x_speed = x / min_speed
        self.y_speed = y / min_speed
        self.duration = 1 / min_speed
        # if x != 0 or y != 0:
        #     self.duration = 0.001
        #     self.x_speed = x * self.duration
        #     self.y_speed = y * self.duration
        # else:
        #     self.x_speed = 0
        #     self.y_speed = 0

    def rotation_by_speed(self, x, y):
        print(x, y)

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

        print(self.x_speed, self.y_speed)

    def controller_band_with_config(self, band_id):
        if self.my_json_config[band_id]["enabled"]:
            msg_l0 = self.json_data_with_config[band_id]
            if self.my_json_config[band_id]["mode"] == "mouse":
                rotation_x = msg_l0['x'] if abs(msg_l0['x']) > 1 else 0
                rotation_y = msg_l0['y'] if abs(msg_l0['y']) > 1 else 0
                self.rotation_by_speed(rotation_x, rotation_y)


class MioAPISignals(QObject):
    band_status = pyqtSignal(object)
    usb_device_status = pyqtSignal(object)


class Mio_API_get_data(QRunnable):
    def __init__(self, band_control=None):
        super(Mio_API_get_data, self).__init__()
        self.config_changed = False
        self.stop_requested = False
        self.band_control = band_control
        self.json_data_with_config = dict()
        self.my_json_config = dict()
        self.signals = MioAPISignals()
        self.ser = serial.Serial()
        self.ser.port = SERIAL_PORT
        self.ser.baudrate = 115200
        self.ser.timeout = 2
        self.init_json()
        self.band_control.start()#TODO

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
                    s_list = line.decode().split(',')[:-1]
                    i_list = []
                    for i in s_list:
                        try:
                            i_list.append(int(i))
                        except:
                            pass
                    try:
                        if i_list[0]:
                            x = -i_list[1]
                        else:
                            x = i_list[1]

                        if i_list[2]:
                            y = -i_list[3]
                        else:
                            y = i_list[3]

                        s = i_list[4]
                        band_id = str(i_list[5])
                        self.json_data_with_config[band_id] = {'x': -y, 'y': x, 's': s}
                        self.set_band_json_data(self.json_data_with_config)
                    except:
                        pass
            except:
                time.sleep(3)
                self.ser.close()

    def check_config(self):
        if self.config_changed:  # Теперь проверка на то был ли изменен конфиг
            print('Config changed, obtaining config again')
            self.init_json()
            self.config_changed = False  # ОБЯЗАТЕЛЬНО ПЕРЕКЛЮЧИТЬ ОБРАТНО!
            print(self.my_json_config)

    # def test_data(self):
    #     while 1:
    #         for i in range(100):
    #             print(i)
    #             if i > 20:
    #                 self.json_data_with_config = {'x': 1, 'y': 3, 's': 0}
    #             if i > 40:
    #                 self.json_data_with_config = {'x': 1, 'y': 3, 's': 0}
    #             if i > 60:
    #                 self.json_data_with_config = {'x': 1, 'y': 1, 's': 1}
    #             if i > 80:
    #                 self.json_data_with_config = {'x': 3, 'y': 1, 's': 0}
    #             if i > 40:
    #                 self.json_data_with_config = {'x': 0, 'y': 0, 's': 0}

    def init_json(self):
        with open(PATH_TO_DEFAULT_CONFIG, mode='r') as f:
            self.json_config = json.load(f)
        # print(self.json_config)
        self.armbands = self.json_config['armbands']
        for armband in self.armbands:
            self.json_data_with_config[armband["id"]] = {'x': 0, 'y': 0, 's': 0}
            # self.set_band_json_data(self.json_data_with_config)
            self.my_json_config[armband["id"]] = armband
            # if armband["arm"] == "right":
            #     self.right_id = armband["id"]
            # elif armband["arm"] == "left":
            #     self.left_id = armband["id"]
        # self.set_band_my_json_config(self.my_json_config)


if __name__ == '__main__':
    mio_control = Mio_API_control()
    get_data = Mio_API_get_data(mio_control)

    # get_data.start()
    # mio_control.start()
import time
from threading import Thread

import serial


class Mio_API_get_data(Thread):
    def __init__(self, serial_port):
        super(Mio_API_get_data, self).__init__()
        self.serial_port = serial_port
        self.config_changed = False
        self.stop_requested = False
        self.json_data_with_config = dict()
        self.my_json_config = dict()
        self.ser = serial.Serial()
        self.ser.port = self.serial_port
        self.ser.baudrate = 115200
        self.ser.timeout = 2
        self.start_time = time.time()
        self.running_time_list = []
        print(f'Start time:{self.start_time}')
        # self.band_control.start()  # TODO

    def run(self):

        self.open_serial()
        # self.test_data()

    def open_serial(self):
        while not self.stop_requested:
            try:
                # print('check conf')
                # print(f'Trying to open port {self.ser.port}')
                self.ser.open()
                line = self.ser.readline()
                # print(f'Data: {line}')
                while 1:
                    line = self.ser.readline()
                    if len(line) < 10 and len(line) > 1:
                        print(f'Power: {line.decode()}')
                        continue

                    # print(f'Data: {line}')

                    s_list = line.decode().split(',')[:-1]
                    # print(s_list)
                    i_list = []
                    # if s_list[-5] == '%':
                    #     print(line)
                    #     continue
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
                        # self.emit_detect(band_id)
                        self.json_data_with_config[band_id] = {'x': -y, 'y': x, 's': s}
                    except:
                        t = time.time() - self.start_time
                        self.start_time = time.time()
                        self.running_time_list.append(t)


                        print(f'Running time: {t}')
                        print(max(self.running_time_list))

            except:
                time.sleep(3)
                self.ser.close()




if __name__ == '__main__':
    serial_port = 'COM3'
    get_data = Mio_API_get_data(serial_port)
    get_data.start()
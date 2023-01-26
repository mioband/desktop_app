import sys
import glob
import json


class BandConfig(object):

    def __str__(self):
        return f"\nName: {self.name}\nID: {self.id}\nIs enabled: {self.enabled}\nMode: {self.mode}\nBindings: {self.bindings}"

    def __init__(self, config_dict):
        self.name = config_dict['name']
        self.id = config_dict['id']
        self.enabled = config_dict['enabled']
        self.mode = config_dict['mode']
        self.bindings = config_dict['bindings']

    def to_dict(self):
        return {'name': self.name, 'id': self.id, 'enabled': self.enabled, 'mode': self.mode,
                       'bindings': self.bindings}


class Config(object):

    def __str__(self):
        header = f"CONFIGURATION OBJECT OBTAINED FROM FILE {self.path}"
        bindings = f"Available bindings: {self.available_bindings}"
        usb_device = f"USB device configuration: {self.usb_device}"
        left_band = f"Left armband configuration: {self.left_band}"
        right_band = f"Right armband configuration: {self.right_band}"
        l = '\n====================================================================================================\n'
        s = '\n----------------------------------------------------------------------------------------------------\n'
        return f"{l}{header}{s}{bindings}{s}{usb_device}{s}{left_band}{s}{right_band}{l}"

    def __init__(self, path_to_config_file):
        self.path = path_to_config_file
        self.config_dict = None
        self.available_bindings = None
        self.usb_device = None
        self.left_band = None
        self.right_band = None
        self.read(self.path)

    def read(self, path_to_config_file):
        with open(path_to_config_file) as json_file:
            self.config_dict = json.load(json_file)
        self.available_bindings = self.config_dict['available_bindings']
        self.usb_device = self.config_dict['usb_device']
        self.left_band = BandConfig(self.config_dict['left'])
        self.right_band = BandConfig(self.config_dict['right'])

    def write(self, path_to_config_file):
        self.config_dict['available_bindings'] = self.available_bindings
        self.config_dict['usb_device'] = self.usb_device
        self.config_dict['left'] = self.left_band.to_dict()
        self.config_dict['right'] = self.right_band.to_dict()
        with open(path_to_config_file, 'w') as fp:
            json.dump(self.config_dict, fp, indent=2)


def get_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = ports
    return result


if __name__ == '__main__':
    config = Config("D:\work\mioband\desktop_app\config\config.json")
    print(config)

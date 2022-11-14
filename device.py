import logging
import pyvisa
import vxi11


class Device:
    def __init__(self, ip=None, usb=None):
        self.device = None
        self.ip = ip
        self.usb = usb


    def write(self, msg):
        logging.debug(f"Message send: {msg} to {self.ip} {self.usb}")
        if self.ip is not None:
            self.device.write(msg)
        elif self.usb is not None:
            self.device.write(msg)

    def ask(self, msg):
        logging.debug(f"Message asked: {msg} to {self.ip} {self.usb}")
        if self.ip is not None:
            ret = self.device.ask(msg)
        elif self.usb is not None:
            ret = self.device.query(msg)
        logging.debug(f"Message received: {ret.strip()} from {self.ip} {self.usb}")
        return ret

    def connect(self):
        if self.ip is not None:
            try:
                self.device = vxi11.Instrument(self.ip)
                return True
            except:
                logging.error(f"Couldn't connect to {self.ip}")
                return False
        elif self.usb is not None:
            try:
                rm = pyvisa.ResourceManager()
                self.device = rm.open_resource(self.usb)

                return True
            except:
                logging.error(f"Couldn't connect to {self.ip}")
                return False

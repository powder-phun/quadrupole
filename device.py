import logging
import pyvisa
import vxi11
import serial
import time


class Device:
    def __init__(self, ip=None, usb=None, serial_port=None, baud=9600):
        self.device = None
        self.ip = ip
        self.usb = usb
        self.baud = baud
        self.serial_port = serial_port


    def write(self, msg):
        logging.debug(f"Message sent: {msg} to {self.ip} {self.usb} {self.serial_port}")
        if self.ip is not None:
            self.device.write(msg)
        elif self.usb is not None:
            self.device.write(msg)
        elif self.serial_port is not None:
            self.device.write((msg+'\n').encode())

    def ask(self, msg):
        logging.debug(f"Message asked: {msg} to {self.ip} {self.usb}")
        if self.ip is not None:
            ret = self.device.ask(msg)
        elif self.usb is not None:
            ret = self.device.query(msg)
        elif self.serial_port is not None:
            self.write(msg)
            ret = self.device.readline()
        logging.debug(f"Message received: {ret.strip()} from {self.ip} {self.usb}")
        return ret

    def read_raw(self):
        logging.debug(f"Reading raw bytes")
        if self.ip is not None:
            ret = self.device.read_raw()
        elif self.usb is not None:
            ret = self.device.read_raw()
        return ret

    def connect(self):
        if self.ip is not None:
            try:
                self.device = vxi11.Instrument(self.ip)
                self.device.timeout = 30
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
        elif self.serial_port is not None:
            try:
                self.device = serial.Serial(self.serial_port, self.baud, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=5)
                return True
            except:
                logging.error(f"Couldn't connect to {self.ip}")
                return False
            

import vxi11
import time
import logging
import pyvisa
import serial
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig
from time import sleep
from device import Device

class HamegHM5014Controller(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.ip = None
        self.usb = None
        self.serial_port = None
        self.param = None
        self.type = None

        self.parseConfig()

    @staticmethod
    def getName():
        return "HM5014"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "Amax": False,
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "Amax": "dB"
        }

    @staticmethod
    def getMinDict() -> dict[str, bool]:
        return {}

    @staticmethod
    def getMaxDict() -> dict[str, bool]:
        return {}

    def parseConfig(self):
        print(self.config.json)
        if "port" in self.config.json:
            self.serial_port = self.config.json["port"]
        else:
            logging.error("No port specified")
            return False

        self.param = self.config.params[0].name

        if "center_freq" in self.config.json:
            self.center_freq = float(self.config.json["center_freq"])
        else:
            self.center_freq = None
        
        if "span" in self.config.json:
            self.span = self.config.json["span"]
        else:
            self.span = None

        if "config_commands" in self.config.json:
            self.config_commands = self.config.json["config_commands"]
        else:
            self.config_commands = None

        return True

    def adjust(self, param: str, value: float) -> None:
        logging.error("No adjustable params")

    def connect(self) -> bool:
        self.ser = serial.Serial(self.serial_port, 4800)
        self.ser.write(b'#kl1\r')
        self.ser.write(b'#br115200\r')
        self.ser.close()
        time.sleep(0.1)
        self.ser = serial.Serial(self.serial_port, 115200)
        time.sleep(0.1)
        self.ser.write(b'#kl1\r')
        time.sleep(0.1)
        if self.center_freq is not None:
            self.ser.write("#cf{:08.3f}\r".format(self.center_freq).encode())
            print("#cf{:08.3f}\r".format(self.center_freq).encode())
            time.sleep(0.1)
        if self.span is not None:
            self.ser.write((f"#sp{int(self.span)}\r").encode())
            print((f"#sp{int(self.span)}\r").encode())
            time.sleep(0.1)
        if self.config_commands is not None:
            pass#self.ser.write(self.config_commands.encode())
        print("sent")
        return True


    def enable(self, state: bool):
        print("enable")
        pass


    def read(self, param: str) -> float:
        if param == "Amax":
            self.ser.write((f"#dm0\r").encode())
            time.sleep(0.1)
            self.ser.write((f"#vm3\r").encode())
            time.sleep(6)
            
            self.ser.flushInput()
            self.ser.write((f"#bm1\r").encode())
            c = self.ser.read(5)
            c = self.ser.read(2001)
            
            
            amplitudes = np.frombuffer(c, dtype=np.uint8)*0.4-80.8
            frequencies = np.linspace(self.center_freq-self.span/2, self.center_freq+self.span/2, 2001)
            lin_amplitudes = 10**(amplitudes/10) * 1e-3
            print(amplitudes)
            
            peaks, properties = sp.signal.find_peaks(amplitudes, height=-56, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)

            plt.plot(frequencies, amplitudes)
            plt.plot(frequencies[peaks], amplitudes[peaks], "x")
            plt.show()

            plt.plot(frequencies, lin_amplitudes)
            plt.plot(frequencies[peaks], lin_amplitudes[peaks], "x")
            plt.show()

            for peak in peaks:
                print(frequencies[peak], lin_amplitudes[peak])


            lin_amplitudes[np.argmax(lin_amplitudes)] = 0

            print(lin_amplitudes[peaks])
            
            lin_Amax = np.max(lin_amplitudes) #in watts
            lin_thd = np.sum(lin_amplitudes[peaks]) / lin_Amax #in terms of power
            Amax = 10 * np.log10(lin_Amax/1e-3)
            thd = 10 * np.log10(lin_thd)


            print(f"THD {lin_thd}, Amax {lin_Amax}w")
            print(f"THD {thd}dB, Amax {Amax}dBm")


            print(self.ser.in_waiting)
            return(np.max(amplitudes))
        else:
            logging.error("Wrong param name")

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
#from time import sleep
#from time import time
import time
from device import Device


#base_freq has to be first parameter invoked in config!

class HamegHM5014Controller(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.ip = None
        self.usb = None
        self.serial_port = None
        self.param = None
        self.type = None
        self.measurement_timestamp = 0

        self.parseConfig()

    @staticmethod
    def getName():
        return "HM5014"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "base_freq": True,
            "timestamp": False,
            "Pmax": False,
            "lin_Pmax": False,
            "base_P": False,
            "base_dB": False,
            "base_V": False,
            "thd": False,
            "lin_thd": False
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "base_freq": "Hz",
            "timestamp": "s",
            "Pmax": "dBm",
            "lin_Pmax": "w",
            "base_P": "w",
            "base_dB": "dB",
            "base_V": "V",
            "thd": "dB",
            "lin_thd": ""
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
        
        if "attenuator" in self.config.json:
            self.attenuator = int(self.config.json["attenuator"])
        else:
            self.attenuator = None

        if "added_attenuator" in self.config.json:
            self.added_attenuator = int(self.config.json["added_attenuator"])
        else:
            self.added_attenuator = 0
        
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
        self.base_freq = value

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
            self.ser.write("#cf{:08.3f}\r".format(self.center_freq/1.0e6).encode())
            print("#cf{:08.3f}\r".format(self.center_freq/1.0e6).encode())
            time.sleep(0.1)
        if self.span is not None:
            self.ser.write((f"#sp{int(self.span)}\r").encode())
            print((f"#sp{int(self.span/1e6)}\r").encode())
            time.sleep(0.1)
        if self.attenuator is not None:
            self.ser.write((f"#at{int(self.attenuator)}\r").encode())
            print((f"#at{int(self.attenuator)}\r").encode())
            time.sleep(0.5)
        if self.config_commands is not None:
            pass#self.ser.write(self.config_commands.encode())
        print("sent")
        time.sleep(1)
        return True


    def enable(self, state: bool):
        print("enable")
        pass

    def measure(self):
        self.ser.write((f"#dm0\r").encode())
        time.sleep(0.1)

        self.ser.write((f"#at{int(self.attenuator)}\r").encode())
        time.sleep(0.5)

        self.ser.write((f"#vm3\r").encode())
        time.sleep(6)
        
        self.ser.flushInput()
        self.ser.write((f"#bm1\r").encode())
        c = self.ser.read(5)
        c = self.ser.read(2001)
        
        print(f"max: {np.max(np.frombuffer(c, dtype=np.uint8))}")

        if np.max(np.frombuffer(c, dtype=np.uint8)) > 230 and self.attenuator < 35:
            self.attenuator += 10
            self.measure()
            return
        
        if np.max(np.frombuffer(c, dtype=np.uint8)) < 177 and self.attenuator > 5:
            self.attenuator -= 10
            self.measure()
            return

        self.peaks, self.properties = sp.signal.find_peaks(np.frombuffer(c, dtype=np.uint8), height=65, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)

        if len(self.peaks)==0:
            self.base_dB = -100
            self.Pmax = -100
            self.thd = 0
            self.lin_Pmax = 0
            self.lin_thd = 1
            self.lin_Pmax = 0

        self.amplitudes = np.frombuffer(c, dtype=np.uint8)*0.4-120.8+self.attenuator+self.added_attenuator #in dB
        self.frequencies = np.linspace(self.center_freq-self.span/2, self.center_freq+self.span/2, 2001) #in Hz
        self.lin_powers = 10**(self.amplitudes/10) * 1e-3 #in w
        

        #find base frequency:
        f_diff = np.abs(self.frequencies[self.peaks] - self.base_freq)
        self.base_peak_index = f_diff.argmin()
        self.harmonic_peaks = np.delete(self.peaks, self.base_peak_index)


        self.base_P = self.lin_powers[self.peaks[self.base_peak_index]]
        self.base_dB = self.amplitudes[self.peaks[self.base_peak_index]]
        self.base_V = np.sqrt(self.base_P*50)

        print(f"base index: {self.base_peak_index}, base freq: {self.frequencies[self.peaks[self.base_peak_index]]}, base dB: {self.base_dB}")

        #plt.plot(frequencies, amplitudes)
        #plt.plot(frequencies[peaks], amplitudes[peaks], "x")
        #plt.show()

        #plt.plot(frequencies, lin_powers)
        #plt.plot(frequencies[peaks], lin_powers[peaks], "x")
        #plt.show()

        for peak in self.peaks:
            print(self.frequencies[peak], self.amplitudes[peak])

        
        self.lin_Pmax = np.max(self.lin_powers) #in watts
        if len(self.harmonic_peaks) == 0:
            self.lin_thd = 1/10000000
        else:
            self.lin_thd = np.sqrt(np.sum(self.lin_powers[self.harmonic_peaks]) / self.base_P) #in terms of voltage
        self.Pmax = 10 * np.log10(self.lin_Pmax/1e-3) #in dB
        self.thd = 20 * np.log10(self.lin_thd) #in dB

        self.measurement_timestamp = int(time.time())


        print(f"THD {self.lin_thd}, Pmax {self.lin_Pmax}w")
        print(f"THD {self.thd}dB, Pmax {self.Pmax}dBm")


        print(self.ser.in_waiting)


    def read(self, param: str) -> float:
        if param == "base_freq":
            self.measure()
            return(self.base_freq)
        if param == "timestamp":
            return(self.measurement_timestamp)
        elif param == "Pmax":
            if self.Pmax is None:
                return(-100)
            return(self.Pmax)
        elif param == "lin_Pmax":
            if self.lin_Pmax is None:
                return(0)
            return(self.lin_Pmax)
        elif param == "base_P":
            return(self.base_P)
        elif param == "base_V":
            return(self.base_V)
        elif param == "base_dB":
            return(self.base_dB)
        elif param == "thd":
            return(self.thd)
        elif param == "lin_thd":
            return(self.lin_thd)
        else:
            logging.error("Wrong param name")

#########################
# IMPORTANT: Due to a used hack, frequency param must always go first in config
#########################
# Available measurement types and their param types (apart from frequency):
#  impedance: |Z|, arg(Z), R, X, L, C, Q
#  transmitance: gain, gain_log, phase
# Reference impedance is specified using "reference_impedance" field (only real for now)
# Probe gain can be specified using: "channel_gain_a", "channel_gain_b"
# Circuit used to measure everything apart from transmitance:
#
# Source - A - Resistor - B - DUT
#    |     |              |    |
#    ----------------------------- GND
#
# Circuit used for measuring transmitance:
#
# Source - A - DUT - B
#    |     |    |    |
#    ------------------- GND
#


import logging
import math
import cmath
import time
import struct
import numpy as np

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig

from device import Device

SCOPE_DELAY = 0.5

class ImpedanceController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.ip = None
        self.usb = None
        self.param = None

        self.frequency = 1
        self.reference_impedance = 50
        self.phasor = [None, None] # last measured phasor of channel a
        self.volt_div = [None, None]

        self.parseConfig()

    @staticmethod
    def getName():
        return "impedance"

    def getIsEditableDict(self) -> dict[str, bool]:
        return {
            "|Z|": False,
            "arg(Z)": False,
            "R": False,
            "X": False,
            "gain": False,
            "gain_log": False,
            "phase": False,
            "L": False,
            "C": False,
            "Q": False,
            "frequency": True
        }
    
    def getUnitDict(self) -> dict[str, str]:
        return {
            "|Z|": "Ω",
            "arg(Z)": "°",
            "R": "Ω",
            "X": "Ω",
            "gain": "-",
            "gain_log": "dB",
            "phase": "°",
            "L": "H",
            "C": "F",
            "Q": "-",
            "frequency": "Hz"
        }

    def getMinDict(self) -> dict[str, bool]:
        return {}

    def getMaxDict(self) -> dict[str, bool]:
        return {}


    def parseConfig(self):
        if "ip" in self.config.json:
            self.ip = self.config.json["ip"]
        elif "usb" in self.config.json:
            self.usb = self.config.json["usb"]
        else:
            logging.error("No ip address or usb specified")
            return False

        if "reference_impedance" in self.config.json:
            self.reference_impedance = self.config.json["reference_impedance"]
        else:
            logging.warning("No reference impedance specified, using 50Ω")
        
        return True

    def connect(self) -> bool:
        self.device = Device(usb=self.usb, ip=self.ip)
        ret = self.device.connect()
        if ret:
            time.sleep(SCOPE_DELAY)
            self.volt_div[0] = self.get_vdiv(0)
            self.volt_div[1] = self.get_vdiv(1)
        return ret

    def enable(self, state: bool):
        pass

    def adjust(self, param: str, value: float) -> None:
        # Assuming set param if frequency, for now
        self.frequency = value

    def read(self, param: str) -> float:
        if param in [p.name for p in self.config.params]:
            logging.debug(f"Searching for param: {param}")
            t = next(p.type for p in self.config.params if p.name == param)
            if t == "frequency":
                self.measure()
                return self.frequency
            elif t == "|Z|":
                return abs(self.calculate_impedance())
            elif t == "arg(Z)":
                return cmath.phase(self.calculate_impedance()) / (2*math.pi) * 360
            elif t == "R":
                return self.calculate_impedance().real
            elif t == "X":
                return self.calculate_impedance().imag
            elif t == "L":
                return self.calculate_impedance().imag/(2*math.pi*self.frequency)
            elif t == "C":
                return -1/(2*math.pi*self.frequency*self.calculate_impedance().imag)
            elif t == "Q":
                return abs(self.calculate_impedance().imag/self.calculate_impedance().real)
            elif t == "gain":
                return abs(self.phasor[1]/self.phasor[0])
            elif t == "gain_log":
                return 20*math.log10(abs(self.phasor[1]/self.phasor[0]))
            elif t == "phase":
                return (cmath.phase(self.phasor[1])-cmath.phase(self.phasor[0])) / (2*math.pi) * 360
            else:
                logging.error(f"Unsupported type: {t}")
        else:
            logging.error(f"Invalid param name: {param}")

    
    def calculate_impedance(self):
        return (self.reference_impedance * self.phasor[1])/(self.phasor[0]-self.phasor[1])


    def measure(self):
        self.set_timediv(1/self.frequency)
        sample_rate = self.get_samplerate()

        a = self.acquire(0)
        while not self.scale(a, 0):
            time.sleep(SCOPE_DELAY)
            a = self.acquire(0)

        b = self.acquire(1)
        while not self.scale(b, 1):
            time.sleep(SCOPE_DELAY)
            b = self.acquire(1)

        self.phasor[0] = self.get_phasor(self.frequency, sample_rate, a)
        self.phasor[1] = self.get_phasor(self.frequency, sample_rate, b)

    @staticmethod
    def get_phasor(frequency, sample_rate, data):
        
        count = len(data)
        print(frequency, sample_rate, count)

        t = np.arange(0, count) / sample_rate
        phase = 2 * np.pi * frequency * t
        value = np.sum(data * np.exp(1j * phase))

        return value

    def acquire(self, channel):
        self.device.write(f"C{channel+1}:WF? ALL")
        return self.parse(self.device.read_raw())

    def set_vdiv(self, channel, value):
        self.device.write(f"C{channel+1}:VDIV {value}V")

    def get_vdiv(self, channel):
        ret = self.device.ask(f"C{channel+1}:VDIV?")
        return(float(ret.split()[1][:-1]))

    def set_timediv(self, value):
        self.device.write(f"TDIV {value}s")

    def get_samplerate(self):
        ret = self.device.ask(f"SARA?")
        num = float(ret.split()[1][:-4])
        return num


    def parse(self, response: bytes):
        index = response.find(b"WAVEDESC")
        wavedesc = response[index: index + 346]

        probe_attenuation = (struct.unpack("<f", wavedesc[328:332]))[0]
        vertical_gain = (struct.unpack("<f", wavedesc[156:160]))[0]
        vertical_offset = (struct.unpack("<f", wavedesc[160:164]))[0]

        points = np.frombuffer(
            response[index + 346: -2], dtype=np.int8).astype(float)
        points *= vertical_gain / 25
        points -= vertical_offset
        points *= probe_attenuation

        logging.debug("Parsed response. Gain: {vertical_gain}, Offset: {vertical_offset}, Probe: {probe_attenuation}")

        return points

    def scale(self, data, channel):
        maximum = np.max(np.abs(data))
        logging.debug(f"Scaling channel: {channel} with volt/div: {self.volt_div[channel]} ({self.volt_div[channel] * 1.5}-{self.volt_div[channel] * 3.6}). Max is {maximum}")

        # Check if not to small, if so, check wheter scale can be increased
        if maximum < self.volt_div[channel] * 1.5 and self.volt_div[channel] >= 0.0005*1.5:
            self.volt_div[channel] /= 1.5
            self.set_vdiv(channel, self.volt_div[channel])
            logging.debug(f'Scale in {channel}')
            return False

        # Check if not clipping, if so, check wheter scale can be decreased
        if maximum > self.volt_div[channel] * 3.6 and self.volt_div[channel] <= 10/1.5:
            self.volt_div[channel] *= 1.5
            self.set_vdiv(channel, self.volt_div[channel])
            logging.debug(f'Scale out {channel}')
            return False

        return True

        
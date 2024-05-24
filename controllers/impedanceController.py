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

SCOPE_DELAY = 1

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
        self.harmonics = [[], []]
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
            "amplitude_1_rms": False,
            "amplitude_1_pkpk": False,
            "amplitude_1_dBm": False,
            "frequency": True,
            "THD_1": False,
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
            "amplitude_1_rms": "Vrms",
            "amplitude_1_pkpk": "Vpp",
            "amplitude_1_dBm": "dBm",
            "THD_1": "-",
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
        
        if "harmonics" in self.config.json:
            count = self.config.json["harmonics"]
            self.harmonics = [[None for i in range(count)], [None for i in range(count)]]
        
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
                return -self.calculate_impedance().imag/(2*math.pi*self.frequency)
            elif t == "C":
                return 1/(2*math.pi*self.frequency*self.calculate_impedance().imag)
            elif t == "Q":
                return abs(self.calculate_impedance().imag/self.calculate_impedance().real)
            elif t == "gain":
                return abs(self.phasor[1]/self.phasor[0])
            elif t == "gain_log":
                return 20*math.log10(abs(self.phasor[1]/self.phasor[0]))
            elif t == "phase":
                return (((cmath.phase(self.phasor[1])-cmath.phase(self.phasor[0]))+3*math.pi)%(2*math.pi)-math.pi) / (2*math.pi) * 360
            elif t == "amplitude_1_rms":
                return abs((self.phasor[0]))
            elif t == "amplitude_1_pkpk":
                return abs((self.phasor[0])*2*math.sqrt(2))
            elif t == "amplitude_1_dBm":
                return 10*np.log10((abs((self.phasor[0]))**2/50.0*1000))
            elif t == "THD_1":
                return self.calculate_THD(0)
            elif t == "THD_2":
                return self.calculate_THD(1)
            else:
                logging.error(f"Unsupported type: {t}")
        else:
            logging.error(f"Invalid param name: {param}")

    
    def calculate_impedance(self):
        return (self.reference_impedance * self.phasor[1])/(self.phasor[0]-self.phasor[1])

    def calculate_THD(self, channel):
        sum_of_squares = sum(abs(x)**2 for x in self.harmonics[channel])
        print(self.harmonics)
        return math.sqrt(sum_of_squares) / abs(self.phasor[channel])

    def measure(self):
        self.set_timediv(1/self.frequency)
        sample_rate = self.get_samplerate()
        time.sleep(SCOPE_DELAY)
        acq_delay = 1.2*self.get_timediv()*14
        self.trigger()
        time.sleep(SCOPE_DELAY+acq_delay)

        b = self.acquire(1)
        a = self.acquire(0)
        self.device.write(f"TRMD AUTO")
        while (not self.scale(a, 0)) or (not self.scale(b, 1)):
            #self.trigger()
            time.sleep(SCOPE_DELAY+acq_delay)
            print(SCOPE_DELAY+acq_delay)
            a = self.acquire(0)
            b = self.acquire(1)


        self.phasor[0] = self.get_phasor(self.frequency, sample_rate, a)
        self.phasor[1] = self.get_phasor(self.frequency, sample_rate, b)

        for i in range(len(self.harmonics[0])):
            self.harmonics[0][i] = self.get_phasor(self.frequency * (i+2), sample_rate, a)
            self.harmonics[1][i] = self.get_phasor(self.frequency * (i+2), sample_rate, b)

    @staticmethod
    def get_phasor(frequency, sample_rate, data):
        
        count = len(data)

        t = np.arange(0, count) / sample_rate
        phase = 2 * np.pi * frequency * t
        value = np.sum(data * np.exp(1j * phase))
        scale = np.sum((np.sin(phase)+np.cos(phase)) * np.exp(1j * phase))

        return (np.real(value)/np.real(scale) + 1j*np.imag(value)/np.imag(scale))/np.sqrt(2)

    def acquire(self, channel):
        self.device.write(f"C{channel+1}:WF? ALL")
        return self.parse(self.device.read_raw())
    
    def trigger(self):
        self.device.write(f"TRMD SINGLE;ARM;FRTR")

    def set_vdiv(self, channel, value):
        self.device.write(f"C{channel+1}:VDIV {value}V")

    def get_vdiv(self, channel):
        ret = self.device.ask(f"C{channel+1}:VDIV?")
        return(float(ret.split()[1][:-1]))

    def set_timediv(self, value):
        self.device.write(f"TDIV {value}s")
    
    def get_timediv(self):
        ret = self.device.ask(f"TDIV?")
        print(ret)
        return(float(ret.split()[1][:-1]))

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


import serial
import time
import logging

from config import ControllerConfig, ParamConfig
from controllers.controller import Controller

EOL = '\x0A'

class FYController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config
        self.device = None
        self.port = None
        self.amplitudeParam: [str, str] = [None, None]
        self.offsetParam: [str, str] = [None, None]
        self.frequencyParam: [str, str] = [None, None]

        self.amplitude: [float, float] = [0, 0]
        self.offset: [float, float] = [0, 0]
        self.frequency: [float, float] = [0, 0]

        self.waveform = [None, None]

        self.parseConfig()

    @staticmethod
    def getName():
        return "fy"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "amplitude": True,
            "offset": True,
            "frequency": True
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "amplitude": "Vpp",
            "offset": "V",
            "frequency": "Hz"
        }

    @staticmethod
    def getMinDict() -> dict[str, float]:
        return {
            "amplitude": 0,
            "offset": -12,
            "frequency": 0
        }

    @staticmethod
    def getMaxDict() -> dict[str, float]:
        return {
            "amplitude": 24,
            "offset": 12,
            "frequency": 60e6
        }

    def parseConfig(self):
        if "port" in self.config.json:
            self.port = self.config.json["port"]
        else:
            logging.error("No port specified")
            return False
        for param in self.config.params:
            if param.json.get("channel", 0) == 1 or param.json.get("channel", 0) == 2:
                if param.type == "amplitude":
                    self.amplitudeParam[param.json["channel"]-1] = param.name
                elif param.type == "offset":
                    self.offsetParam[param.json["channel"]-1] = param.name
                elif param.type == "frequency":
                    self.frequencyParam[param.json["channel"]-1] = param.name
                else:
                    logging.error(f"Invalid parameter name {param}")
            else:
                logging.error(f"Not specified or invalid channel (should be 1 or 2) for param {param.name}")


        return True


    def connect(self) -> bool:
        if self.device is None:
            self.device = serial.Serial(self.port, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=5)
            return True
        else:
            return True

    def adjust(self, param: str, value: float) -> None:
        if param == self.amplitudeParam[0]:
            self.amplitude[0] = value
            self.set_amplitude(value, 1)
        elif param == self.amplitudeParam[1]:
            self.amplitude[1] = value
            self.set_amplitude(value, 2)
        elif param == self.offsetParam[0]:
            self.offset[0] = value
            self.set_offset(value, 1)
        elif param == self.offsetParam[1]:
            self.offset[1] = value
            self.set_offset(value, 2)
        elif param == self.frequencyParam[0]:
            self.frequency[0] = value
            self.set_frequency(value, 1)
        elif param == self.frequencyParam[1]:
            self.frequency[1] = value
            self.set_frequency(value, 2)

    def send_command(self, command, channel):
        channel = "M" if channel == 1 else "F"
        cmd = "W" + channel + command + EOL
        logging.debug(f"Command send: {cmd}")
        self.device.write(cmd.encode())

    def set_frequency(self, frequency, channel):
        self.send_command('F%014u' % int(frequency*1e6), channel)

    def set_amplitude(self, amplitude, channel):
        self.send_command('A%.2f' % amplitude, channel)

    def set_offset(self, offset, channel):
        self.send_command('O%.2f' % offset, channel)

    def enable(self, state: bool):
        if state:
            self.send_command("N1", 1)
            self.send_command("N1", 2)
        else:
            self.send_command("N0", 1)
            self.send_command("N0", 2)

    def read(self, param: str) -> float:
        if param == self.amplitudeParam[0]:
            return self.amplitude[0]
        elif param == self.amplitudeParam[1]:
            return self.amplitude[1]
        elif param == self.offsetParam[0]:
            return self.offset[0]
        elif param == self.offsetParam[1]:
            return self.offset[1]
        elif param == self.frequencyParam[0]:
            return self.frequency[0]
        elif param == self.frequencyParam[1]:
            return self.frequency[1]
        else:
            logging.error(f"Invalid param name {param}")
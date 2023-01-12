import pyvisa
import time
import logging

from config import ControllerConfig, ParamConfig
from controllers.controller import Controller

class AFGController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config
        self.device = None
        self.amplitudeParam: [str, str] = [None, None]
        self.offsetParam: [str, str] = [None, None]
        self.frequencyParam: [str, str] = [None, None]

        self.amplitude: [str, str] = [0, 0]
        self.offset = [0, 0]
        self.frequency = [0, 0]

        self.waveform = [None, None]

        self.parseConfig()

    @staticmethod
    def getName():
        return "afg"

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
            "amplitude": 0.001,
            "offset": -4.999,
            "frequency": 1e-6
        }

    @staticmethod
    def getMaxDict() -> dict[str, float]:
        return {
            "amplitude": 9.999,
            "offset": 4.999,
            "frequency": 60e6
        }

    def parseConfig(self):
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
            rm = pyvisa.ResourceManager()
            devices = rm.list_resources()
            for device in devices:
                if "USB" in device:
                    logging.info(f"TEK: Connecting to: {device}")
                    self.device = rm.open_resource(device)
                    resp = self.device.query("*IDN?")
                    if "AFG1062" in resp:
                        logging.info("TEK: Connected")
                        self.prepare()
                        return True

                    else:
                        self.device.close()
            else:
                return False
        else:
            return True

    def adjust(self, param: str, value: float) -> None:
        if param == self.amplitudeParam[0]:
            self.amplitude[0] = value
            self.device.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {:.0f}mVpp".format(int(value*1000)))
        elif param == self.amplitudeParam[1]:
            self.amplitude[1] = value
            self.device.write("SOURce2:VOLTage:LEVel:IMMediate:AMPLitude {:.0f}mVpp".format(int(value*1000)))
        elif param == self.offsetParam[0]:
            self.offset[0] = value
            self.device.write("SOURce1:VOLTage:LEVel:IMMediate:OFFSet {:.0f}mV".format(int(value*1000)))
        elif param == self.offsetParam[1]:
            self.offset[1] = value
            self.device.write("SOURce2:VOLTage:LEVel:IMMediate:OFFSet {:.0f}mV".format(int(value*1000)))
        elif param == self.frequencyParam[0]:
            self.frequency[0] = value
            self.device.write("SOURce1:FREQuency:FIXed {:.0f}Hz".format(value))
        elif param == self.frequencyParam[1]:
            self.frequency[1] = value
            self.device.write("SOURce2:FREQuency:FIXed {:.0f}Hz".format(value))

    def prepare(self) -> None:
        if "waveformOne" in self.config.json:
            self.device.write(f"SOURce1:FUNCtion:SHAPe {self.config.json['waveformOne']}")
        if "waveformTwo" in self.config.json:
            self.device.write(f"SOURce2:FUNCtion:SHAPe {self.config.json['waveformTwo']}")


    def enable(self, state: bool):
        if state:
            self.device.write("OUTPut1:STATe ON")
            self.device.write("OUTPut2:STATe ON")

        else:
            self.device.write("OUTPut1:STATe OFF")
            self.device.write("OUTPut2:STATe OFF")

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
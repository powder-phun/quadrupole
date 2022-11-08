from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import numpy as np
import math
import logging


from controllers.controller import Controller
from config import ParamConfig, ControllerConfig

class RudiController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config
        self.device = None
        self.ip = None
        self.voltageParam = [None, None, None, None]
        self.voltage = [None, None, None, None]

        self.parseConfig()

    @staticmethod
    def getName():
        return "rudi"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "voltage": True
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "voltage": "V"
        }

    @staticmethod
    def getMinDict() -> dict[str, float]:
        return {
            "voltage": -1500
        }

    @staticmethod
    def getMaxDict() -> dict[str, float]:
        return {
            "voltage": 1500
        }

    def parseConfig(self):

        if "ip" in self.config.json:
            self.ip = self.config.json["ip"]
        else:
            logging.error("No ip address specified")
            return False

        for param in self.config.params:
            if param.json.get("channel", 0) in [1, 2, 3, 4]:
                if param.type == "voltage":
                    self.voltageParam[param.json["channel"]-1] = param.name
                else:
                    logging.error(f"Invalid parameter name {param}")
            else:
                logging.error(f"Not specified or invalid channel (should be 1, 2, 3, or 4) for param {param.name}")


        return True

    def adjust(self, param: str, value: float) -> None:
        if param == self.voltageParam[0]:
            self.setOutput(1, value)
            self.voltage[0] = value
        elif param == self.voltageParam[1]:
            self.setOutput(2, value)
            self.voltage[0] = value
        elif param == self.voltageParam[2]:
            self.setOutput(3, value)
            self.voltage[0] = value
        elif param == self.voltageParam[3]:
            self.setOutput(4, value)
            self.voltage[0] = value
        else:
            logging.error(f"Invalid param name: {param}")

    def connect(self) -> bool:
        self.device = ModbusClient(host=self.ip, port=502, auto_open=True, auto_close=True)
        return True

    def changeMode(self, value):
        self.device.unit_id = 1
        self.device.write_single_register(5, value)
        self.device.unit_id = 2
        self.device.write_single_register(5, value)
        self.device.unit_id = 3
        self.device.write_single_register(5, value)
        self.device.unit_id = 4
        self.device.write_single_register(5, value)

    def enableOutputs(self):
        self.setOutput(1, self.voltage[0])
        self.setOutput(2, self.voltage[1])
        self.setOutput(3, self.voltage[2])
        self.setOutput(4, self.voltage[3])

    def setOutput(self, channel, value):
        self.voltage[channel-1] = value

        self.device.unit_id = channel
        mode = 7
        if value >= 0:
            if value < 1500:
                mode = 5
            else:
                mode = 3
        else:
            if value > -1500:
                mode = 6
            else:
                mode = 4
        self.device.write_single_register(5, mode)

        voltageMilivolts = np.uint32(math.fabs(value) * 1000)
        words = utils.long_list_to_word([voltageMilivolts])

        self.device.write_multiple_registers(2, words) 


    def enable(self, state: bool):
        if state:
            self.enableOutputs()
        else:
            self.changeMode(7)


    def read(self, param: str) -> float:
        if param == self.voltageParam[0]:
            return self.voltage[0]
        elif param == self.voltageParam[1]:
            return self.voltage[1]
        elif param == self.voltageParam[2]:
            return self.voltage[2]
        elif param == self.voltageParam[3]:
            return self.voltage[3]
        else:
            logging.error(f"Invalid param name: {param}")
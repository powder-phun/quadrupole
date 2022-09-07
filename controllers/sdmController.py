import pyvisa
import time

from controllers.controller import Controller
from parameter import ParameterID, Parameter

class SDMController(Controller):
    def __init__(self):
        self.device = None
        
    def getHandled(self):
        return {
            ParameterID.SDM_DC: Parameter(ParameterID.SDM_DC, "DC Multimeter", "V", False, minimum=-200, maximum=200)
        }


    def connect(self) -> bool:
        if self.device is None:
            rm = pyvisa.ResourceManager()
            devices = rm.list_resources()
            for device in devices:
                if "USB" in device:
                    print(f"SDM: Connecting to: {device}")
                    self.device = rm.open_resource(device)
                    resp = self.device.query("*IDN?")
                    if "SDM30" in resp:
                        print("SDM: Connected")
                        self.prepare()
                        return True

                    else:
                        self.device.close()
            else:
                return False
        else:
            return True

    def prepare(self) -> None:
        self.device.write("CONF:VOLT:DC AUTO")
        self.device.write("VOLT:DC:NPLC 1")
        self.device.write("TRIG:SOUR IMM")

    def read(self, param: ParameterID) -> float:
        if param == ParameterID.SDM_DC:
            ret = float(self.device.query("READ?"))
            return ret
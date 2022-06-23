import pyvisa
import time

from controllers.controller import Controller
from parameter import ParameterID, Parameter

class TekController(Controller):
    def __init__(self):
        self.device = None
        self.ac = 0.001
        self.dc = 0.001
        self.frequency = 1e6
        

    def getHandled(self):
        return {
            ParameterID.AC: Parameter(ParameterID.AC, "AC Gen", "V", True, 0, 20),
            ParameterID.DC: Parameter(ParameterID.DC, "DC Gen", "V", True, 0, 20),
            ParameterID.FREQUENCY: Parameter(ParameterID.FREQUENCY, "Gen Frequency", "Hz", True, 0, 60e6)
        }


    def adjust(self, param: ParameterID, value: float) -> None:
        if param == ParameterID.AC:
            self.ac = value
            self.device.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {:.0f}mVpp".format(value*1000))
            print("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {:.0f}mVpp".format(value*1000))
        if param == ParameterID.DC:
            self.dc = value
            self.device.write("SOURce2:VOLTage:LEVel:IMMediate:OFFSet {:.0f}mV".format(int(value*1000)))
        if param == ParameterID.FREQUENCY:
            self.frequency = value
            self.device.write("SOURce1:FREQuency:FIXed {:.0f}Hz".format(value))


    def connect(self) -> bool:
        if self.device is None:
            rm = pyvisa.ResourceManager()
            devices = rm.list_resources()
            for device in devices:
                if "USB" in device:
                    print(f"TEK: Connecting to: {device}")
                    self.device = rm.open_resource(device)
                    resp = self.device.query("*IDN?")
                    if "AFG1062" in resp:
                        print("TEK: Connected")
                        self.prepare()
                        return True

                    else:
                        self.device.close()
            else:
                return False
        else:
            return True

    def prepare(self) -> None:
        self.device.write("SOURce2:FUNCtion:SHAPe DC")
        self.device.write("SOURce2:VOLTage:LEVel:IMMediate:OFFSet 1mV")
        self.device.write("SOURce2:VOLTage:LEVel:IMMediate:AMPLitude 1mVpp")

        self.device.write("SOURce1:FUNCtion:SHAPe SINusoid")
        self.device.write("SOURce1:FREQuency:FIXed 1000000Hz")
        self.device.write("SOURce1:VOLTage:LEVel:IMMediate:OFFSet 1mV")
        self.device.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 1mVpp")



    def enable(self, state: bool):
        if state:
            self.device.write("OUTPut1:STATe ON")
            self.device.write("OUTPut2:STATe ON")

        else:
            self.device.write("OUTPut1:STATe OFF")
            self.device.write("OUTPut2:STATe OFF")



    def read(self, param: ParameterID) -> float:
        if param == ParameterID.AC:
            return self.ac
        if param == ParameterID.DC:
            return self.dc
        if param == ParameterID.FREQUENCY:
            return self.frequency
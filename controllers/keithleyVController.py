import pyvisa
import time

from controllers.controller import Controller
from parameter import ParameterID, Parameter

class KeithleyVController(Controller):
    def __init__(self):
        self.device = None

        self.voltage = 0
        

    def getHandled(self):
        return {
            ParameterID.KEITHLEY_I: Parameter(ParameterID.KEITHLEY_I, "Keythley I", "A", False, 0, 1),
            ParameterID.KEITHLEY_V: Parameter(ParameterID.KEITHLEY_V, "Keythley V", "V", True, 0, 100)
        }


    def adjust(self, param: ParameterID, value: float) -> None:
        if param == ParameterID.KEITHLEY_V:
            self.voltage = value
            self.device.write("B{},0,0X".format(int(value)))


    def connect(self) -> bool:
        if self.device is None:
            rm = pyvisa.ResourceManager()
            devices = rm.list_resources()
            print(devices)
            for device in devices:
                if "GPIB" in device:
                    print("Connecting to keithley")
                    print(device)
                    time.sleep(0.1)
                    self.device = rm.open_resource(device)

                    self.device.write("J0X") # Restore default settings
                    self.device.write("N0X")  #Standby mode
                    self.device.write("G4,2,0X") # Setup communication format
                    self.device.write("F0,0X") # Setup DC V Bias
                    self.device.write("L1,0X") # Setup auto range

                    return True
            else:
                return False
        else:
            return True


    def enable(self, state: bool):
        if state:
            self.device.write("N1X")
            self.device.write("H0X")
        else:
            self.device.write("N0X")


    def read(self, param: ParameterID) -> float:
        if param == ParameterID.KEITHLEY_I:
            val = float(self.device.read().strip())
            return val
        if param == ParameterID.KEITHLEY_V:
            return self.voltage
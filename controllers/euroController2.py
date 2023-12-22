import serial
import time
import logging
from euromeasure import EuroMeasure


from config import ControllerConfig, ParamConfig
from controllers.controller import Controller

em = EuroMeasure() # Create EuroMeasure object

class EM_parameter():
    def __init__(self, channel = None, address = None):
        self.channel = channel
        self.address = address

    def read(self):
        return self.state
    
    def adjust(self, value):
        self.state = value
        self.set(value)


    isEditable = None
    unit = ""
    min = float('-inf')
    max = float('inf')
    n_channels = None
    state = None

class Pid_p(EM_parameter):
    def set(self, p):
        return em.set_pid_d(p, self.address)

    isEditable = True

class Pid_i(EM_parameter):
    def set(self, i):
        return em.set_pid_d(i, self.address)

    isEditable = True

class Pid_d(EM_parameter):
    def set(self, d):
        return em.set_pid_d(d, self.address)

    isEditable = True

class Pid_state(EM_parameter):
    def set(self, state):
        return em.set_pid_state(state, self.address)

    isEditable = True

class Pid_setpoint(EM_parameter):
    def set(self, setpoint):
        return em.set_pid_setpoint(setpoint, self.address)

    isEditable = True

class Generator_amplitude(EM_parameter):
    def set(self, amplitude):
        return em.set_generator_amplitude(self.channel, amplitude, self.address)

    isEditable = True
    unit = "V"
    n_channels = 2

class Generator_frequency(EM_parameter):
    def set(self, frequenecy):
        return em.set_generator_frequency(self.channel, frequenecy, self.address)

    isEditable = True
    unit = "Hz"
    n_channels = 2

class Hvpsu_voltage(EM_parameter):
    def set(self, voltage):
        return em.set_hvpsu_voltage(self.channel, voltage, self.address)

    isEditable = True
    unit = "V"
    n_channels = 4

class Hvpsu_raw(EM_parameter):
    def set(self, voltage):
        return em.set_hvpsu_raw(self.channel, voltage, self.address)

    isEditable = True
    unit = "lsb"
    n_channels = 4

class Hvpsu_(EM_parameter):
    def set(self, voltage):
        return em.set_hvpsu_voltage(self.channel, voltage, self.address)

    isEditable = True
    unit = "A"
    n_channels = 4

class Source_psu_set_voltage(EM_parameter):
    def set(self, voltage):
        return em.set_source_psu_voltage(voltage, self.address)

    isEditable = True
    unit = "V"

class Source_psu_set_current(EM_parameter):
    def set(self, current):
        return em.set_source_psu_current(current, self.address)

    isEditable = True
    unit = "A"

class Source_psu_measured_voltage(EM_parameter):
    def read(self):
        return em.get_source_psu_voltage(self.address)

    isEditable = False
    unit = "V"

class Source_psu_measured_current(EM_parameter):
    def read(self):
        return em.get_source_psu_current(self.address)

    isEditable = False
    unit = "A"

class Voltmeter_voltage(EM_parameter):
    def read(self):
        return em.get_voltmeter_voltage(self.channel, self.address)

    isEditable = False
    unit = "V"
    n_channels = 4

class Voltmeter_raw(EM_parameter):
    def read(self):
        return em.get_voltmeter_raw(self.channel, self.address)

    isEditable = False
    unit = "counts"
    n_channels = 4

class Voltmeter_avglen(EM_parameter):
    def set(self, avglen):
        em.set_voltmeter_avglen(self.channel, avglen, self.address)

    isEditable = True
    unit = "samples"
    n_channels = 4

parameter_class_dict = {"pid_p": Pid_p,
                        "pid_i": Pid_i,
                        "pid_d": Pid_d,
                        "pid_state": Pid_state,
                        "pid_setpoint": Pid_setpoint,
                        "generator_amplitude": Generator_amplitude,
                        "generator_frequency": Generator_frequency,
                        "hvpsu_voltage": Hvpsu_voltage,
                        "hvpsu_raw": Hvpsu_raw,
                        "source_psu_set_voltage": Source_psu_set_voltage,
                        "source_psu_set_current": Source_psu_set_current,
                        "source_psu_measured_voltage": Source_psu_measured_voltage,
                        "source_psu_set_current": Source_psu_set_current,
                        "source_psu_measured_voltage": Source_psu_measured_voltage,
                        "source_psu_set_current": Source_psu_set_current,
                        "source_psu_measured_voltage": Source_psu_measured_voltage,
                        "source_psu_measured_current": Source_psu_measured_current,
                        "voltmeter_voltage": Voltmeter_voltage,
                        "voltmeter_raw": Voltmeter_raw,
                        "voltmeter_avglen": Voltmeter_avglen}

class EuroController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config
        self.params = {}
        self.parseConfig()
        

    @staticmethod
    def getName():
        return "EuroMeasure"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        isEditable = {}
        for key in parameter_class_dict.keys():
            isEditable[key] = parameter_class_dict[key].isEditable
        return isEditable
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        unit = {}
        for key in parameter_class_dict.keys():
            unit[key] = parameter_class_dict[key].unit
        return unit

    @staticmethod
    def getMinDict() -> dict[str, float]:
        min = {}
        for key in parameter_class_dict.keys():
            min[key] = parameter_class_dict[key].min
        return min

    @staticmethod
    def getMaxDict() -> dict[str, float]:
        max = {}
        for key in parameter_class_dict.keys():
            max[key] = parameter_class_dict[key].max
        return max

    def parseConfig(self):
        if "port" in self.config.json:
            self.port = self.config.json["port"]
        else:
            logging.error("No port specified")
            return False
        for param in self.config.params:
            parameter_class = parameter_class_dict[param.type]
            self.params[param.name] = parameter_class(param.json.get("channel", None), param.json.get("address", None))
        return True


    def connect(self) -> bool:
        em.connect(self.port)
        return True

    def adjust(self, param: str, value: float) -> None:
        self.params[param].adjust(value)

    def enable(self, state: bool):
        pass

    def read(self, param: str) -> float:
        return(self.params[param].read())



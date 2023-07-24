import serial
import time
import logging

from config import ControllerConfig, ParamConfig
from controllers.controller import Controller

class EuroController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config
        self.device = None
        self.port = None

        self.pidParam = [None]
        self.genAmplitudeParam = [None, None]
        self.genFreqParam = [None, None]
        self.voltmeterVoltageParam = [None, None, None, None]
        self.HVPSUVoltageParam = [None, None, None, None]
        self.SourcePSUSetVoltParam = None
        self.SourcePSUSetCurrParam = None
        self.SourcePSUMeasVoltParam = None
        self.SourcePSUMeasCurrParam = None


        self.pid = 0
        self.genAmplitude = [0, 0]
        self.genFreq = [0, 0]
        self.voltmeterVoltage = [0, 0, 0, 0]
        self.HVPSUVoltage = [0, 0, 0, 0]
        self.SourcePSUSetVolt = 0
        self.SourcePSUSetCurr = 0
        self.SourcePSUMeasVolt = 0
        self.SourcePSUMeasCurr = 0

        self.nChannelsDict = {
            "pid": 1,
            "generator_amplitude": 2,
            "generator_frequency": 2,
            "voltmeter_voltage": 4,
            "HVPSU_voltage": 4,
            "source_PSU_set_voltage": 1,
            "source_PSU_set_current": 1,
            "source_PSU_measured_voltage": 1,
            "source_PSU_measured_current": 1
        }


        self.parseConfig()

    @staticmethod
    def getName():
        return "EuroMeasure"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "pid": True,
            "generator_amplitude": True,
            "generator_frequency": True,
            "voltmeter_voltage": False,
            "HVPSU_voltage": True,
            "source_PSU_set_voltage": True,
            "source_PSU_set_current": True,
            "source_PSU_measured_voltage": False,
            "source_PSU_measured_current": False
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "pid": "V",
            "generator_amplitude": "Vpp",
            "generator_frequency": "Hz",
            "voltmeter_voltage": "V",
            "HVPSU_voltage": "V",
            "source_PSU_set_voltage": "V",
            "source_PSU_set_current": "I",
            "source_PSU_measured_voltage": "V",
            "source_PSU_measured_current": "I"
        }

    @staticmethod
    def getMinDict() -> dict[str, float]:
        return {
            "pid": 0,
            "generator_amplitude": 0,
            "generator_frequency": 0,
            "voltmeter_voltage": -12,
            "HVPSU_voltage": -250,
            "source_PSU_set_voltage": 0,
            "source_PSU_set_current": 0,
            "source_PSU_measured_voltage": 0,
            "source_PSU_measured_current": 0
        }

    @staticmethod
    def getMaxDict() -> dict[str, float]:
        return {
            "pid": 4,
            "generator_amplitude": 6,
            "generator_frequency": 75e6,
            "voltmeter_voltage": 12,
            "HVPSU_voltage": 65535,
            "source_PSU_set_voltage": 3000, #to be checked
            "source_PSU_set_current": 2e-3, #to be checked
            "source_PSU_measured_voltage": 2000,
            "source_PSU_measured_current": 2e-3
        }

    def parseConfig(self):
        if "port" in self.config.json:
            self.port = self.config.json["port"]
        else:
            logging.error("No port specified")
            return False
        for param in self.config.params:
            if param.type in self.nChannelsDict.keys():
                if self.nChannelsDict[param.type] == 1:
                    if param.type == "source_PSU_set_voltage":
                        self.SourcePSUSetVoltParam = param.name
                    elif param.type == "source_PSU_measured_voltage":
                        self.SourcePSUMeasVoltParam = param.name
                    elif param.type == "source_PSU_set_current":
                        self.SourcePSUSetCurrParam = param.name
                    elif param.type == "source_PSU_measured_current":
                        self.SourcePSUMEasCurrParam = param.name
                    elif param.type == "pid":
                        self.pidParam = param.name
                    else:
                        logging.error(f"Invalid number of channels for {param}")
                else:
                    if param.json.get("channel", 0) in range(1, self.nChannelsDict[param.type]+1):
                        if param.type == "generator_amplitude":
                            self.genAmplitudeParam[param.json["channel"]-1] = param.name
                        elif param.type == "generator_frequency":
                            self.genFreqParam[param.json["channel"]-1] = param.name
                        elif param.type == "voltmeter_voltage":
                            self.voltmeterVoltageParam[param.json["channel"]-1] = param.name
                        elif param.type == "HVPSU_voltage":
                            self.HVPSUVoltageParam[param.json["channel"]-1] = param.name
                    else:
                        logging.error(f"Invalid number of channels for {param}")
            else:
                logging.error(f"Invalid parameter {param}")
        return True


    def connect(self) -> bool:
        if self.device is None:
            self.device = serial.Serial(self.port, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=5)
            return True
        else:
            return True

    def adjust(self, param: str, value: float) -> None:

        multichannelParameters = [
            (self.genAmplitudeParam, self.set_genAmplitude),
            (self.genFreqParam, self.set_genFreq),
            (self.HVPSUVoltageParam, self.set_HVPSUVoltage)
        ]

        monochannelParameters = [
            (self.pidParam, self.setPid),
            (self.SourcePSUSetVoltParam, self.set_SourcePSUSetVolt),
            (self.SourcePSUSetCurrParam, self.set_SourcePSUSetCurr)
        ]

        for multichannelParam in multichannelParameters:
            if param in multichannelParam[0]:
                multichannelParam[1](value, multichannelParam[0].index(param))
        
        for monochannelParam in monochannelParameters:
            if monochannelParam[0] == param:
                monochannelParam[1](value)

    def send_command(self, command):
        cmd = command + '\n'
        logging.debug(f"Command sent: {cmd}")
        self.device.flushInput()
        self.device.write(cmd.encode())
        self.device.flushOutput()

    def send_querry(self, querry):
        cmd = querry + '\n'
        logging.debug(f"Querry sent: {cmd}")
        self.device.flushInput()
        self.device.write(cmd.encode())
        self.device.flushOutput()
        ret = self.device.readline().decode()
        logging.debug(f"Received: {ret}")
        return ret

    def set_genAmplitude(self, amplitude, channel):
        self.genAmplitude[channel] = amplitude
        self.send_command(f'GEN:SET:AMPL {channel+1} {amplitude:.4e}')

    def set_genFreq(self, frequency, channel):
        self.genFreq[channel] = frequency
        self.send_command(f'GEN:SET:FREQ {channel+1} {frequency:.4e}')

    def set_HVPSUVoltage(self, voltage, channel):
        self.HVPSUVoltage[channel] = voltage
        self.send_command(f'HVPSU:SET {channel+1} {voltage}')

    def setPid(self, value):
        self.pid = value
        self.send_command(f'PID:SET:SETPOINT {value:.4e}')
        time.sleep(0.05)

    def set_SourcePSUSetVolt(self, voltage):
        self.SourcePSUSetVolt = voltage
        self.send_command(f'SOURCE:SET {voltage:.4e}')

    def set_SourcePSUSetCurr(self, current):
        self.SourcePSUSetCurr = current
    
    def measure_voltmeterVoltage(self, channel):
        ret = self.send_querry(f'VOLT:MEAS {channel}')
        ret = float(ret.split(" ")[1])
        print(ret)
        return ret
    
    def measure_SourcePSUMeasVolt():
        return 0

    def measure_SourcePSUMeasCurr():
        return 0

    def enable(self, state: bool):
        pass

    def read(self, param: str) -> float:
        if param in self.voltmeterVoltageParam:
            return self.measure_voltmeterVoltage(self.voltmeterVoltageParam.index(param)+1)
        if param == self.SourcePSUMeasVolt:
            return self.measure_SourcePSUMeasVolt()
        if param == self.SourcePSUMeasCurr:
            return self.measure_SourcePSUMeasCurr()

        multichannelParameters = [
            (self.genAmplitudeParam, self.genAmplitude),
            (self.genFreqParam, self.genFreq),
            (self.HVPSUVoltageParam, self.HVPSUVoltage)
        ]

        monochannelParameters = [
            (self.pidParam, self.pid),
            (self.SourcePSUSetVoltParam, self.SourcePSUSetVolt),
            (self.SourcePSUSetCurrParam, self.SourcePSUSetCurr)
        ]

        for multichannelParam in multichannelParameters:
            if param in multichannelParam[0]:
                return multichannelParam[1][multichannelParam[0].index(param)]
        
        for monochannelParam in monochannelParameters:
            if monochannelParam[0] == param:
                return monochannelParam[1]

        logging.error(f"Invalid param name {param}")
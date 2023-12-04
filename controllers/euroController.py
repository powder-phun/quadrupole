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

        self.pidSetpointParam = None
        self.pidEnableParam = None
        self.pidPParam = None
        self.pidIParam = None
        self.pidDParam = None
        self.genAmplitudeParam = [None, None]
        self.genFreqParam = [None, None]
        self.voltmeterVoltageParam = [None, None, None, None]
        self.HVPSUVoltageParam = [None, None, None, None]
        self.SourcePSUSetVoltParam = None
        self.SourcePSUSetCurrParam = None
        self.SourcePSUMeasVoltParam = None
        self.SourcePSUMeasCurrParam = None


        self.pidSetpoint = 0
        self.pidEnabled = False
        self.pidP = 10
        self.pidI = 1000
        self.pidD = 0
        self.genAmplitude = [0, 0]
        self.genFreq = [0, 0]
        self.voltmeterVoltage = [0, 0, 0, 0]
        self.HVPSUVoltage = [0, 0, 0, 0]
        self.SourcePSUSetVolt = 0
        self.SourcePSUSetCurr = 0
        self.SourcePSUMeasVolt = 0
        self.SourcePSUMeasCurr = 0

        self.nChannelsDict = {
            "pid_setpoint": 1,
            "pid_enable": 1,
            "pid_p": 1,
            "pid_i": 1,
            "pid_d": 1,
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
            "pid_setpoint": True,
            "pid_enable": True,
            "pid_p": True,
            "pid_i": True,
            "pid_d": True,
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
            "pid_setpoint": "V",
            "pid_enable": "-",
            "pid_p": "-",
            "pid_i": "-",
            "pid_d": "-",
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
            "pid_setpoint": 0,
            "pid_enable": 0,
            "pid_p": 0,
            "pid_i": 0,
            "pid_d": 0,
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
            "pid_setpoint": 4,
            "pid_enable": 1,
            "pid_p": 1e9,
            "pid_i": 1e9,
            "pid_d": 1e9,
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
                        self.SourcePSUMeasCurrParam = param.name
                    elif param.type == "pid_setpoint":
                        self.pidSetpointParam = param.name
                    elif param.type == "pid_enable":
                        self.pidEnableParam = param.name
                    elif param.type == "pid_p":
                        self.pidPParam = param.name
                    elif param.type == "pid_i":
                        self.pidIParam = param.name
                    elif param.type == "pid_d":
                        self.pidDParam = param.name
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
            self.device = serial.Serial(self.port, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=1, writeTimeout=1)
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
            (self.pidSetpointParam, self.setPidSetpoint),
            (self.pidEnableParam, self.setPidEnable),
            (self.pidPParam, self.setPidP),
            (self.pidIParam, self.setPidI),
            (self.pidDParam, self.setPidD),
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
        print(self.device.readline().decode())
        print(self.device.readline().decode())

    def send_querry(self, querry):
        value = None
        while value is None:
            cmd = querry + '\n'
            ret = None
            try:
                self.device.flushInput()
                self.device.write(cmd.encode())
                logging.debug(f"Querry sent: {cmd}")
                self.device.flushOutput()
                time.sleep(0.01)
                ret = self.device.readline().decode()
                self.device.readline().decode()
                logging.debug(f"Received: {ret}")
            except:
                self.device.close()
                time.sleep(2)
                self.device = serial.Serial(self.port, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=1, writeTimeout=1)
            try:
                value = float(ret)
            except:
                time.sleep(1)
                try:
                    if "ERROR" in ret:
                        logging.info("Error received: %s", self.device.readline().decode())
                except:
                    logging.error("Failed to read error")
        return value

    def set_genAmplitude(self, amplitude, channel):
        self.genAmplitude[channel] = amplitude
        self.send_command(f'GEN:VOLTAGE {channel+1} {amplitude:.4e}')

    def set_genFreq(self, frequency, channel):
        self.genFreq[channel] = frequency
        self.send_command(f'GEN:FREQUENCY {channel+1} {frequency:.4e}')

    def set_HVPSUVoltage(self, voltage, channel):
        print( voltage )
        self.HVPSUVoltage[channel] = voltage
        self.send_command(f'HVPSU:SET {channel+1} {voltage:.4e}')

    def setPidSetpoint(self, value):
        self.pidSetpoint = value
        self.send_command(f'PID:SETPOINT {value:.4e}')
        time.sleep(0.05)

    def setPidEnable(self, value):
        if value <= 0.5:
            self.pidEnabled = False
            self.send_command(f'PID:DISABLE')
        else:
            self.pidEnabled = True
            self.send_command(f'PID:ENABLE')

    def setPidP(self, value):
        self.pidP = value
        self.send_command(f'PID:SET P {value:.4e}')

    def setPidI(self, value):
        self.pidI = value
        self.send_command(f'PID:SET I {value:.4e}')

    def setPidD(self, value):
        self.pidD = value
        self.send_command(f'PID:SET D {value:.4e}')

    def set_SourcePSUSetVolt(self, voltage):
        self.SourcePSUSetVolt = voltage
        self.send_command(f'SOURCE:SET {voltage:.4e}')

    def set_SourcePSUSetCurr(self, current):
        self.SourcePSUSetCurr = current
        self.send_command(f'SOURCE:SET:CURRENT {current:.4e}')
    
    def measure_voltmeterVoltage(self, channel):
        ret = self.send_querry(f'VOLT:MEASURE {channel-1}')
        ret = float(ret)
        print(ret)
        return ret
    
    def measure_SourcePSUMeasVolt(self):
        ret = self.send_querry(f'SOURCE:READ:VOLTAGE')
        print(ret)
        ret = float(ret)
        return ret

    def measure_SourcePSUMeasCurr(self):
        ret = self.send_querry(f'SOURCE:READ:CURRENT')
        ret = float(ret)
        return ret

    def enable(self, state: bool):
        pass

    def read(self, param: str) -> float:
        if param in self.voltmeterVoltageParam:
            return self.measure_voltmeterVoltage(self.voltmeterVoltageParam.index(param)+1)
        if param == self.SourcePSUMeasVoltParam:
            return self.measure_SourcePSUMeasVolt()
        if param == self.SourcePSUMeasCurrParam:
            return self.measure_SourcePSUMeasCurr()

        multichannelParameters = [
            (self.genAmplitudeParam, self.genAmplitude),
            (self.genFreqParam, self.genFreq),
            (self.HVPSUVoltageParam, self.HVPSUVoltage)
        ]

        monochannelParameters = [
            (self.pidSetpointParam, self.pidSetpoint),
            (self.pidEnableParam, self.pidEnabled),
            (self.pidPParam, self.pidP),
            (self.pidIParam, self.pidI),
            (self.pidDParam, self.pidD),
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
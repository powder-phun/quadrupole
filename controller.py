import pyvisa


class Controller:
    def __init__(self):
        self.resource_manager = pyvisa.ResourceManager()
        self.generator = None  # Tektronix
        self.meter = None  # Keithley

        self.ac_voltage = 0  # Volts
        self.dc_voltage = 0  # Volts pk-pk

        self.detector_voltage = 0  # Volts

        self.outputs_enabled = False

        self.connect()
        self.setup()

    def connect(self):
        self.generator = rm.open_resource(
            "USB0::0x0699::0x0353::1742374::INSTR")
        self.meter = rm.open_resource("GPIB0::0::INSTR")

    def setup(self):
        # Tektronix
        self.generator.write("OUTPut1:STATe OFF")
        self.generator.write("OUTPut2:STATe OFF")

        # AC Channel
        self.generator.write("SOURce1:FUNCtion:SHAPe SINusoid")
        self.generator.write("SOURce1:FREQuency:FIXed {}Hz".format(FREQUENCY))
        self.generator.write("SOURce1:VOLTage:LEVel:IMMediate:OFFSet 0mV")
        self.generator.write(
            "SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {}Vpp".format(AC_MIN))

        # DC Channel
        self.generator.write("SOURce2:FUNCtion:SHAPe DC")
        self.generator.write("SOURce2:VOLTage:LEVel:IMMediate:OFFSet 0mV")
        self.generator.write(
            "SOURce2:VOLTage:LEVel:IMMediate:AMPLitude {}Vpp".format(DC_MIN))

        # Keithley
        self.meter.write("JOX")  # Restore default settings
        self.meter.write("N0")  # Standby mode
        self.meter.write("G4,2,0X")  # Set communication format
        self.meter.write("F0,0X")  # Setup DC bias

    def disable_outputs(self):
        self.outputs_enabled = False
        self.generator.write("OUTPut1:STATe OFF")
        self.generator.write("OUTPut2:STATe OFF")
        self.meter.write("N0")

    def enable_outputs(self):
        self.outputs_enabled = True
        self.generator.write("OUTPut1:STATe ON")
        self.generator.write("OUTPut2:STATe ON")
        self.meter.write("N1")

    def set_DC_voltage(self, voltage: float):
        self.dc_voltage = voltage

        self.generator.write(
            "SOURce2:VOLTage:LEVel:IMMediate:AMPLitude {}Vpp".format(self.dc_voltage))

    def set_AC_voltage(self, voltage: float):
        self.ac_voltage = voltage

        self.generator.write(
            "SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {}Vpp".format(self.ac_voltage))

    def set_detector_voltage(self, voltage: float):
        self.detector_voltage = voltage

        self.meter.write("B{},O,OX".format(self.detector_voltage))

    def measure(self):
        val = float(keithley.read().strip())
        return val

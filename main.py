from PySide6.QtWidgets import QApplication
import sys

from gui import GUI
from controller import Controller
from parameter import ParameterID, Parameter

class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.gui = GUI()
        #self.controller = Controller()
        self.params = []
        self.init_params()
    
    def start(self):
        self.gui.show()
        self.gui.initialize(self)
        sys.exit(self.app.exec())

    def init_params(self):
        self.params.append(Parameter(ParameterID.DELAY, "Delay", "s", True, 0, 100))
        self.params.append(Parameter(ParameterID.DC, "DC", "V", True, 0, 20))
        self.params.append(Parameter(ParameterID.AC, "AC", "V", True, 0, 20))
        self.params.append(Parameter(ParameterID.PRESSURE, "Pressure", "mbar", True, 0, 1e-2))
        self.params.append(Parameter(ParameterID.CURRENT, "Ion Current", "A", False, None, None))


if __name__ == "__main__":
   m = Main()
   m.start()

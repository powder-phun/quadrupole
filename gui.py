from PySide6.QtWidgets import QMainWindow
from ui.main_window import Ui_MainWindow

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.main = None
    
    def initialize(self, main):
        self.main = main
        self.ui.paramDock.fill(self.main.params)
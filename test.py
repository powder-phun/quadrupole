from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QObject, Signal, Slot, QThread
import sys


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.executor = Executor()
        self.executorThread = QThread()
        self.executor.moveToThread(self.executorThread)

        self.executorThread.started.connect(self.executor.testSlot)
        self.executor.testSignal.connect(self.testSlot)

        self.executorThread.start()

    @Slot()
    def testSlot(self):
        print("XD")


class Executor(QObject):
    testSignal = Signal()

    def __init__(self):
        super(Executor, self).__init__()

    @Slot()
    def testSlot(self):
        self.testSignal.emit()

    @Slot()
    def connecta(self):
        print("Connecting")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec())

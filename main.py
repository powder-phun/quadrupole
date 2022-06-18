from PySide6.QtWidgets import QApplication
import sys
from gui import Main

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec())

from PySide6.QtGui import QRegularExpressionValidator

FLOAT_VALIDATOR = QRegularExpressionValidator("[+-]?[0-9]+[.,]?[0-9]*(e[+-]?[0-9]+)?")
from PySide6.QtWidgets import QWidget, QCheckBox
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QAbstractSeries, QLineSeries
from PySide6.QtCore import Qt, QMargins, Signal, Slot
from PySide6.QtGui import QPainter, QMouseEvent

from ui.three_d_chart import Ui_threeDChart

from parameter import ParameterID, Parameter
from utils import DataPacket, FLOAT_VALIDATOR


class ThreeDChart(QWidget):
    def __init__(self, parent=None):
        super(ThreeDChart, self).__init__(parent)
        self.ui = None
        self.setupUi()

        self.xMin: float = 0
        self.xMax: float = 1
        self.yMin: float = -1
        self.yMax: float = 1
        self.zMin: float = 0
        self.zMax: float = 1

        self.data: dict[ParameterID, list[float]] = {}
        self.params: dict[ParameterID, Parameter] = None

    def setupUi(self):
        self.ui = Ui_threeDChart()
        self.ui.setupUi(self)

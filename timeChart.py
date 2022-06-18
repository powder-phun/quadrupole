from PySide6.QtWidgets import QWidget, QCheckBox
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QLineSeries
from PySide6.QtCore import Qt, QMargins

from ui.time_chart import Ui_timeChart

from parameter import ParameterID, Parameter
from utils import DataPacket

TIMESTAMP = "Timestamp"


class TimeChart(QWidget):
    def __init__(self, parent=None):
        super(TimeChart, self).__init__(parent)
        self.ui = Ui_timeChart()
        self.ui.setupUi(self)
        self.chart = QChart()
        self.chartView = QChartView(self.chart)

        self.series: dict[ParameterID, QLineSeries] = {}

        self.xAxis: QValueAxis = QValueAxis()
        self.yAxis: QValueAxis = QValueAxis()

        self.xMin: float = 0
        self.xMax: float = 1
        self.yMin: float = -1
        self.yMax: float = 1

        self.timestamps: [float] = []

        self.initialize()

        self.checkboxes: dict[ParameterID, QCheckBox] = {}

        self.params: dict[ParameterID, Parameter] = None

    def initialize(self):
        self.chartView.setRubberBand(QChartView.RectangleRubberBand)
        self.ui.horizontalLayout.replaceWidget(self.ui.chart, self.chartView)

        self.chart.setMargins(QMargins(0, 0, 0, 0))

        self.ui.resetButton.clicked.connect(self.chart.zoomReset)
        self.chart.addAxis(self.xAxis, Qt.AlignBottom)
        self.chart.addAxis(self.yAxis, Qt.AlignLeft)
        self.xAxis.setLabelFormat("%.2f")
        self.yAxis.setLabelFormat("%.2f")

        self.chart.legend().setVisible(False)
        self.chart.layout().setContentsMargins(0, 0, 0, 0)

    def setup(self, params: dict[ParameterID, Parameter]):
        self.params = params
        for identifier, param in params.items():
            self.series[identifier] = QLineSeries()
            self.chart.addSeries(self.series[identifier])
            self.series[identifier].attachAxis(self.xAxis)
            self.series[identifier].attachAxis(self.yAxis)
            self.series[identifier].setName(param.name)
            self.series[identifier].setVisible(False)

            self.checkboxes[identifier] = QCheckBox(param.name)
            self.ui.checkboxLayout.addWidget(self.checkboxes[identifier])
            self.checkboxes[identifier].setStyleSheet(
                "QCheckBox {background-color:"
                + self.series[identifier].color().name()
                + "}"
            )
            self.checkboxes[identifier].clicked.connect(
                (
                    lambda identifier: lambda value: self.checkboxClicked(
                        identifier, value
                    )
                )(identifier)
            )

            self.yMin = min(self.yMin, param.minimum)
            self.yMax = max(self.yMax, param.maximum)

        self.yAxis.setRange(self.yMin, self.yMax)

    def addData(self, packet: DataPacket):
        self.timestamps.append(packet.timestamp)
        if self.ui.scrollCheckbox.isChecked() and len(self.timestamps) > 1:
            self.xMin += self.timestamps[-1] - self.timestamps[-2]
            self.xMax += self.timestamps[-1] - self.timestamps[-2]
            self.xAxis.setRange(self.xMin, self.xMax)
        if self.ui.scaleCheckbox.isChecked():
            self.xMin = 0
            self.xMax = self.timestamps[-1]
            self.xAxis.setRange(self.xMin, self.xMax)

        for identifier, value in packet.data.items():
            self.series[identifier].append(packet.timestamp, value)

    def checkboxClicked(self, param, value):
        self.series[param].setVisible(value)

        self.yMin = 1e20
        self.yMax = -1e20

        for param, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                self.yMin = min(self.yMin, self.params[param].minimum)
                self.yMax = max(self.yMax, self.params[param].maximum)

        self.yAxis.setRange(self.yMin, self.yMax)

    def clear(self):
        for series in self.series.values():
            series.clear()

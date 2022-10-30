from PySide6.QtCharts import QScatterSeries
from PySide6.QtCharts import QLineSeries


from customChart import CustomChart
from ui.two_d_chart import Ui_twoDChart
from utils import DataPacket
from parameter import Parameter
from queue import Queue
import logging

class TwoDChart(CustomChart):
    def __init__(self, parent=None):
        super(TwoDChart, self).__init__(parent)
        self.selected = None

        self.points = 5000

    def setupUi(self):
        self.ui = Ui_twoDChart()
        self.ui.setupUi(self)

        self.ui.horizontalLayout.replaceWidget(self.ui.chart, self.chartView)

    def setup(self, params: dict[str, str]):
        super(TwoDChart, self).setup(params)

        for param in self.params.values():
            self.ui.xAxisCombobox.addItem(param.name)
        self.selected = self.ui.xAxisCombobox.currentText()

        self.ui.xAxisCombobox.currentTextChanged.connect(self.parameterChanged)
        self.ui.pointsSpinBox.valueChanged.connect(self.pointsChanged)

        logging.debug("Setup complete")

    def parameterChanged(self, text):
        self.selected = text

        # Clear series but not the data
        for series in self.series.values():
            series.clear()

        for identifier in self.params.keys():
            for i in range(len(self.data[identifier])):
                self.series[identifier].append(self.data[self.selected][i], self.data[identifier][i])

        self.scale()

    def pointsChanged(self, points):
        self.points = points
        for series in self.series.values():
            while series.count() > self.points:
                series.remove(0)

    def updateSeries(self, packet: DataPacket()):
        for identifier in packet.data.keys():
            self.series[identifier].append(self.data[self.selected][-1], self.data[identifier][-1])
            if self.series[identifier].count() > self.points:
                self.series[identifier].remove(0)

    def createSeries(self):
        series = QScatterSeries()
        series.setMarkerSize(10)
        return series

    def scale(self, force=False):
        # Autoscaling x if selected
        if self.ui.scaleXCheckbox.isChecked() or force:
            self.xMin = min(self.data[self.selected])
            self.xMax = max(self.data[self.selected])
            x = self.xMax - self.xMin
            # Fix for bug when setting scale with the same or reversed numbers
            if x<=0: x = 1
            self.xMax += 0.1 * x
            self.xMin -= 0.1 * x

            print(self.data[self.selected])

            self.updateXRange()
            logging.debug("Rescaling x")

        # Autoscaling y if selected
        if self.ui.scaleYCheckbox.isChecked() or force:
            self.yMin = 1e20
            self.yMax = -1e20
            for param, checkbox in self.checkboxes.items():
                if checkbox.isChecked():
                    for point in self.series[param].points():
                        self.yMin = min(self.yMin, point.y())
                        self.yMax = max(self.yMax, point.y())


            y = self.yMax - self.yMin
            # Fix for bug when setting scale with the same or reversed numbers
            if y<=0: y=1
            self.yMax += 0.1 * y
            self.yMin -= 0.1 * y

            self.updateYRange()
            logging.debug("Rescaling y")


from PySide6.QtCharts import QScatterSeries


from customChart import CustomChart
from ui.two_d_chart import Ui_twoDChart
from utils import DataPacket
from parameter import ParameterID, Parameter

class TwoDChart(CustomChart):
    def __init__(self, parent=None):
        super(TwoDChart, self).__init__(parent)
        self.selected = None

    def setupUi(self):
        self.ui = Ui_twoDChart()
        self.ui.setupUi(self)

        self.ui.horizontalLayout.replaceWidget(self.ui.chart, self.chartView)

    def setup(self, params: dict[ParameterID, Parameter]):
        super(TwoDChart, self).setup(params)

        for param in self.params.values():
            self.ui.xAxisCombobox.addItem(param.name)
        self.selected = next(param.id for param in self.params.values() if param.name == self.ui.xAxisCombobox.currentText())

        self.ui.xAxisCombobox.currentTextChanged.connect(self.parameterChanged)

    def parameterChanged(self, text):
        self.selected = next(param.id for param in self.params.values() if param.name == text)

        self.clear()

        for identifier in self.params.keys():
            for i in range(len(self.data[identifier])):
                self.series[identifier].append(self.data[self.selected][i], self.data[identifier][i])

    def updateSeries(self, packet: DataPacket()):
        for identifier in packet.data.keys():
            self.series[identifier].append(self.data[self.selected][-1], self.data[identifier][-1])

    def createSeries(self):
        return QScatterSeries()

    def scale(self, force=False):
        # Autoscaling x if selected
        if self.ui.scaleXCheckbox.isChecked() or force:
            self.xMin = min(self.data[self.selected])
            self.xMax = max(self.data[self.selected])
            self.updateXRange()

        # Autoscaling y if selected
        if self.ui.scaleYCheckbox.isChecked() or force:
            self.yMin = 1e20
            self.yMax = -1e20
            for param, checkbox in self.checkboxes.items():
                if checkbox.isChecked():
                    for point in self.series[param].points():
                        self.yMin = min(self.yMin, point.y())
                        self.yMax = max(self.yMax, point.y())

            self.updateYRange()


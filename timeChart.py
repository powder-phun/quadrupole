from customChart import CustomChart
from ui.time_chart import Ui_timeChart
from utils import DataPacket

class TimeChart(CustomChart):
    def setupUi(self):
        self.ui = Ui_timeChart()
        self.ui.setupUi(self)
        
        self.ui.horizontalLayout.replaceWidget(self.ui.chart, self.chartView)

    def updateSeries(self, packet: DataPacket()):
        for identifier in packet.data.keys():
            self.series[identifier].append(self.timestamps[-1], self.data[identifier][-1])

    def scale(self, force=False):
        # Scrolling if scrolling selected
        if self.ui.scrollCheckbox.isChecked() and len(self.timestamps) > 1:
            self.xMin += self.timestamps[-1] - self.timestamps[-2]
            self.xMax += self.timestamps[-1] - self.timestamps[-2]
            self.updateXRange()

        # Autoscaling x if selected
        if self.ui.scaleXCheckbox.isChecked() or force:
            self.xMin = 0
            self.xMax = self.timestamps[-1]
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


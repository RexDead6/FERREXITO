from PyQt5 import QtCore, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries

class Dialog_producto_grafico(QtWidgets.QDialog):
    
    def __init__(self, *args, **kwargs):
        super(Dialog_producto_grafico, self).__init__()
        self.mainApp = kwargs["args"][0]
        self.id_producto = kwargs["args"][1]
        self.create_widgets()

    def create_widgets(self):
        self.setModal(True)
        self.resize(800, 600)
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        titulo = QtWidgets.QLabel("VENTAS POR DIA")
        titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        data_for_date = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO_POR_DIA(self.id_producto)
        max_value = 0
        dataChart = {}
        for data in data_for_date:
            format_date = data[0][8:10]+"/"+data[0][5:7]+"/"+data[0][:4]
            if not format_date in dataChart:
                dataChart[format_date] = 0
            dataChart[format_date] += int(data[1])

            if dataChart[format_date] > max_value: max_value = dataChart[format_date]

        newDataChart = {}
        for key in dataChart.keys():
            newDataChart[str(dataChart[key])+"\n"+key] = dataChart[key]

        set1 = QBarSet("producto")
        set1.append(newDataChart.values())

        series = QBarSeries()
        series.append(set1)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        labels = newDataChart.keys()

        axisX = QBarCategoryAxis()
        axisX.append(labels)

        axisY = QValueAxis()
        axisY.setRange(0, max_value)

        chart.addAxis(axisX, QtCore.Qt.AlignBottom)
        chart.addAxis(axisY, QtCore.Qt.AlignLeft)

        chart.legend().setVisible(False)

        chartView = QChartView(chart)

        layout_main.addWidget(chartView)

        self.show()
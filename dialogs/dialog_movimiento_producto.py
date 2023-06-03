from PyQt5 import QtWidgets, QtCore, QtGui

class Dialog_movimiento_producto(QtWidgets.QDialog):

    mainApp = None
    id_producto = None
    movimientos = []
    temp_movimientos = []
    producto = None

    def __init__(self, mainApp, id_producto):
        super(Dialog_movimiento_producto, self).__init__()
        self.mainApp = mainApp
        self.movimientos = self.mainApp.DATA_SYSTEM.SELECT_MOVIMIENTO_PRODUCTO(id_producto)
        self.temp_movimientos = self.movimientos
        self.producto = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO_BY_ID(id_producto)
        self.create_widgets()
        self.setDataTable()

    def setDataTable(self):
        if self.temp_movimientos == [] or self.temp_movimientos == None: return None

        self.table_movimientos.setRowCount(0)
        for i in range(len(self.temp_movimientos)):
            self.table_movimientos.insertRow(0)
            self.table_movimientos.setItem(0, 0, QtWidgets.QTableWidgetItem(self.temp_movimientos[i][0]))
            
            tipo = "VENTA"
            if (self.temp_movimientos[i][1] == '2'): tipo = "COMPRA"
            if (self.temp_movimientos[i][1] == '3'): tipo = "DEVOLUCIÓN"
            if (self.temp_movimientos[i][1] == '4'): tipo = "AJUSTE (-)"
            if (self.temp_movimientos[i][1] == '5'): tipo = "AJUSTE (+)"

            self.table_movimientos.setItem(0, 1, QtWidgets.QTableWidgetItem(tipo))
            self.table_movimientos.setItem(0, 2, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(self.temp_movimientos[i][2])))
            self.table_movimientos.setItem(0, 3, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(self.temp_movimientos[i][3])))
            self.table_movimientos.setItem(0, 4, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(self.temp_movimientos[i][4])))
            self.table_movimientos.setItem(0, 5, QtWidgets.QTableWidgetItem(self.mainApp.formato_fecha(self.temp_movimientos[i][5])))

        self.table_movimientos.resizeRowsToContents()
        self.table_movimientos.resizeColumnsToContents()

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)
        self.resize(900, 600)

        titulo = QtWidgets.QLabel("MOVIMIENTOS DE: "+self.producto[2])
        titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        layout_horizontal = QtWidgets.QHBoxLayout()
        layout_main.addLayout(layout_horizontal)

        self.table_movimientos = QtWidgets.QTableWidget()
        self.table_movimientos.setFont(self.mainApp.font_m)
        self.table_movimientos.setColumnCount(6)
        self.table_movimientos.setHorizontalHeaderLabels(['REFERENCIA', 'TIPO', 'PRECIO UNITARIO', 'CANTIDAD', 'PRECIO TOTAL', 'FECHA'])
        self.table_movimientos.resizeColumnsToContents()
        self.table_movimientos.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        layout_horizontal.addWidget(self.table_movimientos)

        layout_botones = QtWidgets.QVBoxLayout()
        layout_horizontal.addLayout(layout_botones)
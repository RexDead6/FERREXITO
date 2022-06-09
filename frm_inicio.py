from PyQt5 import QtWidgets, QtCore, QtGui

class Frame_inicio(QtWidgets.QFrame):

    mainApp = None

    def __init__(self, *args, **kwargs):
        super(Frame_inicio, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

    def add_data_table(self):
        data = self.mainApp.DATA_SYSTEM.SELECT_ALL_PRODUCTO()
        self.rellena_tabla(data)

    def rellena_tabla(self, data):
        if data == None: return None

        self.table_productos.setRowCount(0)
        for i in range(len(data)):
            if int(data[i][3]) > int(data[i][5]): continue
            self.table_productos.insertRow(0)
            self.table_productos.setItem(0,0, QtWidgets.QTableWidgetItem(data[i][0]))
            self.table_productos.setItem(0,1, QtWidgets.QTableWidgetItem(data[i][1]))
            self.table_productos.setItem(0,2, QtWidgets.QTableWidgetItem(data[i][2]))
            self.table_productos.setItem(0,3, QtWidgets.QTableWidgetItem(data[i][3]))
            self.table_productos.setItem(0,4, QtWidgets.QTableWidgetItem(data[i][5]))
            self.table_productos.setItem(0,5, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(float(data[i][4]))))

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        titulo = QtWidgets.QLabel("FERREXITO")
        titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        titulo1 = QtWidgets.QLabel("PRODUCTOS POR REPONER")
        titulo1.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo1)
        layout_main.setAlignment(titulo1, QtCore.Qt.AlignHCenter)

        layout_horizontal = QtWidgets.QHBoxLayout()
        layout_main.addLayout(layout_horizontal)

        self.table_productos = QtWidgets.QTableWidget()
        self.table_productos.setFont(self.mainApp.font_m)
        self.table_productos.setColumnCount(6)
        self.table_productos.setHorizontalHeaderLabels(['ID', 'CÓDIGO', 'NOMBRE', 'EXISTENCIA', 'ALERTA', 'PRECIO'])
        self.table_productos.resizeColumnsToContents()
        self.table_productos.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        layout_horizontal.addWidget(self.table_productos)

        layout_botones = QtWidgets.QVBoxLayout()
        layout_horizontal.addLayout(layout_botones)

        label_titulo = QtWidgets.QLabel("ACCESOS RÁPIDOS")
        label_titulo.setFont(self.mainApp.font_m)
        

        self.btn_facturacion = QtWidgets.QPushButton("FACTURACION")
        self.btn_facturacion.setFont(self.mainApp.font_m)
        self.btn_facturacion.clicked.connect(lambda: self.mainApp.change_frame("venta"))
        layout_botones.addWidget(self.btn_facturacion)
        layout_botones.setAlignment(self.btn_facturacion, QtCore.Qt.AlignTop)
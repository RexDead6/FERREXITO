from PyQt5 import QtWidgets, QtCore, QtGui

class Tabla_productos(QtWidgets.QFrame):

    mainApp = None

    def __init__(self, *args, **kwargs):
        super(Tabla_productos, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

    def add_data_table(self):
        data = self.mainApp.DATA_SYSTEM.SELECT_ALL_PRODUCTO()
        self.rellena_tabla(data)

    def input_buscar(self):
        data = self.mainApp.DATA_SYSTEM.LIKE_SENTENCE_PRODUCTO("SELECT * FROM producto WHERE codigo LIKE '%{}%' OR descripcion LIKE '%{}%';".format(self.txt_buscar.text(), self.txt_buscar.text()))
        self.rellena_tabla(data)

    def rellena_tabla(self, data):
        if data == None: return None

        self.table_productos.setRowCount(0)
        for i in range(len(data)):
            self.table_productos.insertRow(0)
            self.table_productos.setItem(0,0, QtWidgets.QTableWidgetItem(data[i][0]))
            self.table_productos.setItem(0,1, QtWidgets.QTableWidgetItem(data[i][1]))
            self.table_productos.setItem(0,2, QtWidgets.QTableWidgetItem(data[i][2]))
            self.table_productos.setItem(0,3, QtWidgets.QTableWidgetItem(data[i][3]))
            self.table_productos.setItem(0,4, QtWidgets.QTableWidgetItem(data[i][5]))
            self.table_productos.setItem(0,5, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(float(data[i][4]))))

        self.table_productos.resizeRowsToContents()
        self.table_productos.resizeColumnsToContents()

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        titulo = QtWidgets.QLabel("PRODUCTOS")
        titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

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
        
        self.txt_buscar = QtWidgets.QLineEdit()
        self.txt_buscar.setFont(self.mainApp.font_m)
        self.txt_buscar.setMaximumWidth(200)
        self.txt_buscar.textChanged.connect(self.input_buscar)
        layout_botones.addWidget(self.txt_buscar)

        self.btn_abrir = QtWidgets.QPushButton("ABRIR")
        self.btn_abrir.setFont(self.mainApp.font_m)
        self.btn_abrir.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_abrir.setMinimumHeight(80)
        self.btn_abrir.setVisible(False)
        layout_botones.addWidget(self.btn_abrir)

        layout_botones.addStretch()
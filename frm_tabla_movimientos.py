from PyQt5 import QtWidgets, QtCore, QtGui

class Tabla_movimientos(QtWidgets.QFrame):

    mainApp = None

    def __init__(self, *args, **kwargs):
        super(Tabla_movimientos, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

    def add_data_table(self):
        data = self.mainApp.DATA_SYSTEM.SELECT_ALL_MOVIMIENTOS()
        self.rellena_tabla(data)

    def input_buscar(self):
        data = self.mainApp.DATA_SYSTEM.LIKE_SENTENCE_MOVIMIENTOS("SELECT * FROM cuerpo WHERE referencia LIKE '%{}%' OR tipo LIKE '%{}%';".format(self.txt_buscar.text(), self.mainApp.DATA_SYSTEM.format_type_mov(self.txt_buscar.text())))
        self.rellena_tabla(data)

    def rellena_tabla(self, data):
        if data == None: return None

        self.table_movimientos.setRowCount(0)
        for i in range(len(data)):
            self.table_movimientos.insertRow(0)
            self.table_movimientos.setItem(0,0, QtWidgets.QTableWidgetItem(data[i][0]))
            self.table_movimientos.setItem(0,1, QtWidgets.QTableWidgetItem(data[i][4]))
            self.table_movimientos.setItem(0,2, QtWidgets.QTableWidgetItem(self.mainApp.DATA_SYSTEM.format_type_mov(int(data[i][2]))))
            self.table_movimientos.setItem(0,3, QtWidgets.QTableWidgetItem(data[i][5]))
            self.table_movimientos.setItem(0,4, QtWidgets.QTableWidgetItem(data[i][7]))
            self.table_movimientos.setItem(0,5, QtWidgets.QTableWidgetItem(data[i][8]))

        self.table_movimientos.resizeRowsToContents()
        self.table_movimientos.resizeColumnsToContents()

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        titulo = QtWidgets.QLabel("MOVIMIENTOS")
        titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        layout_horizontal = QtWidgets.QHBoxLayout()
        layout_main.addLayout(layout_horizontal)

        self.table_movimientos = QtWidgets.QTableWidget()
        self.table_movimientos.setFont(self.mainApp.font_m)
        self.table_movimientos.setColumnCount(6)
        self.table_movimientos.setHorizontalHeaderLabels(['ID', 'REFERENCIA', 'TIPO', 'SUBTOTAL', 'IVA', 'TOTAL'])
        self.table_movimientos.resizeColumnsToContents()
        self.table_movimientos.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        layout_horizontal.addWidget(self.table_movimientos)

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
        layout_botones.addWidget(self.btn_abrir)

        layout_botones.addStretch()
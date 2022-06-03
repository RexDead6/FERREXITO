from PyQt5 import QtWidgets, QtCore, QtGui

from dialogs.dialog_personal import Dialog_personal

class Tabla_empleados(QtWidgets.QFrame):

    mainApp = None

    def __init__(self, *args, **kwargs):
        super(Tabla_empleados, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

    def open_forms(self, edit):
        self.dialog = Dialog_personal(args=self.mainApp)
        self.dialog.SET_EDIT(edit)

    def add_data_table(self):
        data = self.mainApp.DATA_SYSTEM.SELECT_ALL_USER()
        self.rellena_tabla(data)

    def input_buscar(self):
        data = self.mainApp.DATA_SYSTEM.LIKE_SENTENCE_USER("SELECT * FROM personal WHERE `C.I.` LIKE '%{}%' OR nombre LIKE '%{}%';".format(self.txt_buscar.text(), self.txt_buscar.text()))
        self.rellena_tabla(data)

    def rellena_tabla(self, data):
        if data == None: return None

        self.table_personal.setRowCount(0)
        for i in range(len(data)):
            self.table_personal.insertRow(0)
            self.table_personal.setItem(0,0, QtWidgets.QTableWidgetItem(data[i][1]))
            self.table_personal.setItem(0,1, QtWidgets.QTableWidgetItem(data[i][3]))
            self.table_personal.setItem(0,2, QtWidgets.QTableWidgetItem(data[i][2]))

        self.table_personal.resizeRowsToContents()
        self.table_personal.resizeColumnsToContents()

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        titulo = QtWidgets.QLabel("USUARIOS")
        titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        layout_horizontal = QtWidgets.QHBoxLayout()
        layout_main.addLayout(layout_horizontal)

        self.table_personal = QtWidgets.QTableWidget()
        self.table_personal.setFont(self.mainApp.font_m)
        self.table_personal.setColumnCount(3)
        self.table_personal.setHorizontalHeaderLabels(['CEDULA', 'CARGO', 'NOMBRE'])
        self.table_personal.resizeColumnsToContents()
        self.table_personal.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        layout_horizontal.addWidget(self.table_personal)

        layout_botones = QtWidgets.QVBoxLayout()
        layout_horizontal.addLayout(layout_botones)
        
        self.txt_buscar = QtWidgets.QLineEdit()
        self.txt_buscar.setFont(self.mainApp.font_m)
        self.txt_buscar.setMaximumWidth(200)
        self.txt_buscar.textChanged.connect(self.input_buscar)
        layout_botones.addWidget(self.txt_buscar)
        
        self.btn_registrar = QtWidgets.QPushButton("REGISTRAR")
        self.btn_registrar.setFont(self.mainApp.font_m)
        self.btn_registrar.setMinimumHeight(80)
        self.btn_registrar.clicked.connect(lambda: self.open_forms(False))
        layout_botones.addWidget(self.btn_registrar)

        self.btn_abrir = QtWidgets.QPushButton("EDITAR")
        self.btn_abrir.setFont(self.mainApp.font_m)
        self.btn_abrir.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_abrir.setMinimumHeight(80)
        self.btn_abrir.clicked.connect(lambda: self.open_forms(True))
        layout_botones.addWidget(self.btn_abrir)

        if self.mainApp.cargo > 0:
            self.btn_abrir.setEnabled(False)
            self.btn_registrar.setEnabled(False)

        layout_botones.addStretch()
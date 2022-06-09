from PyQt5 import QtWidgets, QtCore, QtGui

class Tabla_auditoria(QtWidgets.QFrame):

    mainApp = None

    def __init__(self, *args, **kwargs):
        super(Tabla_auditoria, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

    def add_data_table(self):
        data = self.mainApp.DATA_SYSTEM.SELECT_AUDITORIA()
        self.fill_table(data)

    def fill_table(self, data):
        if data == None: return None

        self.table_auditoria.setRowCount(0)
        for i in range(len(data)):
            
            empleado = self.mainApp.DATA_SYSTEM.SELECT_USER_BY_ID(data[i][3])

            self.table_auditoria.insertRow(0)
            self.table_auditoria.setItem(0,0, QtWidgets.QTableWidgetItem(empleado[1]))
            self.table_auditoria.setItem(0,1, QtWidgets.QTableWidgetItem(empleado[2]))
            self.table_auditoria.setItem(0,2, QtWidgets.QTableWidgetItem(data[i][1]))
            self.table_auditoria.setItem(0,3, QtWidgets.QTableWidgetItem(self.mainApp.formato_fecha(data[i][2])))

        self.table_auditoria.resizeRowsToContents()
        self.table_auditoria.resizeColumnsToContents()

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        titulo = QtWidgets.QLabel("REGISTROS DE AUDITORIA")
        titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        layout_horizontal = QtWidgets.QHBoxLayout()
        layout_main.addLayout(layout_horizontal)

        self.table_auditoria = QtWidgets.QTableWidget()
        self.table_auditoria.setFont(self.mainApp.font_m)
        self.table_auditoria.setColumnCount(4)
        self.table_auditoria.setHorizontalHeaderLabels(['CEDULA', 'NOMBRE', 'DESCRIPCION', 'FECHA'])
        self.table_auditoria.resizeColumnsToContents()
        self.table_auditoria.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        layout_horizontal.addWidget(self.table_auditoria)

        layout_botones = QtWidgets.QVBoxLayout()
        layout_horizontal.addLayout(layout_botones)
        
        self.txt_buscar = QtWidgets.QLineEdit()
        self.txt_buscar.setFont(self.mainApp.font_m)
        self.txt_buscar.setMaximumWidth(200)
        #self.txt_buscar.textChanged.connect(self.input_buscar)
        layout_botones.addWidget(self.txt_buscar)

        self.box_accion = QtWidgets.QComboBox()
        self.box_accion.addItem("SIN ESPECIFICAR")
        self.box_accion.setFont(self.mainApp.font_m)
        self.box_accion.setMaximumWidth(200)
        #self.box_accion.currentIndexChanged.connect(self.onCurrentIndexComboTipo)
        layout_botones.addWidget(self.box_accion)

        label_inicio = QtWidgets.QLabel("INICIO:")
        label_inicio.setFont(self.mainApp.font_m)
        layout_botones.addWidget(label_inicio)

        self.date_inicio = QtWidgets.QDateEdit(calendarPopup=True)
        self.date_inicio.setFont(self.mainApp.font_m)
        self.date_inicio.setDateTime(QtCore.QDateTime.currentDateTime())
        layout_botones.addWidget(self.date_inicio)

        label_fin = QtWidgets.QLabel("FIN:")
        label_fin.setFont(self.mainApp.font_m)
        layout_botones.addWidget(label_fin)

        self.date_fin = QtWidgets.QDateEdit(calendarPopup=True)
        self.date_fin.setFont(self.mainApp.font_m)
        self.date_fin.setDateTime(QtCore.QDateTime.currentDateTime())
        layout_botones.addWidget(self.date_fin)

        self.btn_buscar = QtWidgets.QPushButton("BUSCAR")
        self.btn_buscar.setFont(self.mainApp.font_m)
        layout_botones.addWidget(self.btn_buscar)

        layout_botones.addStretch()
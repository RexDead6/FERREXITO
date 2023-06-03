from PyQt5 import QtWidgets, QtCore, QtGui

class Dialog_movimiento(QtWidgets.QDialog):

    mainApp = None

    def __init__(self, mainApp):
        super(Dialog_movimiento, self).__init__()
        self.mainApp = mainApp
        self.create_widgets()
    
    def setData(self, tipo, ref):
        data = self.mainApp.DATA_SYSTEM.SELECT_CABECERA(tipo, ref)
        mov  = self.mainApp.DATA_SYSTEM.SELECT_MOVIMIENTO(ref)
        cuerpo_productos = self.mainApp.DATA_SYSTEM.SELECT_CUERPO_PRODUCTOS(mov[0])
        empleado = self.mainApp.DATA_SYSTEM.SELECT_USER_BY_ID(data[3])

        self.txt_fecha.setText(self.mainApp.formato_fecha(data[4]))
        self.txt_total.setText(self.mainApp.formato_moneda(float(mov[8])))
        self.txt_user.setText(empleado[1] + " - " + empleado[2])

        self.fill_table(cuerpo_productos)

        if tipo == "venta":
            cliente = self.mainApp.DATA_SYSTEM.SELECT_CLIENTE_BY_ID(data[9])
            self.label_ci.setText("CEDULA:")
            self.txt_ci.setText(cliente[1])
            self.txt_nombre.setText("NOMBRE:")
            self.txt_nombre.setText(cliente[2])
            self.txt_descripcion.setText("N/A")
        elif tipo == "compra":
            proveedor = self.mainApp.DATA_SYSTEM.SELECT_PROVEEDOR_BY_ID(data[8])
            self.label_ci.setText("RIF:")
            self.txt_ci.setText(proveedor[1])
            self.label_nombre.setText("RAZÓN SOCIAL:")
            self.txt_nombre.setText(proveedor[2])
            self.label_descripcion.setText("NÚMERO FACTURA:")
            self.txt_descripcion.setText(data[10])
        elif tipo == "inventario":
            self.label_ci.setText("CEDULA:")
            self.txt_ci.setText("N/A")
            self.txt_nombre.setText("NOMBRE:")
            self.txt_nombre.setText("N/A")
            self.txt_descripcion.setText(data[6])
        elif tipo == "devolucion":
            cliente = self.mainApp.DATA_SYSTEM.SELECT_CLIENTE_BY_ID(data[9])
            self.label_ci.setText("CEDULA:")
            self.txt_ci.setText(cliente[1])
            self.txt_nombre.setText("NOMBRE:")
            self.txt_nombre.setText(cliente[2])
            self.txt_descripcion.setText(data[6])
        self.show()
    
    def fill_table(self, cuerpo_productos):

        self.table_productos.setRowCount(0)
        for i in range(len(cuerpo_productos)):

            producto = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO_BY_ID(cuerpo_productos[i][1])

            self.table_productos.insertRow(0)
            self.table_productos.setItem(0,0, QtWidgets.QTableWidgetItem(producto[0]))
            self.table_productos.setItem(0,1, QtWidgets.QTableWidgetItem(producto[2]))
            self.table_productos.setItem(0,2, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(float(cuerpo_productos[i][3]))))
            self.table_productos.setItem(0,3, QtWidgets.QTableWidgetItem(cuerpo_productos[i][4]))
            self.table_productos.setItem(0,4, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(float(cuerpo_productos[i][5]))))

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        layout_main.setSpacing(0)
        self.setModal(True)
        self.setLayout(layout_main)
        self.setWindowTitle("DETALLES DE MOVIMIENTO")

        self.frame_info = QtWidgets.QFrame()
        layout_info = QtWidgets.QVBoxLayout()
        self.frame_info.setLayout(layout_info)
        layout_main.addWidget(self.frame_info)
        layout_main.setAlignment(self.frame_info, QtCore.Qt.AlignTop)

        grid_info = QtWidgets.QGridLayout()
        layout_info.addLayout(grid_info)

        self.label_ci = QtWidgets.QLabel("CEDULA:")
        self.label_ci.setFont(self.mainApp.font_m)
        grid_info.addWidget(self.label_ci, 0, 0)

        self.txt_ci = QtWidgets.QLineEdit()
        self.txt_ci.setFont(self.mainApp.font_m)
        self.txt_ci.setReadOnly(True)
        grid_info.addWidget(self.txt_ci, 1, 0)

        self.label_nombre = QtWidgets.QLabel("NOMBRE:")
        self.label_nombre.setFont(self.mainApp.font_m)
        grid_info.addWidget(self.label_nombre, 0, 1)

        self.txt_nombre = QtWidgets.QLineEdit()
        self.txt_nombre.setFont(self.mainApp.font_m)
        self.txt_nombre.setReadOnly(True)
        grid_info.addWidget(self.txt_nombre, 1, 1)

        label_fecha = QtWidgets.QLabel("FECHA/HORA")
        label_fecha.setFont(self.mainApp.font_m)
        grid_info.addWidget(label_fecha, 0, 2)

        self.txt_fecha = QtWidgets.QLineEdit()
        self.txt_fecha.setFont(self.mainApp.font_m)
        self.txt_fecha.setReadOnly(True)
        grid_info.addWidget(self.txt_fecha, 1, 2)

        self.label_descripcion = QtWidgets.QLabel("DESCRIPCIÓN:")
        self.label_descripcion.setFont(self.mainApp.font_m)
        grid_info.addWidget(self.label_descripcion, 2, 0)

        self.txt_descripcion = QtWidgets.QLineEdit()
        self.txt_descripcion.setFont(self.mainApp.font_m)
        self.txt_descripcion.setReadOnly(True)
        self.txt_descripcion.setText("N/A")
        grid_info.addWidget(self.txt_descripcion, 2, 1, 1, 2)

        label_user = QtWidgets.QLabel("EMPLEADO:")
        label_user.setFont(self.mainApp.font_m)
        grid_info.addWidget(label_user, 3, 0)

        self.txt_user = QtWidgets.QLineEdit()
        self.txt_user.setFont(self.mainApp.font_m)
        self.txt_user.setReadOnly(True)
        grid_info.addWidget(self.txt_user, 3, 1, 1, 2)

        self.table_productos = QtWidgets.QTableWidget()
        self.table_productos.setFont(self.mainApp.font_m)
        self.table_productos.setColumnCount(5)
        self.table_productos.setHorizontalHeaderLabels(['ID', 'PRODUCTO', 'P.UNITARIO', 'CANTIDAD', 'P.TOTAL'])
        self.table_productos.resizeColumnsToContents()
        self.table_productos.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_productos.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.table_productos.setMinimumWidth(600)
        layout_main.addWidget(self.table_productos)
        
        self.layout_horizontal = QtWidgets.QHBoxLayout()
        layout_main.addLayout(self.layout_horizontal)

        label_total = QtWidgets.QLabel("MONTO TOTAL:")
        label_total.setFont(self.mainApp.font_m)
        self.layout_horizontal.addWidget(label_total)

        self.txt_total = QtWidgets.QLineEdit()
        self.txt_total.setFont(self.mainApp.font_m)
        self.txt_total.setReadOnly(True)
        self.txt_total.setMinimumWidth(240)
        self.txt_total.setStyleSheet("QLineEdit {margin-top:10px}")
        self.layout_horizontal.addWidget(self.txt_total)
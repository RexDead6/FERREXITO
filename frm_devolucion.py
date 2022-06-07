from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
import jpype

import jpype

class Frame_devolucion(QtWidgets.QFrame):
    
    mainApp = None
    id_user = 0

    def __init__(self, *args, **kwargs):
        super(Frame_devolucion, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

        self.msgBox = QMessageBox()

    def search_factura(self):
        if self.txt_factura.text() == "":
            self.clear_forms()
            return None

        mov = self.mainApp.DATA_SYSTEM.SELECT_MOVIMIENTO(self.txt_factura.text())

        if mov == None:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "FACTURA INEXISTENTE")
            self.clear_forms()
            return False

        if int(mov[2]) != 1:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "FACTURA INGRESADA NO PERTENECE A UNA VENTA")
            self.clear_forms()
            return False

        data = self.mainApp.DATA_SYSTEM.SELECT_FACTURA_VENTA(mov[3])

        if int(data[1]) != 0:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "FACTURA YA HA SIDO DEVUELTA Y ANULADA")
            self.clear_forms()
            return False
        
        self.id_venta = data[0]

        cliente = self.mainApp.DATA_SYSTEM.SELECT_CLIENTE_BY_ID(data[4])
        self.txt_ci.setText(cliente[1])
        self.txt_nombre.setText(cliente[2])
        self.txt_fecha.setText(self.mainApp.formato_fecha(data[5]))
        self.txt_total.setText(self.mainApp.formato_moneda(float(mov[8])))

        cuerpo_productos = self.mainApp.DATA_SYSTEM.SELECT_CUERPO_PRODUCTOS(self.txt_factura.text())

        self.table_productos.setRowCount(0)
        for i in range(len(cuerpo_productos)):

            producto = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO_BY_ID(cuerpo_productos[i][1])

            self.table_productos.insertRow(0)
            self.table_productos.setItem(0,0, QtWidgets.QTableWidgetItem(producto[0]))
            self.table_productos.setItem(0,1, QtWidgets.QTableWidgetItem(producto[2]))
            self.table_productos.setItem(0,2, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(float(cuerpo_productos[i][3]))))
            self.table_productos.setItem(0,3, QtWidgets.QTableWidgetItem(cuerpo_productos[i][4]))
            self.table_productos.setItem(0,4, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(float(cuerpo_productos[i][5]))))
    
    def generar_devolucion(self):
        productos_raw = jpype.JArray(jpype.JInt)
        cantidad_raw  = jpype.JArray(jpype.JInt)
        precio_raw    = jpype.JArray(jpype.JFloat)
        productos = productos_raw(self.table_productos.rowCount())
        cantidad  = cantidad_raw(self.table_productos.rowCount())
        precio    = precio_raw(self.table_productos.rowCount())
        for i in range(self.table_productos.rowCount()):
            productos[i] = int(self.table_productos.item(i, 0).text())
            cantidad[i]  = int(self.table_productos.item(i, 3).text())
            precio[i]    = float(self.table_productos.item(i, 2).text().replace(".", "").replace(",", "."))

        referencia = self.mainApp.DATA_SYSTEM.MOVIMIENTO(3, self.id_venta, self.id_user, self.txt_total.text().replace(".", "").replace(",", "."), productos, cantidad, precio)
        
        if referencia != None:
            QMessageBox.information(self.msgBox, "::DEVOLUCIÓN EXITOSA::", "SU DEVOLUCION HA SIDO PROCESADA EXITOSAMENTE (REF: "+referencia+")")
        else:
            QMessageBox.critical(self.msgBox, "::ERROR::", "NO SE HA PODIDO PROCESAR SU DEVOLUION,\nINTENTE DE NUEVO")
        self.mainApp.change_frame("venta")
        self.clear_forms()

    def clear_forms(self):
        self.txt_ci.setText("")
        self.txt_factura.setText("")
        self.txt_fecha.setText("")
        self.txt_nombre.setText("")
        self.txt_total.setText("")
        self.table_productos.setRowCount(0)

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        layout_main.setSpacing(0)
        self.setLayout(layout_main)

        frame_input = QtWidgets.QFrame()
        frame_input.setMaximumHeight(60)
        layout_input = QtWidgets.QHBoxLayout()
        frame_input.setLayout(layout_input)
        layout_main.addWidget(frame_input)

        self.btn_atras = QtWidgets.QPushButton("CANCELAR")
        self.btn_atras.setFont(self.mainApp.font_m)
        self.btn_atras.setMaximumWidth(120)
        self.btn_atras.clicked.connect(lambda: self.mainApp.change_frame("venta"))
        layout_input.addWidget(self.btn_atras)

        label_input = QtWidgets.QLabel("NUMERO DE FACTURA:")
        label_input.setFont(self.mainApp.font_m)
        layout_input.addWidget(label_input)

        self.txt_factura = QtWidgets.QLineEdit()
        self.txt_factura.setFont(self.mainApp.font_m)
        self.txt_factura.setMaximumWidth(230)
        layout_input.addWidget(self.txt_factura)

        self.btn_buscar = QtWidgets.QPushButton("BUSCAR")
        self.btn_buscar.setFont(self.mainApp.font_m)
        self.btn_buscar.clicked.connect(self.search_factura)
        self.btn_buscar.setMaximumWidth(120)
        layout_input.addWidget(self.btn_buscar)

        layout_input.addStretch()

        self.frame_info = QtWidgets.QFrame()
        layout_info = QtWidgets.QVBoxLayout()
        self.frame_info.setLayout(layout_info)
        layout_main.addWidget(self.frame_info)
        layout_main.setAlignment(self.frame_info, QtCore.Qt.AlignTop)

        grid_info = QtWidgets.QGridLayout()
        layout_info.addLayout(grid_info)

        label_ci = QtWidgets.QLabel("CEDULA:")
        label_ci.setFont(self.mainApp.font_m)
        grid_info.addWidget(label_ci, 0, 0)

        self.txt_ci = QtWidgets.QLineEdit()
        self.txt_ci.setFont(self.mainApp.font_m)
        self.txt_ci.setReadOnly(True)
        grid_info.addWidget(self.txt_ci, 1, 0)

        label_nombre = QtWidgets.QLabel("NOMBRE:")
        label_nombre.setFont(self.mainApp.font_m)
        grid_info.addWidget(label_nombre, 0, 1)

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

        self.table_productos = QtWidgets.QTableWidget()
        self.table_productos.setFont(self.mainApp.font_m)
        self.table_productos.setColumnCount(5)
        self.table_productos.setHorizontalHeaderLabels(['ID', 'PRODUCTO', 'P.UNITARIO', 'CANTIDAD', 'P.TOTAL'])
        self.table_productos.resizeColumnsToContents()
        self.table_productos.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_productos.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_main.addWidget(self.table_productos)
        
        self.layout_horizontal = QtWidgets.QHBoxLayout()
        layout_main.addLayout(self.layout_horizontal)

        label_total = QtWidgets.QLabel("MONTO TOTAL:")
        label_total.setFont(self.mainApp.font_m)
        self.layout_horizontal.addWidget(label_total)

        self.txt_total = QtWidgets.QLineEdit()
        self.txt_total.setFont(self.mainApp.font_m)
        self.txt_total.setReadOnly(True)
        self.layout_horizontal.addWidget(self.txt_total)

        self.layout_horizontal.addStretch()

        self.btn_aceptar = QtWidgets.QPushButton("GENERAR DEVOLUCIÓN")
        self.btn_aceptar.setFont(self.mainApp.font_m)
        self.btn_aceptar.clicked.connect(self.generar_devolucion)
        self.btn_aceptar.setMaximumWidth(230)
        self.layout_horizontal.addWidget(self.btn_aceptar)
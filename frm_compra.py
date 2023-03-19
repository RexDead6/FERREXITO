from PyQt5 import QtCore, QtGui, QtWidgets
import jpype

from dialogs.dialog_reportView import Dialog_reportView
from class_secundary import lineAmount

class Frame_compra(QtWidgets.QFrame):
    
    mainApp = None
    id_prod = None

    def __init__(self, *args, **kwargs):
        super(Frame_compra, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

        self.txt_barcode.setFocus()

    def search_rif(self):
        if self.txt_ci.text() == "":
            self.msg.setText("INGRESE EL RIF DE SU PROVEEDOR")
            return None

        proveedor = self.mainApp.DATA_SYSTEM.SELECT_PROVEEDOR(self.txt_ci.text())

        if proveedor != None:
            self.txt_nombre.setEnabled(True)
            self.txt_nombre.setText(proveedor[2])
            self.txt_ci.setReadOnly(True)
            self.txt_nombre.setReadOnly(True)
            self.txt_barcode.setEnabled(True)
            self.txt_barcode.setFocus()
        else:
            self.msg.setText("REGISTRAR PROVEEDOR NUEVO")
            self.txt_nombre.setEnabled(True)
            self.txt_nombre.setFocus()

        self.msg.setText("")

    def enter_proveedor(self):
        if self.txt_ci.text() == "" or self.txt_nombre.text() == "":
            self.msg.setText("RELLENE TODOS LOS CAMPOS DISPONIBLES")
            return None
        
        success = self.mainApp.DATA_SYSTEM.INSERT_PROVEEDOR(self.txt_ci.text(), self.txt_nombre.text(), "00000000000")
        if success:
            msg = "INGRESE UN PRODUCTO"
            self.txt_barcode.setEnabled(True)
            self.txt_ci.setReadOnly(True)
            self.txt_nombre.setReadOnly(True)
            self.txt_barcode.setFocus()
        else:
            msg = "ERROR AL REGISTRAR, INTENTE DE NUEVO"
        self.msg.setText(msg)

    def search_barcode(self):
        if self.txt_barcode.text() == "":
            return None
        
        self.data = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO(self.txt_barcode.text())

        if self.data == None:
            self.msg.setText("PRODUCTO SIN REGISTRAR")
            self.txt_descripcion.setEnabled(True)
            self.txt_descripcion.setFocus()
        else:
            self.id_prod = self.data[0]
            self.txt_descripcion.setEnabled(True)
            self.txt_descripcion.setReadOnly(True)
            self.txt_descripcion.setText(self.data[2])
            self.txt_alerta.setEnabled(True)
            self.txt_alerta.setReadOnly(True)
            self.txt_alerta.setText(self.data[5])
            self.txt_cantidad_max.setEnabled(True)
            self.txt_cantidad_max.setReadOnly(True)
            self.txt_cantidad_max.setText(self.data[6])
            self.txt_costo_venta.setEnabled(True)
            self.txt_costo_venta.setReadOnly(True)
            self.txt_costo_compra.setEnabled(True)
            self.txt_costo_compra.setFocus()

    def enter_descripcion(self):
        if self.txt_descripcion.text() == "":
            return None
        
        self.txt_alerta.setEnabled(True)
        self.txt_alerta.setFocus()

    def enter_cantidad_alerta(self):
        if self.txt_alerta.text() == "":
            return None

        self.txt_cantidad_max.setEnabled(True)
        self.txt_cantidad_max.setFocus()

    def enter_cantidad_max(self):
        if self.txt_cantidad_max.text() == "":
            return None

        success = self.mainApp.DATA_SYSTEM.INSERT_PRODUCTO(
            self.txt_barcode.text(),
            self.txt_descripcion.text(),
            self.txt_alerta.text(),
            self.txt_cantidad_max.text())

        if success:
            self.id_prod = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO(self.txt_barcode.text())[0]
            self.msg.setText("INGRESE EL PRECIO DE COMPRA")
            self.txt_barcode.setReadOnly(True)
            self.txt_descripcion.setReadOnly(True)
            self.txt_alerta.setReadOnly(True)
            self.txt_costo_venta.setEnabled(True)
            self.txt_costo_venta.setReadOnly(True)
            self.txt_costo_compra.setEnabled(True)
            self.txt_costo_compra.setFocus()
        else:
            self.msg.setText("ERROR AL REGISTRAR, INTENTE DE NUEVO")

    def change_txt_compra(self):
        aumento = float(self.mainApp.DATA_SYSTEM.SELECT_AJUSTE("AUMENTO_VENTA"))
        monto_compra = float(self.txt_costo_compra.text().replace(".", "").replace(",", "."))
        monto_venta = ((aumento/100) * monto_compra) + monto_compra
        self.txt_costo_venta.setText(self.mainApp.formato_moneda(monto_venta))

    def enter_txt_compra(self):
        if float(self.txt_costo_compra.text().replace(".", "").replace(",", ".")) <= 0.0:
            return None
        
        '''
        producto = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO(self.txt_barcode.text())
        self.msg.setText("PRECIO DE VENTA ACTUAL\n{} BsF".format(self.mainApp.formato_moneda(float(producto[4]))))
        self.txt_costo_venta.setReadOnly(False)
        self.txt_costo_venta.setFocus()
        self.txt_costo_compra.setReadOnly(True)
        '''

        self.txt_cantidad.setEnabled(True)
        self.txt_cantidad.setFocus()
        self.txt_costo_compra.setReadOnly(True)
        self.msg.setText("INGRESE LA CANTIDAD DEL PRODUCTO")

    def enter_txt_venta(self):
        if float(self.txt_costo_venta.text().replace(".", "").replace(",", ".")) <= 0.0:
            return None

        self.txt_cantidad.setEnabled(True)
        self.txt_cantidad.setFocus()
        self.txt_costo_venta.setReadOnly(True)
        self.msg.setText("INGRESE LA CANTIDAD DEL PRODUCTO")

    def enter_cantidad(self):
        cantidad = None
        try:
            cantidad = int(self.txt_cantidad.text())
        except ValueError:
            self.msg.setText("INGRESE UNA CANTIDAD VALIDA")
            return None

        if cantidad <= 0:
            self.msg.setText("INGRESE UNA CANTIDAD VALIDA")
            return None

        TOTAL = cantidad * float(self.txt_costo_compra.text().replace(".", "").replace(",", "."))

        self.table_productos.insertRow(0)
        self.table_productos.setItem(0,0, QtWidgets.QTableWidgetItem(self.id_prod))
        self.table_productos.setItem(0,1, QtWidgets.QTableWidgetItem(self.txt_descripcion.text()))
        self.table_productos.setItem(0,2, QtWidgets.QTableWidgetItem(self.txt_cantidad.text()))
        self.table_productos.setItem(0,3, QtWidgets.QTableWidgetItem(self.txt_costo_compra.text()))
        self.table_productos.setItem(0,4, QtWidgets.QTableWidgetItem(self.txt_costo_venta.text()))
        self.table_productos.setItem(0,5, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(TOTAL)))

        self.table_productos.resizeRowsToContents()
        self.table_productos.resizeColumnsToContents()

        self.txt_total.setText(self.mainApp.formato_moneda(TOTAL + float(self.txt_total.text().replace(".", "").replace(",", "."))))

        self.txt_barcode.setText("")
        self.txt_barcode.setEnabled(True)
        self.txt_barcode.setReadOnly(False)
        self.txt_descripcion.setText("")
        self.txt_descripcion.setReadOnly(False)
        self.txt_descripcion.setEnabled(False)
        self.txt_alerta.setText("")
        self.txt_alerta.setReadOnly(False)
        self.txt_alerta.setEnabled(False)
        self.txt_costo_compra.setText("0")
        self.txt_costo_compra.setReadOnly(False)
        self.txt_costo_compra.setEnabled(False)
        self.txt_costo_venta.setText("0")
        self.txt_costo_venta.setReadOnly(False)
        self.txt_costo_venta.setEnabled(False)
        self.txt_cantidad.setText("")
        self.txt_cantidad.setReadOnly(False)
        self.txt_cantidad.setEnabled(False)
        self.txt_cantidad_max.setReadOnly(False)
        self.txt_cantidad_max.setEnabled(False)
        self.txt_cantidad_max.setText("")
        self.txt_barcode.setFocus()

    def procesar(self):
        productos_raw = jpype.JArray(jpype.JInt)
        cantidad_raw  = jpype.JArray(jpype.JInt)
        precio_raw    = jpype.JArray(jpype.JFloat)
        productos = productos_raw(self.table_productos.rowCount())
        cantidad  = cantidad_raw(self.table_productos.rowCount())
        precio    = precio_raw(self.table_productos.rowCount())
        for i in range(self.table_productos.rowCount()):
            productos[i] = int(self.table_productos.item(i, 0).text())
            cantidad[i]  = int(self.table_productos.item(i, 2).text())
            precio[i]    = float(self.table_productos.item(i, 3).text().replace(".", "").replace(",", "."))
            self.mainApp.DATA_SYSTEM.UPDATE_PRODUCTO(self.table_productos.item(i, 0).text(), "costo_venta", self.table_productos.item(i, 4).text().replace(".", "").replace(",", "."))

        ref = self.mainApp.DATA_SYSTEM.MOVIMIENTO(2, self.txt_ci.text(), self.mainApp.id_user, self.mainApp.frame_compra.txt_total.text().replace(".", "").replace(",", "."), productos, cantidad, precio)
        if ref != "false":
            if self.mainApp.reporte_compra(ref):
                    self.default_forms()
                    self.dialog_report = Dialog_reportView(args=(self.mainApp, f"compra_{ref}.pdf"))
                    self.dialog_report.show()

    def delete_a_row(self):
        try:
            self.txt_total.setText(self.mainApp.formato_moneda(float(self.txt_total.text().replace(".", "").replace(",", ".")) - float(self.table_productos.item(0, 4).text().replace(".", "").replace(",", "."))))
            self.table_productos.removeRow(0)
        except AttributeError:
            pass

    def default_forms(self):
        self.msg.setText("")
        self.txt_ci.setText("")
        self.txt_ci.setReadOnly(False)
        self.txt_ci.setEnabled(True)
        self.txt_ci.setFocus()
        self.txt_nombre.setText("")
        self.txt_nombre.setReadOnly(False)
        self.txt_nombre.setEnabled(False)
        self.txt_barcode.setText("")
        self.txt_barcode.setReadOnly(False)
        self.txt_barcode.setEnabled(False)
        self.txt_descripcion.setText("")
        self.txt_descripcion.setReadOnly(False)
        self.txt_descripcion.setEnabled(False)
        self.txt_alerta.setText("")
        self.txt_alerta.setReadOnly(False)
        self.txt_alerta.setEnabled(False)
        self.txt_costo_compra.setText("0")
        self.txt_costo_compra.setReadOnly(False)
        self.txt_costo_compra.setEnabled(False)
        self.txt_costo_venta.setText("0")
        self.txt_costo_venta.setReadOnly(False)
        self.txt_costo_venta.setEnabled(False)
        self.txt_cantidad.setText("")
        self.txt_cantidad.setReadOnly(False)
        self.txt_cantidad.setEnabled(False)
        self.table_productos.setRowCount(0)
        self.txt_total.setText("0,00")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F2:
            self.delete_a_row()
        elif event.key() == QtCore.Qt.Key_F5:
            pass

    def create_widgets(self):
        hlayout_main = QtWidgets.QHBoxLayout()
        self.setLayout(hlayout_main)

        vlayout_table = QtWidgets.QVBoxLayout()
        hlayout_main.addLayout(vlayout_table)

        self.table_productos = QtWidgets.QTableWidget()
        self.table_productos.setFont(self.mainApp.font_m)
        self.table_productos.setColumnCount(6)
        self.table_productos.setHorizontalHeaderLabels(['ID', 'NOMBRE', 'CANTIDAD', 'P. COMPRA', 'P. VENTA', 'P. TOTAL'])
        self.table_productos.resizeColumnsToContents()
        vlayout_table.addWidget(self.table_productos)

        form_total = QtWidgets.QFormLayout()
        vlayout_table.addLayout(form_total)

        label_total = QtWidgets.QLabel("TOTAL PAGADO:")
        label_total.setFont(self.mainApp.font_m)

        self.txt_total = QtWidgets.QLineEdit()
        self.txt_total.setFont(self.mainApp.font_g)
        self.txt_total.setText("0,00")
        self.txt_total.setAlignment(QtCore.Qt.AlignRight)
        self.txt_total.setReadOnly(True)
        form_total.addRow(label_total, self.txt_total)

        form_facturacion = QtWidgets.QFormLayout()

        vlayout_botones = QtWidgets.QVBoxLayout()

        font_msg = QtGui.QFont()
        font_msg.setPointSize(16)
        font_msg.setFamily("Impact Normal")
        font_msg.setBold(True)

        self.msg = QtWidgets.QLabel()
        
        # AJUSTAR COLOR MAS TARDE
        
        self.msg.setStyleSheet("QLabel {background: #1F10FF; color: white}")
        self.msg.setMinimumHeight(60)
        self.msg.setFont(font_msg)
        self.msg.setAlignment(QtCore.Qt.AlignCenter)
        vlayout_botones.addWidget(self.msg)

        label_ci = QtWidgets.QLabel("RIF:")
        label_ci.setFont(self.mainApp.font_m)

        self.txt_ci = QtWidgets.QLineEdit()
        self.txt_ci.setFont(self.mainApp.font_m)
        self.txt_ci.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_ci, self.search_rif, context=QtCore.Qt.WidgetShortcut)
        self.txt_ci.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_ci, self.search_rif, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_ci, self.txt_ci)

        label_nombre = QtWidgets.QLabel("RAZÓN SOCIAL:")
        label_nombre.setFont(self.mainApp.font_m)

        self.txt_nombre = QtWidgets.QLineEdit()
        self.txt_nombre.setFont(self.mainApp.font_m)
        self.txt_nombre.setEnabled(False)
        self.txt_nombre.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_nombre, self.enter_proveedor, context=QtCore.Qt.WidgetShortcut)
        self.txt_nombre.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_nombre, self.enter_proveedor, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_nombre, self.txt_nombre)

        label_barcode = QtWidgets.QLabel("CÓDIGO DE BARRA:")
        label_barcode.setFont(self.mainApp.font_m)

        self.txt_barcode = QtWidgets.QLineEdit()
        self.txt_barcode.setFont(self.mainApp.font_m)
        self.txt_barcode.setEnabled(False)
        self.txt_barcode.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_barcode, self.search_barcode, context=QtCore.Qt.WidgetShortcut)
        self.txt_barcode.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_barcode, self.search_barcode, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_barcode, self.txt_barcode)

        label_descripcion = QtWidgets.QLabel("DESCRIPCIÓN:")
        label_descripcion.setFont(self.mainApp.font_m)

        self.txt_descripcion = QtWidgets.QLineEdit()
        self.txt_descripcion.setFont(self.mainApp.font_m)
        self.txt_descripcion.setEnabled(False)
        self.txt_descripcion.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_descripcion, self.enter_descripcion, context=QtCore.Qt.WidgetShortcut)
        self.txt_descripcion.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_descripcion, self.enter_descripcion, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_descripcion, self.txt_descripcion)

        label_alerta = QtWidgets.QLabel("STOCK MINIMO:")
        label_alerta.setFont(self.mainApp.font_m)

        self.txt_alerta = QtWidgets.QLineEdit()
        self.txt_alerta.setFont(self.mainApp.font_m)
        self.txt_alerta.setEnabled(False)
        self.txt_alerta.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_alerta, self.enter_cantidad_alerta, context=QtCore.Qt.WidgetShortcut)
        self.txt_alerta.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_alerta, self.enter_cantidad_alerta, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_alerta, self.txt_alerta)

        label_cantidad_max = QtWidgets.QLabel("STOCK MAXIMO:")
        label_cantidad_max.setFont(self.mainApp.font_m)

        self.txt_cantidad_max = QtWidgets.QLineEdit()
        self.txt_cantidad_max.setFont(self.mainApp.font_m)
        self.txt_cantidad_max.setEnabled(False)
        self.txt_cantidad_max.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_cantidad_max, self.enter_cantidad_max, context=QtCore.Qt.WidgetShortcut)
        self.txt_cantidad_max.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_cantidad_max, self.enter_cantidad_max, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_cantidad_max, self.txt_cantidad_max)

        label_costo_compra = QtWidgets.QLabel("COSTO DE COMPRA:")
        label_costo_compra.setFont(self.mainApp.font_m)

        self.txt_costo_compra = lineAmount()
        self.txt_costo_compra.setFont(self.mainApp.font_m)
        self.txt_costo_compra.setEnabled(False)
        self.txt_costo_compra.setText("0")
        self.txt_costo_compra.textChanged.connect(self.change_txt_compra)
        self.txt_costo_compra.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_costo_compra, self.enter_txt_compra, context=QtCore.Qt.WidgetShortcut)
        self.txt_costo_compra.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_costo_compra, self.enter_txt_compra, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_costo_compra, self.txt_costo_compra)

        label_costo_venta = QtWidgets.QLabel("COSTO DE VENTA:")
        label_costo_venta.setFont(self.mainApp.font_m)

        self.txt_costo_venta = lineAmount()
        self.txt_costo_venta.setFont(self.mainApp.font_m)
        self.txt_costo_venta.setEnabled(False)
        self.txt_costo_venta.setText("0")
        self.txt_costo_venta.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_costo_venta, self.enter_txt_venta, context=QtCore.Qt.WidgetShortcut)
        self.txt_costo_venta.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_costo_venta, self.enter_txt_venta, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_costo_venta, self.txt_costo_venta)

        label_cantidad = QtWidgets.QLabel("CANTIDAD:")
        label_cantidad.setFont(self.mainApp.font_m)

        self.txt_cantidad = QtWidgets.QLineEdit()
        self.txt_cantidad.setFont(self.mainApp.font_m)
        self.txt_cantidad.setEnabled(False)
        self.txt_cantidad.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_cantidad, self.enter_cantidad, context=QtCore.Qt.WidgetShortcut)
        self.txt_cantidad.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_cantidad, self.enter_cantidad, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_cantidad, self.txt_cantidad)

        hlayout_main.addLayout(vlayout_botones)
        vlayout_botones.addLayout(form_facturacion)

        grid_botones = QtWidgets.QGridLayout()
        vlayout_botones.addLayout(grid_botones)

        self.btn_aceptar = QtWidgets.QPushButton("ACEPTAR (ENTER)")
        self.btn_aceptar.setFont(self.mainApp.font_m)
        self.btn_aceptar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_aceptar.setMinimumHeight(80)
        self.btn_aceptar.clicked.connect(self.enter_cantidad)
        grid_botones.addWidget(self.btn_aceptar, 0, 0)

        self.btn_borrar = QtWidgets.QPushButton("BORRAR REGISTRO (F2)")
        self.btn_borrar.setFont(self.mainApp.font_m)
        self.btn_borrar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_borrar.setMinimumHeight(80)
        self.btn_borrar.clicked.connect(self.delete_a_row)
        grid_botones.addWidget(self.btn_borrar, 0, 1)

        self.btn_cobrar = QtWidgets.QPushButton("INGRESAR (F5)")
        self.btn_cobrar.setFont(self.mainApp.font_m)
        self.btn_cobrar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_cobrar.clicked.connect(self.procesar)
        self.btn_cobrar.setMinimumHeight(80)
        grid_botones.addWidget(self.btn_cobrar, 1, 0)

        vlayout_botones.addStretch()
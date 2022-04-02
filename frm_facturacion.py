from PyQt5 import QtCore, QtGui, QtWidgets

from dialogs.dialog_cobranza import Dialog_cobranza
from dialogs.dialog_registro_cliente import Dialog_cliente
from dialogs.dialog_consultar import Dialog_consultar

class Frame_facturacion(QtWidgets.QFrame):
    
    mainApp = None
    id_prod = None

    def __init__(self, *args, **kwargs):
        super(Frame_facturacion, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

    def search_cliente(self):
        cliente = self.mainApp.DATA_SYSTEM.SELECT_CLIENTE(self.txt_ci.text())

        if cliente == None:
            client_dialog = Dialog_cliente(args=self.mainApp)
        else:
            self.txt_nombre.setText(cliente[2])
            self.txt_barcode.setFocus()

    def search_barcode(self):
        self.data = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO(self.txt_barcode.text())
        
        if self.data == None:
            self.msg.setText("ARTICULO INEXISTENTE")
            return None
        
        self.id_prod = self.data[0]
        self.txt_descripcion.setText(self.data[2])
        self.txt_costo.setText(self.mainApp.formato_moneda(float(self.data[4])))

        self.txt_cantidad.setEnabled(True)
        self.txt_cantidad.setFocus()

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
        
        print("cantidad: {} existencia: {}".format(cantidad, self.data[3]))
        if cantidad > int(self.data[3]):
            self.msg.setText("CANTIDAD DESEADA SUPERA EXISTENCIAS")
            self.txt_cantidad.setText("")
            return None

        TOTAL = cantidad * float(self.txt_costo.text().replace(".", "").replace(",", "."))

        self.table_productos.insertRow(0)
        self.table_productos.setItem(0,0, QtWidgets.QTableWidgetItem(self.id_prod))
        self.table_productos.setItem(0,1, QtWidgets.QTableWidgetItem(self.txt_descripcion.text()))
        self.table_productos.setItem(0,2, QtWidgets.QTableWidgetItem(self.txt_cantidad.text()))
        self.table_productos.setItem(0,3, QtWidgets.QTableWidgetItem(self.txt_costo.text()))
        self.table_productos.setItem(0,4, QtWidgets.QTableWidgetItem(self.mainApp.formato_moneda(TOTAL)))

        self.table_productos.resizeRowsToContents()
        self.table_productos.resizeColumnsToContents()

        self.txt_total.setText(self.mainApp.formato_moneda(TOTAL + float(self.txt_total.text().replace(".", "").replace(",", "."))))

        self.txt_barcode.setText("")
        self.txt_descripcion.setText("")
        self.txt_costo.setText("")
        self.txt_cantidad.setText("")
        self.txt_cantidad.setEnabled(False)
        self.txt_barcode.setFocus()

    def cobrar(self):

        if float(self.txt_total.text().replace(".", "").replace(",", ".")) <= 0.0:
            self.msg.setText("SIN ARTICULOS PARA COBRAR")
            return None

        self.dialog_cobrar = Dialog_cobranza(args=self.mainApp)
        self.dialog_cobrar.get_total(self.txt_total.text())

    def delete_a_row(self):
        try:
            self.txt_total.setText(self.mainApp.formato_moneda(float(self.txt_total.text().replace(".", "").replace(",", ".")) - float(self.table_productos.item(0, 4).text().replace(".", "").replace(",", "."))))
            self.table_productos.removeRow(0)
        except AttributeError:
            pass

    def open_consultar(self):
        self.dialog_consultar = Dialog_consultar(args=self.mainApp)

    def default_forms(self):
        self.table_productos.setRowCount(0)
        self.txt_total.setText("0,00")
        self.txt_ci.setText("")
        self.txt_nombre.setText("")
        self.txt_nombre.setReadOnly(True)
        self.txt_barcode.setText("")
        self.txt_descripcion.setText("")
        self.txt_costo.setText("")
        self.txt_cantidad.setText("")
        self.txt_ci.setFocus()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F1:
            self.open_consultar()
        elif event.key() == QtCore.Qt.Key_F2:
            self.delete_a_row()
        elif event.key() == QtCore.Qt.Key_F5:
            self.cobrar()

    def create_widgets(self):
        hlayout_main = QtWidgets.QHBoxLayout()
        self.setLayout(hlayout_main)

        vlayout_table = QtWidgets.QVBoxLayout()
        hlayout_main.addLayout(vlayout_table)

        self.table_productos = QtWidgets.QTableWidget()
        self.table_productos.setFont(self.mainApp.font_m)
        self.table_productos.setColumnCount(5)
        self.table_productos.setHorizontalHeaderLabels(['ID', 'NOMBRE', 'CANTIDAD', 'P. UNIDAD', 'P. TOTAL'])
        self.table_productos.resizeColumnsToContents()
        vlayout_table.addWidget(self.table_productos)

        form_total = QtWidgets.QFormLayout()
        vlayout_table.addLayout(form_total)

        label_total = QtWidgets.QLabel("TOTAL A PAGAR:")
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

        label_ci = QtWidgets.QLabel("CEDULA:")
        label_ci.setFont(self.mainApp.font_m)

        self.txt_ci = QtWidgets.QLineEdit()
        self.txt_ci.setFont(self.mainApp.font_m)
        self.txt_ci.setText("-")
        self.txt_ci.textChanged.connect(lambda: self.mainApp.input_format_number(self.txt_ci))
        self.txt_ci.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_ci, self.search_cliente, context=QtCore.Qt.WidgetShortcut)
        self.txt_ci.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_ci, self.search_cliente, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_ci, self.txt_ci)

        label_nombre = QtWidgets.QLabel("NOMBRE:")
        label_nombre.setFont(self.mainApp.font_m)

        self.txt_nombre = QtWidgets.QLineEdit()
        self.txt_nombre.setFont(self.mainApp.font_m)
        self.txt_nombre.setText("CLIENTE GENERAL")
        self.txt_nombre.setReadOnly(True)
        form_facturacion.addRow(label_nombre, self.txt_nombre)

        label_barcode = QtWidgets.QLabel("CÓDIGO DE BARRA:")
        label_barcode.setFont(self.mainApp.font_m)

        self.txt_barcode = QtWidgets.QLineEdit()
        self.txt_barcode.setFont(self.mainApp.font_m)
        self.txt_barcode.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_barcode, self.search_barcode, context=QtCore.Qt.WidgetShortcut)
        self.txt_barcode.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_barcode, self.search_barcode, context=QtCore.Qt.WidgetShortcut)
        form_facturacion.addRow(label_barcode, self.txt_barcode)

        label_descripcion = QtWidgets.QLabel("DESCRIPCIÓN:")
        label_descripcion.setFont(self.mainApp.font_m)

        self.txt_descripcion = QtWidgets.QLineEdit()
        self.txt_descripcion.setFont(self.mainApp.font_m)
        self.txt_descripcion.setReadOnly(True)
        form_facturacion.addRow(label_descripcion, self.txt_descripcion)

        label_costo = QtWidgets.QLabel("COSTO:")
        label_costo.setFont(self.mainApp.font_m)

        self.txt_costo = QtWidgets.QLineEdit()
        self.txt_costo.setFont(self.mainApp.font_m)
        self.txt_costo.setReadOnly(True)
        form_facturacion.addRow(label_costo, self.txt_costo)

        label_cantidad = QtWidgets.QLabel("CANTIDAD:")
        label_cantidad.setFont(self.mainApp.font_m)

        self.txt_cantidad = QtWidgets.QLineEdit()
        self.txt_cantidad.setFont(self.mainApp.font_m)
        self.txt_cantidad.setEnabled(False)
        self.txt_cantidad.textChanged.connect(lambda: self.mainApp.input_format_number(self.txt_cantidad))
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

        self.btn_devolucion = QtWidgets.QPushButton("DEVOLUCION (F10)")
        self.btn_devolucion.setFont(self.mainApp.font_m)
        self.btn_devolucion.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_devolucion.setMinimumHeight(80)
        grid_botones.addWidget(self.btn_devolucion, 1, 0)

        self.btn_consultar = QtWidgets.QPushButton("CONSULTAR (F1)")
        self.btn_consultar.setFont(self.mainApp.font_m)
        self.btn_consultar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_consultar.setMinimumHeight(80)
        self.btn_consultar.clicked.connect(self.open_consultar)
        grid_botones.addWidget(self.btn_consultar, 1, 1)

        self.btn_cobrar = QtWidgets.QPushButton("COBRAR (F5)")
        self.btn_cobrar.setFont(self.mainApp.font_m)
        self.btn_cobrar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_cobrar.setMinimumHeight(80)
        self.btn_cobrar.clicked.connect(self.cobrar)
        grid_botones.addWidget(self.btn_cobrar, 2, 0)

        self.btn_cierre = QtWidgets.QPushButton("CIERRE DE CAJA (F11)")
        self.btn_cierre.setFont(self.mainApp.font_m)
        self.btn_cierre.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_cierre.setMinimumHeight(80)
        grid_botones.addWidget(self.btn_cierre, 2, 1)

        vlayout_botones.addStretch()
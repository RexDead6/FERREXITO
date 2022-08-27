from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
import jpype

import jpype

class Frame_inventario(QtWidgets.QFrame):
    
    mainApp = None

    def __init__(self, *args, **kwargs):
        super(Frame_inventario, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

        self.msgBox = QMessageBox()

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

    def generar_ajuste(self):
        if float(self.txt_total.text().replace(".", "").replace(",", ".")) <= 0.0:
            self.msg.setText("SIN ARTICULOS")
            return None

        if self.txt_descripcion_inv.text() == "":
            self.msg.setText("INGRESE UNA DESCRIPCION DEL AJUSTE")
            return None

        if self.box_manejo.currentIndex() == 0:
            self.msg.setText("INGRESE UNA METODO PARA EL AJUSTE")
            return None

        metodo = 5 if self.box_manejo.currentIndex() == 1 else 4

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

        referencia = self.mainApp.DATA_SYSTEM.MOVIMIENTO(metodo, self.txt_descripcion_inv.text(), self.mainApp.id_user, self.txt_total.text().replace(".", "").replace(",", "."), productos, cantidad, precio)

        if referencia != None:
            QMessageBox.information(self.msgBox, "::AJUSTE EXITOSO::", "SU AJUSTE HA SIDO PROCESADO EXITOSAMENTE (REF: "+referencia+")")
        else:
            QMessageBox.critical(self.msgBox, "::ERROR::", "NO SE HA PODIDO PROCESAR SU AJUSTE,\nINTENTE DE NUEVO")
        self.default_forms()

    def delete_a_row(self):
        try:
            self.txt_total.setText(self.mainApp.formato_moneda(float(self.txt_total.text().replace(".", "").replace(",", ".")) - float(self.table_productos.item(0, 4).text().replace(".", "").replace(",", "."))))
            self.table_productos.removeRow(0)
        except AttributeError:
            pass

    def default_forms(self):
        self.table_productos.setRowCount(0)
        self.txt_total.setText("0,00")
        self.txt_barcode.setText("")
        self.txt_descripcion.setText("")
        self.txt_descripcion_inv.setText("")
        self.txt_costo.setText("")
        self.txt_cantidad.setText("")
        self.box_manejo.setCurrentIndex(0)

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
        self.table_productos.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
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

        vlayout_botones = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()

        font_msg = QtGui.QFont()
        font_msg.setPointSize(16)
        font_msg.setFamily("Impact Normal")
        font_msg.setBold(True)

        self.msg = QtWidgets.QLabel()
        self.msg.setStyleSheet("QLabel {background: #1F10FF; color: white}")
        self.msg.setMaximumHeight(60)
        self.msg.setFont(font_msg)
        self.msg.setAlignment(QtCore.Qt.AlignCenter)
        vlayout_botones.addWidget(self.msg)

        label_manejo =  QtWidgets.QLabel("MANEJO:")
        label_manejo.setFont(self.mainApp.font_m)

        self.box_manejo = QtWidgets.QComboBox()
        self.box_manejo.addItem("---SELECCIONE---")
        self.box_manejo.addItem("AGREGAR")
        self.box_manejo.addItem("SUBTRAER")
        self.box_manejo.setFont(self.mainApp.font_m)
        form_layout.addRow(label_manejo, self.box_manejo)

        label_descripcion_inv = QtWidgets.QLabel("DESCRIPCION DE AJUSTE:")
        label_descripcion_inv.setFont(self.mainApp.font_m)

        self.txt_descripcion_inv = QtWidgets.QLineEdit()
        self.txt_descripcion_inv.setFont(self.mainApp.font_m)
        self.txt_descripcion_inv.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_descripcion_inv, lambda: self.txt_barcode.setFocus(), context=QtCore.Qt.WidgetShortcut)
        self.txt_descripcion_inv.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_descripcion_inv, lambda: self.txt_barcode.setFocus(), context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_descripcion_inv, self.txt_descripcion_inv)
        
        label_barcode = QtWidgets.QLabel("CÓDIGO DE BARRA:")
        label_barcode.setFont(self.mainApp.font_m)

        self.txt_barcode = QtWidgets.QLineEdit()
        self.txt_barcode.setFont(self.mainApp.font_m)
        self.txt_barcode.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_barcode, self.search_barcode, context=QtCore.Qt.WidgetShortcut)
        self.txt_barcode.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_barcode, self.search_barcode, context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_barcode, self.txt_barcode)

        label_descripcion = QtWidgets.QLabel("PRODUCTO:")
        label_descripcion.setFont(self.mainApp.font_m)

        self.txt_descripcion = QtWidgets.QLineEdit()
        self.txt_descripcion.setFont(self.mainApp.font_m)
        self.txt_descripcion.setReadOnly(True)
        form_layout.addRow(label_descripcion, self.txt_descripcion)

        label_costo = QtWidgets.QLabel("COSTO:")
        label_costo.setFont(self.mainApp.font_m)

        self.txt_costo = QtWidgets.QLineEdit()
        self.txt_costo.setFont(self.mainApp.font_m)
        self.txt_costo.setReadOnly(True)
        form_layout.addRow(label_costo, self.txt_costo)

        label_cantidad = QtWidgets.QLabel("CANTIDAD:")
        label_cantidad.setFont(self.mainApp.font_m)

        self.txt_cantidad = QtWidgets.QLineEdit()
        self.txt_cantidad.setFont(self.mainApp.font_m)
        self.txt_cantidad.setEnabled(False)
        self.txt_cantidad.textChanged.connect(lambda: self.mainApp.input_format_number(self.txt_cantidad))
        self.txt_cantidad.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_cantidad, self.enter_cantidad, context=QtCore.Qt.WidgetShortcut)
        self.txt_cantidad.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_cantidad, self.enter_cantidad, context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_cantidad, self.txt_cantidad)

        hlayout_main.addLayout(vlayout_botones)
        vlayout_botones.addLayout(form_layout)

        grid_botones = QtWidgets.QGridLayout()
        vlayout_botones.addLayout(grid_botones)

        self.btn_aceptar = QtWidgets.QPushButton("GENERAR AJUSTE (F1)")
        self.btn_aceptar.setFont(self.mainApp.font_m)
        self.btn_aceptar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_aceptar.setMinimumHeight(80)
        self.btn_aceptar.clicked.connect(self.generar_ajuste)
        grid_botones.addWidget(self.btn_aceptar, 0, 0)

        self.btn_borrar = QtWidgets.QPushButton("BORRAR REGISTRO (F2)")
        self.btn_borrar.setFont(self.mainApp.font_m)
        self.btn_borrar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_borrar.setMinimumHeight(80)
        self.btn_borrar.clicked.connect(self.delete_a_row)
        grid_botones.addWidget(self.btn_borrar, 0, 1)
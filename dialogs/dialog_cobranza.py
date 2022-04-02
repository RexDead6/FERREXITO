from PyQt5 import QtCore, QtGui, QtWidgets
import jpype

from class_secundary import lineAmount

class Dialog_cobranza(QtWidgets.QDialog):

    TOTAL_PAGAR = 0.0

    def __init__(self, *args, **kwargs):
        super(Dialog_cobranza, self).__init__()
        self.mainApp = kwargs["args"]
        self.create_widgets()

    def get_total(self, total):
        self.TOTAL_PAGAR = float(total.replace(".", "").replace(",", "."))

    def set_metodo(self, metodo):
        self.txt_ref.setText("")
        self.txt_ref.setEnabled(False)
        self.txt_monto.setText("")
        self.txt_monto.setEnabled(False)
        self.combo_metodo.setCurrentIndex(metodo)
        if metodo > 0:
            self.txt_ref.setEnabled(True)
            self.txt_ref.setFocus()
        else:
            self.txt_monto.setEnabled(True)
            self.txt_monto.setText("{:.2f}".format(self.TOTAL_PAGAR))
            self.txt_monto.setFocus()

    def enter_referencia(self):
        self.txt_monto.setEnabled(True)
        self.txt_monto.setText("{:.2f}".format(self.TOTAL_PAGAR))
        self.txt_monto.setFocus()

    def enter_monto(self):
        referencia = self.txt_ref.text()
        if referencia == "": referencia = "0"
        self.table_pago.insertRow(0)
        self.table_pago.setItem(0,0, QtWidgets.QTableWidgetItem(self.combo_metodo.currentText()))
        self.table_pago.setItem(0,1, QtWidgets.QTableWidgetItem(referencia))
        self.table_pago.setItem(0,2, QtWidgets.QTableWidgetItem(self.txt_monto.text()))

        self.TOTAL_PAGAR = float(self.mainApp.DATA_SYSTEM.substract(str(self.TOTAL_PAGAR), self.txt_monto.text().replace(".", "").replace(",", ".")))

        if self.TOTAL_PAGAR <= 0:
            productos_raw = jpype.JArray(jpype.JInt)
            cantidad_raw  = jpype.JArray(jpype.JInt)
            precio_raw    = jpype.JArray(jpype.JFloat)
            productos = productos_raw(self.mainApp.frame_facturacion.table_productos.rowCount())
            cantidad  = cantidad_raw(self.mainApp.frame_facturacion.table_productos.rowCount())
            precio    = precio_raw(self.mainApp.frame_facturacion.table_productos.rowCount())
            for i in range(self.mainApp.frame_facturacion.table_productos.rowCount()):
                productos[i] = int(self.mainApp.frame_facturacion.table_productos.item(i, 0).text())
                cantidad[i]  = int(self.mainApp.frame_facturacion.table_productos.item(i, 2).text())
                precio[i]    = float(self.mainApp.frame_facturacion.table_productos.item(i, 3).text().replace(".", "").replace(",", "."))

            metodo_raw = jpype.JArray(jpype.JInt)
            ref_raw    = jpype.JArray(jpype.JInt)
            monto_raw  = jpype.JArray(jpype.JFloat)
            metodo = metodo_raw(self.table_pago.rowCount())
            ref    = ref_raw(self.table_pago.rowCount())
            monto  = monto_raw(self.table_pago.rowCount())
            for i in range(self.table_pago.rowCount()):
                metodo[i] = self.mainApp.DATA_SYSTEM.format_type_meth(self.table_pago.item(i, 0).text())
                ref[i]    = int(self.table_pago.item(i, 1).text())
                monto[i]  = float(self.table_pago.item(i, 2).text().replace(".", "").replace(",", "."))

            ci = self.mainApp.frame_facturacion.txt_ci.text()
            if self.mainApp.frame_facturacion.txt_ci.text() == "-": ci = "0"
            ref = self.mainApp.DATA_SYSTEM.MOVIMIENTO(1, ci, self.mainApp.id_user, self.mainApp.frame_facturacion.txt_total.text().replace(".", "").replace(",", "."), productos, cantidad, precio, metodo, ref, monto)
            if ref != "false":
                text_data = "{:<25}{:>25}".format("REFERENCIA:", ref)
                text_data = text_data + "\n{:<25}{:>25}".format("CLIENTE:", self.mainApp.frame_facturacion.txt_nombre.text())
                text_data = text_data + "\n{:<25}{:>25}".format("MONTO:", self.mainApp.frame_facturacion.txt_total.text()+" Bs")
                self.label_data.setText(text_data)
                self.stack.setCurrentIndex(1)
                self.mainApp.frame_facturacion.default_forms()
        else:
            self.txt_monto.setText("{:.2f}".format(self.TOTAL_PAGAR))
            self.txt_monto.setFocus()
            self.combo_metodo.setCurrentIndex(0)
            self.txt_ref.setText("")
            self.txt_ref.setEnabled(False)

    def input_txt_monto(self):
        txt = self.txt_monto.text()[:len(self.txt_monto.text())-2].replace(".", "").replace(",", "")
        total = str(self.TOTAL_PAGAR).replace(".", "").replace(",", "")

        if total == txt:
            self.txt_monto.setText(self.txt_monto.text()[len(self.txt_monto.text())-1:])

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F1:
            self.set_metodo(0)
        elif event.key() == QtCore.Qt.Key_F2:
            self.set_metodo(1)
        elif event.key() == QtCore.Qt.Key_F3:
            self.set_metodo(2)
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def create_widgets(self):
        self.setWindowTitle("COBRANZA")
        self.setModal(True)

        layout_main = QtWidgets.QHBoxLayout()
        self.setLayout(layout_main)

        frame_table  = QtWidgets.QFrame()
        layout_table = QtWidgets.QVBoxLayout()
        layout_table_h = QtWidgets.QHBoxLayout()
        frame_table.setLayout(layout_table_h)
        layout_table_h.addLayout(layout_table)

        frame_info  = QtWidgets.QFrame()
        layout_info = QtWidgets.QVBoxLayout()
        frame_info.setLayout(layout_info)

        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(frame_table)
        self.stack.addWidget(frame_info)
        layout_main.addWidget(self.stack)

        #--------------- FRAME TABLE ---------------------

        self.table_pago = QtWidgets.QTableWidget()
        self.table_pago.setFont(self.mainApp.font_m)
        self.table_pago.setColumnCount(3)
        self.table_pago.setHorizontalHeaderLabels(['METODO', 'REF', 'MONTO'])
        self.table_pago.resizeColumnsToContents()
        layout_table.addWidget(self.table_pago)

        layout_forms = QtWidgets.QGridLayout()
        layout_table.addLayout(layout_forms)

        label_metodo = QtWidgets.QLabel("METODO:")
        label_metodo.setFont(self.mainApp.font_m)
        layout_forms.addWidget(label_metodo, 0, 0)

        self.combo_metodo = QtWidgets.QComboBox()
        self.combo_metodo.addItem("EFECTIVO")
        self.combo_metodo.addItem("DEBITO")
        self.combo_metodo.addItem("CREDITO")
        self.combo_metodo.setFont(self.mainApp.font_m)
        layout_forms.addWidget(self.combo_metodo, 1, 0)

        label_ref = QtWidgets.QLabel("REFERENCIA:")
        label_ref.setFont(self.mainApp.font_m)
        layout_forms.addWidget(label_ref, 0, 1)

        self.txt_ref = QtWidgets.QLineEdit()
        self.txt_ref.setFont(self.mainApp.font_m)
        self.txt_ref.enter_short_cut  = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_ref, self.enter_referencia, context=QtCore.Qt.WidgetShortcut)
        self.txt_ref.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_ref, self.enter_referencia , context=QtCore.Qt.WidgetShortcut)
        self.txt_ref.setEnabled(False)
        layout_forms.addWidget(self.txt_ref, 1, 1)

        label_monto = QtWidgets.QLabel("MONTO:")
        label_monto.setFont(self.mainApp.font_m)
        layout_forms.addWidget(label_monto, 0, 2)

        self.txt_monto = lineAmount()
        self.txt_monto.setFont(self.mainApp.font_m)
        self.txt_monto.setEnabled(False)
        self.txt_monto.textChanged.connect(self.input_txt_monto)
        self.txt_monto.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_monto, self.enter_monto, context=QtCore.Qt.WidgetShortcut)
        self.txt_monto.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_monto, self.enter_monto , context=QtCore.Qt.WidgetShortcut)
        layout_forms.addWidget(self.txt_monto, 1, 2)

        layout_btn = QtWidgets.QVBoxLayout()
        layout_table_h.addLayout(layout_btn)

        self.btn_efectivo = QtWidgets.QPushButton("EFECTIVO (F1)")
        self.btn_efectivo.setFont(self.mainApp.font_m)
        self.btn_efectivo.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_efectivo.setMinimumHeight(80)
        self.btn_efectivo.setMinimumWidth(160)
        self.btn_efectivo.clicked.connect(lambda: self.set_metodo(0))
        layout_btn.addWidget(self.btn_efectivo)

        self.btn_debito = QtWidgets.QPushButton("DEBITO (F2)")
        self.btn_debito.setFont(self.mainApp.font_m)
        self.btn_debito.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_debito.setMinimumHeight(80)
        self.btn_debito.setMinimumWidth(160)
        self.btn_debito.clicked.connect(lambda: self.set_metodo(1))
        layout_btn.addWidget(self.btn_debito)

        self.btn_credito = QtWidgets.QPushButton("CREDITO (F3)")
        self.btn_credito.setFont(self.mainApp.font_m)
        self.btn_credito.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_credito.setMinimumHeight(80)
        self.btn_credito.setMinimumWidth(160)
        self.btn_credito.clicked.connect(lambda: self.set_metodo(2))
        layout_btn.addWidget(self.btn_credito)

        #--------------------- FRAME INFO ----------------------
        font_titulo = QtGui.QFont()
        font_titulo.setBold(True)
        font_titulo.setPointSize(20)

        font_data = QtGui.QFont()
        font_data.setPointSize(16)

        titulo_info = QtWidgets.QLabel("OPERACIÓN APROBADA")
        titulo_info.setFont(font_titulo)
        titulo_info.setStyleSheet("QLabel{ color:green }")
        layout_info.addWidget(titulo_info)
        layout_info.setAlignment(titulo_info, QtCore.Qt.AlignHCenter)

        self.label_data = QtWidgets.QLabel()
        self.label_data.setFont(font_data)
        layout_info.addWidget(self.label_data)
        layout_info.setAlignment(self.label_data, QtCore.Qt.AlignHCenter)

        self.show()
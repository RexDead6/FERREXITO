from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Dialog_cliente(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(Dialog_cliente, self).__init__()
        self.mainApp = kwargs["args"]
        self.create_widgets()

        self.msgBox = QMessageBox()

    def register_user(self):
        if self.txt_ci.text() == "" or self.txt_nombre.text() == "":
            QMessageBox.Critical(self.msgBox, "::: ATENCIÓN :::", "RELLENE TODOS LOS FORMULARIOS IMPORTANTES (*)")
            return None

        success = self.mainApp.DATA_SYSTEM.INSERT_CLIENTE(self.txt_ci.text(), self.txt_nombre.text(), self.txt_tlfn.text(), self.txt_direccion.text())
        if success:
            self.mainApp.frame_facturacion.msg.setText("CLIENTE REGISTRADO CON EXITO")
            self.mainApp.frame_facturacion.txt_nombre.setText(self.txt_nombre.text())
            self.mainApp.frame_facturacion.txt_barcode.setFocus()
            self.hide()

    def create_widgets(self):
        self.setWindowTitle("REGISTRO CLIENTE")
        self.setModal(True)

        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        font_titulo = QtGui.QFont()
        font_titulo.setBold(True)
        font_titulo.setPointSize(20)

        titulo = QtWidgets.QLabel("REGISTRO DE CLIENTES")
        titulo.setFont(font_titulo)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        layout_form = QtWidgets.QFormLayout()
        layout_main.addLayout(layout_form)

        label_ci = QtWidgets.QLabel("* Cedula de Identidad:")
        label_ci.setFont(self.mainApp.font_m)

        self.txt_ci = QtWidgets.QLineEdit(self.mainApp.frame_facturacion.txt_ci.text())
        self.txt_ci.setFont(self.mainApp.font_m)
        self.txt_ci.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_ci, lambda: self.txt_nombre.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_ci.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_ci, lambda: self.txt_nombre.setFocus() , context=QtCore.Qt.WidgetShortcut)
        layout_form.addRow(label_ci, self.txt_ci)

        label_nombre = QtWidgets.QLabel("* Nombre y Apellido:")
        label_nombre.setFont(self.mainApp.font_m)

        self.txt_nombre = QtWidgets.QLineEdit()
        self.txt_nombre.setFont(self.mainApp.font_m)
        self.txt_nombre.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_nombre, lambda: self.txt_tlfn.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_nombre.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_nombre, lambda: self.txt_tlfn.setFocus() , context=QtCore.Qt.WidgetShortcut)
        layout_form.addRow(label_nombre, self.txt_nombre)

        label_tlfn = QtWidgets.QLabel("Telefono:")
        label_tlfn.setFont(self.mainApp.font_m)

        self.txt_tlfn = QtWidgets.QLineEdit()
        self.txt_tlfn.setFont(self.mainApp.font_m)
        self.txt_tlfn.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_tlfn, lambda: self.txt_direccion.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_tlfn.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_tlfn, lambda: self.txt_direccion.setFocus(), context=QtCore.Qt.WidgetShortcut)
        layout_form.addRow(label_tlfn, self.txt_tlfn)

        label_direccion = QtWidgets.QLabel("Direccion:")
        label_direccion.setFont(self.mainApp.font_m)

        self.txt_direccion = QtWidgets.QLineEdit()
        self.txt_direccion.setFont(self.mainApp.font_m)
        self.txt_direccion.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_direccion, self.register_user, context=QtCore.Qt.WidgetShortcut)
        self.txt_direccion.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_direccion, self.register_user, context=QtCore.Qt.WidgetShortcut)
        layout_form.addRow(label_direccion, self.txt_direccion)

        self.show()
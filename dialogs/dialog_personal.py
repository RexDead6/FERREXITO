from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Dialog_personal(QtWidgets.QDialog):

    IS_EDIT = False

    def __init__(self, *args, **kwargs):
        super(Dialog_personal, self).__init__()
        self.mainApp = kwargs["args"]
        self.create_widgets()

        self.msgBox = QMessageBox()

    def SET_EDIT(self, edit):
        self.IS_EDIT = edit

        if self.IS_EDIT and self.mainApp.frame_personal.table_personal.selectionModel().hasSelection():
            row = self.mainApp.frame_personal.table_personal.currentRow()
            self.personal = self.mainApp.DATA_SYSTEM.SELECT_USER(self.mainApp.frame_personal.table_personal.item(row, 0).text())
            self.txt_ci.setText(self.personal[1])
            self.txt_nombre.setText(self.personal[2])
            self.box_cargo.setCurrentIndex(int(self.personal[3]))

    def register_user(self):
        if self.txt_ci.text() == "" or self.box_cargo.currentIndex() == 0 or self.txt_nombre.text() == "" or self.txt_pass.text() == "" or self.txt_pass1.text() == "":
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "RELLENE TODOS LOS FORMULARIOS")
            return None
        
        if self.txt_pass.text() != self.txt_pass1.text():
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "CONTRASEÑAS NO COINCIDEN")
            self.txt_pass.setText("")
            self.txt_pass1.setText("")
            self.txt_pass.setFocus()
            return None

        if self.mainApp.DATA_SYSTEM.SELECT_USER(self.txt_ci.text()) != None:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "USUARIO YA HA SIDO REGISTRADO")
            return None

        SUCCESS = self.mainApp.DATA_SYSTEM.INSERT_USER(self.txt_ci.text(), self.txt_nombre.text(), self.box_cargo.currentIndex(), self.txt_pass.text())
        if SUCCESS:
            QMessageBox.information(self.msgBox, "::: OPERACIÓN EXITOSA :::", "USUARIO REGISTRADO EXITOSAMENTE")
            self.mainApp.frame_personal.add_data_table()
            self.close()
        else:
            QMessageBox.Critical(self.msgBox, "::: ATENCIÓN :::", "ERROR AL REGISTRAR USUARIO, INTENTE DE NUEVO")

    def create_widgets(self):
        self.setModal(True)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        titulo = QtWidgets.QLabel("::FORMULARIO EMPLEADOS::")
        titulo.setFont(self.mainApp.font_g)
        main_layout.addWidget(titulo)
        main_layout.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        form_layout = QtWidgets.QFormLayout()
        main_layout.addLayout(form_layout)

        label_ci = QtWidgets.QLabel("CEDULA:")
        label_ci.setFont(self.mainApp.font_m)

        self.txt_ci = QtWidgets.QLineEdit()
        self.txt_ci.setFont(self.mainApp.font_m)
        self.txt_ci.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_ci, lambda: self.txt_nombre.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_ci.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_ci, lambda: self.txt_nombre.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_ci, self.txt_ci)
        
        label_nombre =  QtWidgets.QLabel("NOMBRE COMPLETO:")
        label_nombre.setFont(self.mainApp.font_m)

        self.txt_nombre = QtWidgets.QLineEdit()
        self.txt_nombre.setFont(self.mainApp.font_m)
        self.txt_nombre.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_nombre, lambda: self.box_cargo.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_nombre.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_nombre, lambda: self.box_cargo.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_nombre, self.txt_nombre)

        label_cargo =  QtWidgets.QLabel("CARGO:")
        label_cargo.setFont(self.mainApp.font_m)

        self.box_cargo = QtWidgets.QComboBox()
        self.box_cargo.addItem("---SELECCIONE---")
        self.box_cargo.addItem("SUPERVISOR")
        self.box_cargo.addItem("OPERADOR")
        self.box_cargo.setFont(self.mainApp.font_m)
        self.box_cargo.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.box_cargo, lambda: self.box_cargo.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.box_cargo.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.box_cargo, lambda: self.box_cargo.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_cargo, self.box_cargo)

        label_pass =  QtWidgets.QLabel("CONTRASEÑA:")
        label_pass.setFont(self.mainApp.font_m)

        self.txt_pass = QtWidgets.QLineEdit()
        self.txt_pass.setFont(self.mainApp.font_m)
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_pass.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_pass, lambda: self.txt_pass1.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_pass.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_pass, lambda: self.txt_pass1.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_pass, self.txt_pass)

        label_pass1 =  QtWidgets.QLabel("CONFIRMAR CONTRASEÑA:")
        label_pass1.setFont(self.mainApp.font_m)

        self.txt_pass1 = QtWidgets.QLineEdit()
        self.txt_pass1.setFont(self.mainApp.font_m)
        self.txt_pass1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_pass1.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_pass1, self.register_user , context=QtCore.Qt.WidgetShortcut)
        self.txt_pass1.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_pass1, self.register_user , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_pass1, self.txt_pass1)

        layout_button = QtWidgets.QHBoxLayout()
        main_layout.addLayout(layout_button)
        main_layout.setAlignment(layout_button, QtCore.Qt.AlignHCenter)

        self.btn_aceptar = QtWidgets.QPushButton("ACEPTAR")
        self.btn_aceptar.setFont(self.mainApp.font_m)
        self.btn_aceptar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_aceptar.clicked.connect(self.register_user)
        layout_button.addWidget(self.btn_aceptar)

        self.btn_cancelar = QtWidgets.QPushButton("CANCELAR")
        self.btn_cancelar.setFont(self.mainApp.font_m)
        self.btn_cancelar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_cancelar.clicked.connect(lambda: self.close())
        layout_button.addWidget(self.btn_cancelar)
        
        self.show()
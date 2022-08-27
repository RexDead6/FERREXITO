from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Dialog_ajustes(QtWidgets.QDialog):
    
    mainApp = None

    def __init__(self, *args, **kwargs):
        self.mainApp = kwargs['args']
        super(Dialog_ajustes, self).__init__()
        self.create_widgets()
        self.setValues()

        self.msgBox = QMessageBox()

    def setValues(self):
        IVA = float(self.mainApp.DATA_SYSTEM.SELECT_AJUSTE("IVA"))
        self.txt_iva.setValue(IVA)

        aumento = float(self.mainApp.DATA_SYSTEM.SELECT_AJUSTE("AUMENTO_VENTA"))
        self.txt_aumento.setValue(aumento)

    def guardar_admin(self):
        if self.txt_ci.text() == "" or self.txt_clave.text() == "" or self.txt_clave1.text() == "":
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "RELLENE TODOS LOS FORMULARIOS")
            return None

        if self.txt_clave.text() != self.txt_clave1.text():
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "CLAVES NO COINCIDEN")
            self.txt_clave.setText("")
            self.txt_clave1.setText("")
            self.txt_clave.setFocus()
            return None

        if self.mainApp.DATA_SYSTEM.SELECT_USER(self.txt_ci.text()) != None:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "CEDULA PERTENECE A UN USUARIO YA REGISTRADO")
            return None

        success = self.mainApp.DATA_SYSTEM.UPDATE_USER_ADMIN(self.txt_ci.text(), self.txt_clave.text())
        if success:
            QMessageBox.information(self.msgBox, "::: ATENCIÓN :::", "USUARIO ADMINISTRADOR\nACTUALIZADO CON EXITO")
        else:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "ERROR AL ACTUALIZAR EL USUARIO ADMINISTRADOR")
        
        self.txt_ci.setText("")
        self.txt_clave.setText("")
        self.txt_clave1.setText("")

    def update_valores(self):
        if self.txt_iva.value() <= 0.0 or self.txt_aumento.value() <= 0.0:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "INGRESE VALORES MAYORES A 0")
            return None

        iva_success = self.mainApp.DATA_SYSTEM.UPDATE_AJUSTE("IVA", str(self.txt_iva.value()))
        aumento_success = self.mainApp.DATA_SYSTEM.UPDATE_AJUSTE("AUMENTO_VENTA", str(self.txt_aumento.value()))
        
        if not iva_success and not aumento_success:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "ERROR AL ACTUALIZAR AMBOS VALORES")
        elif iva_success and not aumento_success:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "ERROR AL ACTUALIZAR EL VALOR DE AUMENTO")
        elif not iva_success and aumento_success:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "ERROR AL ACTUALIZAR EL VALOR DE IVA")
        else:
            QMessageBox.information(self.msgBox, "::: ATENCIÓN :::", "VALORES ACTUALIZADOS CON EXITO")
        
    def create_widgets(self):
        self.setWindowTitle("AJUSTES")
        self.setModal(True)

        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)
        
        label_admin = QtWidgets.QLabel("EDITAR USUADIO ADMINISTRADOR")
        label_admin.setFont(self.mainApp.font_m)
        #layout_main.addWidget(label_admin)

        form_admin = QtWidgets.QFormLayout()
        #layout_main.addLayout(form_admin)

        label_ci = QtWidgets.QLabel("CEDULA ADMINISTRADOR:")
        label_ci.setFont(self.mainApp.font_m)

        self.txt_ci = QtWidgets.QLineEdit()
        self.txt_ci.setFont(self.mainApp.font_m)
        form_admin.addRow(label_ci, self.txt_ci)

        label_clave = QtWidgets.QLabel("CONTRASEÑA:")
        label_clave.setFont(self.mainApp.font_m)

        self.txt_clave = QtWidgets.QLineEdit()
        self.txt_clave.setFont(self.mainApp.font_m)
        self.txt_clave.setEchoMode(QtWidgets.QLineEdit.Password)
        form_admin.addRow(label_clave, self.txt_clave)

        label_clave1 = QtWidgets.QLabel("CONFIRME CONTRASEÑA:")
        label_clave1.setFont(self.mainApp.font_m)

        self.txt_clave1 = QtWidgets.QLineEdit()
        self.txt_clave1.setFont(self.mainApp.font_m)
        self.txt_clave1.setEchoMode(QtWidgets.QLineEdit.Password)
        form_admin.addRow(label_clave1, self.txt_clave1)

        self.btn_guardar_admin = QtWidgets.QPushButton("GUARDAR CREDENCIALES")
        self.btn_guardar_admin.setFont(self.mainApp.font_m)
        self.btn_guardar_admin.clicked.connect(self.guardar_admin)
        #layout_main.addWidget(self.btn_guardar_admin)

        form_ajuste = QtWidgets.QFormLayout()
        layout_main.addLayout(form_ajuste)

        label_iva = QtWidgets.QLabel("PORCENTAJE IMPUESTO (IVA):")
        label_iva.setFont(self.mainApp.font_m)
        
        self.txt_iva = QtWidgets.QDoubleSpinBox()
        self.txt_iva.setDecimals(2)
        self.txt_iva.setFont(self.mainApp.font_m)
        form_ajuste.addRow(label_iva, self.txt_iva)

        label_aumento = QtWidgets.QLabel("PORCENTAJE AUMENTO DE VENTA:")
        label_aumento.setFont(self.mainApp.font_m)
        
        self.txt_aumento = QtWidgets.QDoubleSpinBox()
        self.txt_aumento.setDecimals(2)
        self.txt_aumento.setFont(self.mainApp.font_m)
        form_ajuste.addRow(label_aumento, self.txt_aumento)

        self.btn_guardar_valores = QtWidgets.QPushButton("GUARDAR VALORES")
        self.btn_guardar_valores.setFont(self.mainApp.font_m)
        self.btn_guardar_valores.clicked.connect(self.update_valores)
        layout_main.addWidget(self.btn_guardar_valores)

        self.show()
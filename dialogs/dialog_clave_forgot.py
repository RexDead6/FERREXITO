from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import jpype

class Dialog_clave_forgot(QtWidgets.QDialog):

    respuesta = ""

    def __init__(self, *args, **kwargs):
        super(Dialog_clave_forgot, self).__init__()
        self.mainApp = kwargs["args"]
        self.create_widgets()

        self.msgBox = QMessageBox()

    def buscar_user(self):
        respuesta_user = self.mainApp.DATA_SYSTEM.SELECT_RESPUESTAS(self.txt_user.text())

        if respuesta_user == None:
            QMessageBox.critical(self.msgBox, "::ATENCION::", "CEDULA NO REGISTRADA")
            return None

        self.respuesta = respuesta_user[1]
        self.btn_ini.setVisible(False)
        self.txt_user.setEnabled(False)
        self.txt_respuesta.setVisible(True)
        self.btn_validar.setVisible(True)
        self.label_msg.setText(respuesta_user[0])
        self.label_msg.setVisible(True)

    def validar_respuesta(self):
        if (self.respuesta != self.txt_respuesta.text()):
            QMessageBox.critical(self.msgBox, "::ATENCION::", "RESPUESTA INCORRECTA")
            self.close()
            return None
        
        self.stack.setCurrentIndex(1)

    def save_pass(self):
        if self.txt_pass.text() != self.txt_pass1.text():
            QMessageBox.critical(self.msgBox, "::ATENCION::", "CLAVES NO COINCIDEN")
            return None
        
        success = self.mainApp.DATA_SYSTEM.UPDATE_CLAVE_USER(self.txt_user.text(), self.txt_pass.text())
        if success:
            QMessageBox.information(self.msgBox, "::ATENCION::", "CLAVE ACTUALIZADA CORRECTAMENTE")
        else:
            QMessageBox.critical(self.msgBox, "::ATENCION::", "NO SE HA PODIDO ACTUALIZAR LA CLAVE, INTENTE DE NUEVO")

        self.close()

    def create_widgets(self):
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

        label_user = QtWidgets.QLabel("CEDULA DE IDENTIDAD:")
        label_user.setFont(self.mainApp.font_m)
        layout_table.addWidget(label_user)

        self.txt_user = QtWidgets.QLineEdit()
        self.txt_user.setFont(self.mainApp.font_m)
        self.txt_user.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_user, self.buscar_user, context=QtCore.Qt.WidgetShortcut)
        self.txt_user.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_user, self.buscar_user , context=QtCore.Qt.WidgetShortcut)
        layout_table.addWidget(self.txt_user)

        self.btn_ini = QtWidgets.QPushButton("BUSCAR")
        self.btn_ini.setFont(self.mainApp.font_m)
        self.btn_ini.clicked.connect(self.buscar_user)
        layout_table.addWidget(self.btn_ini)

        self.label_msg = QtWidgets.QLabel()
        self.label_msg.setFont(self.mainApp.font_m)
        self.label_msg.setVisible(False)
        layout_table.addWidget(self.label_msg)

        self.txt_respuesta = QtWidgets.QLineEdit()
        self.txt_respuesta.setFont(self.mainApp.font_m)
        self.txt_respuesta.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_respuesta, self.validar_respuesta, context=QtCore.Qt.WidgetShortcut)
        self.txt_respuesta.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_respuesta, self.validar_respuesta , context=QtCore.Qt.WidgetShortcut)
        self.txt_respuesta.setVisible(False)
        layout_table.addWidget(self.txt_respuesta)

        self.btn_validar = QtWidgets.QPushButton("ACEPTAR")
        self.btn_validar.setFont(self.mainApp.font_m)
        self.btn_validar.clicked.connect(self.validar_respuesta)
        self.btn_validar.setVisible(False)
        layout_table.addWidget(self.btn_validar)

        #--------------- FRAME INFO ---------------------

        label_user = QtWidgets.QLabel("INGRESE SU CLAVE NUEVA:")
        label_user.setFont(self.mainApp.font_g)
        layout_info.addWidget(label_user)

        layout_form = QtWidgets.QFormLayout()
        layout_info.addLayout(layout_form)

        label_pass =  QtWidgets.QLabel("CONTRASEÑA:")
        label_pass.setFont(self.mainApp.font_m)

        self.txt_pass = QtWidgets.QLineEdit()
        self.txt_pass.setFont(self.mainApp.font_m)
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_pass.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_pass, lambda: self.txt_pass1.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_pass.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_pass, lambda: self.txt_pass1.setFocus() , context=QtCore.Qt.WidgetShortcut)
        layout_form.addRow(label_pass, self.txt_pass)

        label_pass1 =  QtWidgets.QLabel("CONFIRMAR CONTRASEÑA:")
        label_pass1.setFont(self.mainApp.font_m)

        self.txt_pass1 = QtWidgets.QLineEdit()
        self.txt_pass1.setFont(self.mainApp.font_m)
        self.txt_pass1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_pass1.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_pass1, self.save_pass , context=QtCore.Qt.WidgetShortcut)
        self.txt_pass1.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_pass1, self.save_pass , context=QtCore.Qt.WidgetShortcut)
        layout_form.addRow(label_pass1, self.txt_pass1)

        self.btn_aceptar = QtWidgets.QPushButton("ACEPTAR")
        self.btn_aceptar.setFont(self.mainApp.font_m)
        self.btn_aceptar.clicked.connect(self.save_pass)
        layout_info.addWidget(self.btn_aceptar)

        self.show()
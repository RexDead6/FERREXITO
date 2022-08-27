from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

class Dialog_auth(QtWidgets.QDialog):

    mainApp = None
    success_funct = None
    error_funct = None

    def __init__(self, mainApp, success = None, error = None):
        super(Dialog_auth, self).__init__()
        self.mainApp = mainApp
        self.success_funct = success
        self.error_funct = error
        self.create_widgets()

        self.msgBox = QMessageBox()

    def auth(self):
        if self.txt_ci.text() == "" and self.txt_clave.text() == "":
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "RELLENE TODOS LOS FORMULARIOS")
            return False

        
        data = self.mainApp.DATA_SYSTEM.SELECT_USER(self.txt_ci.text(), self.txt_clave.text())

        if data == None:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "USUARIO O CONTRASEÑA INVÁLIDOS")
            self.close()
            return False

        if int(data[3]) <= 1:
            self.mainApp.temp_user = data[0]
            self.doSuccess()
        else:
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "USUARIO SIN PERMISOS VÁLIDOS")
        self.close()

    def setFuntions(self, success, error):
        self.success_funct = success
        self.error_funct = error

    def doSuccess(self):
        self.success_funct()

    def doError(self):
        self.error_funct()

    def create_widgets(self):
        layout_main = QtWidgets.QVBoxLayout()
        self.setWindowTitle("::AUTENTICACION::")
        self.setLayout(layout_main)
        self.setModal(True)

        label_titulo = QtWidgets.QLabel("AUTENTICACIÓN")
        label_titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(label_titulo)
        layout_main.setAlignment(label_titulo, QtCore.Qt.AlignHCenter)

        label_subtitle = QtWidgets.QLabel("Esta acción requiere una autenticacion\nde un usuario de nivel SUPERVISOR")
        label_subtitle.setFont(self.mainApp.font_p)
        layout_main.addWidget(label_subtitle)
        layout_main.setAlignment(label_subtitle, QtCore.Qt.AlignHCenter)

        form_auth = QtWidgets.QFormLayout()
        layout_main.addLayout(form_auth)

        label_ci = QtWidgets.QLabel("CEDULA:")
        label_ci.setFont(self.mainApp.font_m)
        
        self.txt_ci = QtWidgets.QLineEdit()
        self.txt_ci.setFont(self.mainApp.font_m)
        self.txt_ci.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_ci, lambda: self.txt_clave.setFocus(), context=QtCore.Qt.WidgetShortcut)
        self.txt_ci.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_ci, lambda: self.txt_clave.setFocus(), context=QtCore.Qt.WidgetShortcut)
        form_auth.addRow(label_ci, self.txt_ci)

        label_clave = QtWidgets.QLabel("CONTRASEÑA:")
        label_clave.setFont(self.mainApp.font_m)
        
        self.txt_clave = QtWidgets.QLineEdit()
        self.txt_clave.setFont(self.mainApp.font_m)
        self.txt_clave.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_clave.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_clave, self.auth, context=QtCore.Qt.WidgetShortcut)
        self.txt_clave.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_clave, self.auth, context=QtCore.Qt.WidgetShortcut)
        form_auth.addRow(label_clave, self.txt_clave)

        buttons_layout = QtWidgets.QHBoxLayout()
        layout_main.addLayout(buttons_layout)

        self.btn_aceptar = QtWidgets.QPushButton("ACEPTAR")
        self.btn_aceptar.setFont(self.mainApp.font_m)
        self.btn_aceptar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_aceptar.clicked.connect(self.auth)
        buttons_layout.addWidget(self.btn_aceptar)

        self.btn_cancelar = QtWidgets.QPushButton("CANCELAR")
        self.btn_cancelar.setFont(self.mainApp.font_m)
        self.btn_cancelar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.btn_cancelar.clicked.connect(lambda: self.close())
        buttons_layout.addWidget(self.btn_cancelar)

        self.show()
from PyQt5 import QtGui, QtCore, QtWidgets

from dialogs.dialog_clave_forgot import Dialog_clave_forgot

class Frame_login(QtWidgets.QFrame):

    mainApp = None

    def __init__(self, *args, **kwargs):
        super(Frame_login, self).__init__()
        self.mainApp = kwargs['args']
        self.create_widgets()

    def iniciar_sesion(self):
        data = self.mainApp.DATA_SYSTEM.SELECT_USER(self.txt_user.text(), self.txt_clave.text())
        
        self.txt_user.setText("")
        self.txt_clave.setText("")

        if data == None:
            self.label_msg.setVisible(True)
            self.txt_user.setFocus()
            return None
        
        self.mainApp.nombre  = data[2]
        self.mainApp.id_user = data[0]
        self.mainApp.cargo   = int(data[3])

        cargo_n = "Administrador"
        if data[3] == "1": cargo_n = "Supervisor"
        if data[3] == "2": cargo_n = "Operador"

        self.mainApp.label_user.setVisible(True)
        self.mainApp.label_user.setText("{} - {}".format(data[2], cargo_n))

        self.mainApp.action_compra.setVisible(True)
        self.mainApp.logistica_menu.setEnabled(True)
        self.mainApp.action_empleados.setVisible(True)
        self.mainApp.action_inventario.setVisible(True)
        self.mainApp.administracion_menu.setEnabled(True)

        if self.mainApp.cargo == 1:
            self.mainApp.action_empleados.setVisible(False)
            self.mainApp.action_inventario.setVisible(False)
        elif self.mainApp.cargo == 2:
            self.mainApp.action_compra.setVisible(False)
            self.mainApp.logistica_menu.setEnabled(False)
            self.mainApp.administracion_menu.setEnabled(False)
        self.mainApp.menubar.setVisible(True)

        if self.mainApp.cargo < 2:
            self.mainApp.change_frame("inicio")
        else:
            self.mainApp.change_frame("venta")

    def olvide_clave(self):
        self.dialog = Dialog_clave_forgot(args=self.mainApp)

    def create_widgets(self):
        self.setStyleSheet("QFrame{background-color: #C6C38B; margin:0}")
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        frame_ini = QtWidgets.QFrame()
        layout_main.addWidget(frame_ini)
        layout_main.setAlignment(frame_ini, QtCore.Qt.AlignCenter)

        layout_frame = QtWidgets.QVBoxLayout()
        frame_ini.setLayout(layout_frame)

        label_logo = QtWidgets.QLabel()
        label_logo.setLineWidth(0)
        label_logo.setPixmap(QtGui.QPixmap("./img/logo.png").scaled(400, 200, QtCore.Qt.KeepAspectRatio))
        label_logo.setScaledContents(True)
        layout_frame.addWidget(label_logo)
        layout_frame.setAlignment(label_logo, QtCore.Qt.AlignVCenter)

        self.label_msg = QtWidgets.QLabel("USUARIO O CONTRASEÑA\n           INVALIDOS")
        self.label_msg.setFont(self.mainApp.font_m)
        self.label_msg.setStyleSheet("QLabel{color: red}")
        self.label_msg.setVisible(False)
        layout_frame.addWidget(self.label_msg)

        label_user = QtWidgets.QLabel("CEDULA DE IDENTIDAD:")
        label_user.setFont(self.mainApp.font_m)
        layout_frame.addWidget(label_user)

        self.txt_user = QtWidgets.QLineEdit()
        self.txt_user.setFont(self.mainApp.font_m)
        self.txt_user.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_user, lambda: self.txt_clave.setFocus(), context=QtCore.Qt.WidgetShortcut)
        self.txt_user.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_user, lambda: self.txt_clave.setFocus() , context=QtCore.Qt.WidgetShortcut)
        layout_frame.addWidget(self.txt_user)

        label_clave = QtWidgets.QLabel("CONTRASEÑA:")
        label_clave.setFont(self.mainApp.font_m)
        layout_frame.addWidget(label_clave)

        self.txt_clave = QtWidgets.QLineEdit()
        self.txt_clave.setFont(self.mainApp.font_m)
        self.txt_clave.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_clave.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_clave, self.iniciar_sesion, context=QtCore.Qt.WidgetShortcut)
        self.txt_clave.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_clave, self.iniciar_sesion , context=QtCore.Qt.WidgetShortcut)
        layout_frame.addWidget(self.txt_clave)

        self.btn_ini = QtWidgets.QPushButton("INICIAR SESION")
        self.btn_ini.setFont(self.mainApp.font_m)
        self.btn_ini.clicked.connect(self.iniciar_sesion)
        layout_frame.addWidget(self.btn_ini)

        self.label_pass = QtWidgets.QPushButton("¿Has olvidado tu contraseña?")
        self.label_pass.setFont(self.mainApp.font_m)
        self.label_pass.clicked.connect(self.olvide_clave)
        layout_frame.addWidget(self.label_pass)
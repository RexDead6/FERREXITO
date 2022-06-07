from PyQt5 import QtGui, QtCore, QtWidgets

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
        self.mainApp.change_frame("venta")

        self.mainApp.menubar.setVisible(True)

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
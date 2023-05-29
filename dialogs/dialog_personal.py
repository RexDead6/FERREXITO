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
            self.txt_id.setText(self.personal[0])
            self.txt_ci.setText(self.personal[1])
            self.txt_ci.setReadOnly(True)
            self.txt_nombre.setText(self.personal[2])
            self.box_cargo.setCurrentIndex(int(self.personal[3]))
            self.label_pass_current.setVisible(True)
            self.txt_pass_current.setVisible(True)
        else:
            self.label_pass_current.setVisible(False)
            self.txt_pass_current.setVisible(False)

    def register_user(self):
        if self.txt_ci.text() == "" or self.box_cargo.currentIndex() == 0 or self.txt_nombre.text() == "" or self.txt_pass.text() == "" or self.txt_pass1.text() == "" or self.box_pregunta1.currentIndex() == 0 or self.box_pregunta2.currentIndex() == 0 or self.box_pregunta3.currentIndex() == 0 or self.txt_respuesta1.text() == "" or self.txt_respuesta2.text() == "" or self.txt_respuesta3.text() == "":
            QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "RELLENE TODOS LOS FORMULARIOS")
            return None
        
        if not self.IS_EDIT:
            if self.txt_pass.text() != self.txt_pass1.text():
                QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "CONTRASEÑAS NO COINCIDEN")
                self.txt_pass.setText("")
                self.txt_pass1.setText("")
                self.txt_pass.setFocus()
                return None

            USER_DATA = self.mainApp.DATA_SYSTEM.SELECT_USER(self.txt_ci.text())
            print(USER_DATA)
            if USER_DATA != None:
                QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "USUARIO YA HA SIDO REGISTRADO")
                return None

            SUCCESS = self.mainApp.DATA_SYSTEM.INSERT_USER(self.txt_ci.text(), self.txt_nombre.text(), self.box_cargo.currentIndex(), self.txt_pass.text())
            if SUCCESS:
                self.mainApp.DATA_SYSTEM.INSERT_RESPUESTA(self.txt_respuesta1.text(), self.box_pregunta1.currentText(), self.txt_ci.text())
                self.mainApp.DATA_SYSTEM.INSERT_RESPUESTA(self.txt_respuesta2.text(), self.box_pregunta2.currentText(), self.txt_ci.text())
                self.mainApp.DATA_SYSTEM.INSERT_RESPUESTA(self.txt_respuesta3.text(), self.box_pregunta3.currentText(), self.txt_ci.text())
                QMessageBox.information(self.msgBox, "::: OPERACIÓN EXITOSA :::", "USUARIO REGISTRADO EXITOSAMENTE")
                self.mainApp.frame_personal.add_data_table()
                self.close()
            else:
                QMessageBox.Critical(self.msgBox, "::: ATENCIÓN :::", "ERROR AL REGISTRAR USUARIO, INTENTE DE NUEVO")
        else:
            user = self.mainApp.DATA_SYSTEM.SELECT_USER(self.txt_ci.text(), self.txt_pass_current.text())
            if user == None:
                QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "CONTRASEÑA ACTUAL INCORRECTA")
                return None

            password = self.txt_pass_current.text()

            if self.txt_pass1.text() != "" and self.txt_pass.text() != "":
                if self.txt_pass.text() != self.txt_pass1.text():
                    QMessageBox.critical(self.msgBox, "::: ATENCIÓN :::", "CONTRASEÑA NUEVA NO COINCIDEN")
                    return None
                password = self.txt_pass.text()
            SUCCESS = self.mainApp.DATA_SYSTEM.UPDATE_USER(self.txt_id.text(), self.txt_nombre.text(), str(self.box_cargo.currentIndex()), password)
            if SUCCESS:
                QMessageBox.information(self.msgBox, "::: OPERACIÓN EXITOSA :::", "USUARIO ACTUALIZADO EXITOSAMENTE")
                self.mainApp.frame_personal.add_data_table()
                self.close()
            else:
                QMessageBox.Critical(self.msgBox, "::: ATENCIÓN :::", "ERROR AL ACTUALIZAR USUARIO, INTENTE DE NUEVO")

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

        self.txt_id = QtWidgets.QLineEdit()
        self.txt_id.setFont(self.mainApp.font_m)
        self.txt_id.setVisible(False)
        form_layout.addWidget(self.txt_id)

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
        self.txt_pass1.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_pass1, lambda: self.box_pregunta1.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_pass1.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_pass1, lambda: self.box_pregunta1.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_pass1, self.txt_pass1)

        self.label_pass_current = QtWidgets.QLabel("CONTRASEÑA ACTUAL:")
        self.label_pass_current.setFont(self.mainApp.font_m)

        self.txt_pass_current = QtWidgets.QLineEdit()
        self.txt_pass_current.setFont(self.mainApp.font_m)
        self.txt_pass_current.setEchoMode(QtWidgets.QLineEdit.Password)
        form_layout.addRow(self.label_pass_current, self.txt_pass_current)

        layout_button = QtWidgets.QHBoxLayout()
        main_layout.addLayout(layout_button)
        main_layout.setAlignment(layout_button, QtCore.Qt.AlignHCenter)

        label_pregunta1 =  QtWidgets.QLabel("PREGUNTA SEGURIDAD 1:")
        label_pregunta1.setFont(self.mainApp.font_m)

        preguntas = self.mainApp.DATA_SYSTEM.SELECT_PREGUNTAS();

        self.box_pregunta1 = QtWidgets.QComboBox()
        self.box_pregunta1.addItem("---SELECCIONE---")
        self.box_pregunta1.addItem(preguntas[0][1])
        self.box_pregunta1.addItem(preguntas[1][1])
        self.box_pregunta1.addItem(preguntas[2][1])
        self.box_pregunta1.setFont(self.mainApp.font_m)
        self.box_pregunta1.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.box_pregunta1, lambda: self.txt_respuesta1.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.box_pregunta1.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.box_pregunta1, lambda: self.txt_respuesta1.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_pregunta1, self.box_pregunta1)

        label_respuesta1 =  QtWidgets.QLabel("RESPUESTA SEGURIDAD 1:")
        label_respuesta1.setFont(self.mainApp.font_m)

        self.txt_respuesta1 = QtWidgets.QLineEdit()
        self.txt_respuesta1.setFont(self.mainApp.font_m)
        self.txt_respuesta1.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_respuesta1, lambda: self.box_pregunta2.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_respuesta1.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_respuesta1, lambda: self.box_pregunta2.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_respuesta1, self.txt_respuesta1)

        label_pregunta2 =  QtWidgets.QLabel("PREGUNTA SEGURIDAD 2:")
        label_pregunta2.setFont(self.mainApp.font_m)

        self.box_pregunta2 = QtWidgets.QComboBox()
        self.box_pregunta2.addItem("---SELECCIONE---")
        self.box_pregunta2.addItem(preguntas[3][1])
        self.box_pregunta2.addItem(preguntas[4][1])
        self.box_pregunta2.addItem(preguntas[5][1])
        self.box_pregunta2.setFont(self.mainApp.font_m)
        self.box_pregunta2.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.box_pregunta2, lambda: self.txt_respuesta2.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.box_pregunta2.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.box_pregunta2, lambda: self.txt_respuesta2.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_pregunta2, self.box_pregunta2)

        label_respuesta2 =  QtWidgets.QLabel("RESPUESTA SEGURIDAD 2:")
        label_respuesta2.setFont(self.mainApp.font_m)

        self.txt_respuesta2 = QtWidgets.QLineEdit()
        self.txt_respuesta2.setFont(self.mainApp.font_m)
        self.txt_respuesta2.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_respuesta2, lambda: self.box_pregunta3.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.txt_respuesta2.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_respuesta2, lambda: self.box_pregunta3.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_respuesta2, self.txt_respuesta2)

        label_pregunta3 =  QtWidgets.QLabel("PREGUNTA SEGURIDAD 3:")
        label_pregunta3.setFont(self.mainApp.font_m)

        self.box_pregunta3 = QtWidgets.QComboBox()
        self.box_pregunta3.addItem("---SELECCIONE---")
        self.box_pregunta3.addItem(preguntas[6][1])
        self.box_pregunta3.addItem(preguntas[7][1])
        self.box_pregunta3.addItem(preguntas[8][1])
        self.box_pregunta3.setFont(self.mainApp.font_m)
        self.box_pregunta3.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.box_cargo, lambda: self.txt_respuesta3.setFocus() , context=QtCore.Qt.WidgetShortcut)
        self.box_pregunta3.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.box_cargo, lambda: self.txt_respuesta3.setFocus() , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_pregunta3, self.box_pregunta3)

        label_respuesta3 =  QtWidgets.QLabel("RESPUESTA SEGURIDAD 3:")
        label_respuesta3.setFont(self.mainApp.font_m)

        self.txt_respuesta3 = QtWidgets.QLineEdit()
        self.txt_respuesta3.setFont(self.mainApp.font_m)
        self.txt_respuesta3.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_respuesta3, lambda: self.register_user , context=QtCore.Qt.WidgetShortcut)
        self.txt_respuesta3.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_respuesta3, lambda: self.register_user , context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_respuesta3, self.txt_respuesta3)

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
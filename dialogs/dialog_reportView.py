from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pdfkit

class Dialog_reportView(QtWidgets.QDialog):

    FILE_NAME = None
    
    def __init__(self, *args, **kwargs):
        super(Dialog_reportView, self).__init__()
        self.mainApp = kwargs["args"][0]
        self.FILE_NAME = kwargs["args"][1]
        self.msg = QMessageBox()
        self.create_widgets()
        self.label_nombre.setText(self.FILE_NAME)

        with open("./templates/html_temp_report.html") as f:
            self.webEngine.setHtml(f.read())

    def guardar(self):
        self.btn_guardar.setEnabled(False)
        PATH_TO_INIT = self.mainApp.DATA_SYSTEM.SELECT_AJUSTE("path_pdf")
        if PATH_TO_INIT == "":
            PATH_TO_SAVE = QFileDialog.getExistingDirectory(
                self,
                caption="Seleccione una carpeta"
            )
        else:
            PATH_TO_SAVE = QFileDialog.getExistingDirectory(
                self,
                caption="Seleccione una carpeta",
                directory=PATH_TO_INIT
            )
        pdfkit.from_file("templates/html_temp_report.html", PATH_TO_SAVE+"/"+self.FILE_NAME, options={"enable-local-file-access": ""})
        self.mainApp.DATA_SYSTEM.UPDATE_AJUSTE("path_pdf", PATH_TO_SAVE)
        QMessageBox.information(self.msg, "::REPORTE::", "REPORTE GENERADO CON ÉXITO")
        self.close()

    def create_widgets(self):
        self.resize(800, 600)
        self.setWindowTitle("Reporte")
        self.setModal(True)
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        frame_header = QtWidgets.QFrame()
        header_layout = QtWidgets.QHBoxLayout()
        frame_header.setLayout(header_layout)
        layout_main.addWidget(frame_header)

        self.label_nombre = QtWidgets.QLabel("nombre_documento")
        self.label_nombre.setFont(self.mainApp.font_m)
        header_layout.addWidget(self.label_nombre, QtCore.Qt.AlignLeft)

        self.btn_guardar = QtWidgets.QPushButton('Guardar')
        self.btn_guardar.setMaximumWidth(120)
        self.btn_guardar.setMinimumHeight(40)
        self.btn_guardar.clicked.connect(self.guardar)
        header_layout.addWidget(self.btn_guardar, QtCore.Qt.AlignRight)

        self.webEngine = QWebEngineView()
        layout_main.addWidget(self.webEngine)
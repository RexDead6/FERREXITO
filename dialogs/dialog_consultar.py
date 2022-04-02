from csv import QUOTE_ALL
from PyQt5 import QtWidgets, QtCore, QtGui

class Dialog_consultar(QtWidgets.QDialog):

    mainApp = None

    def __init__(self, *args, **kwargs):
        super(Dialog_consultar, self).__init__()
        self.mainApp = kwargs["args"]
        self.create_widgets()

    def enter_barcode(self):
        if self.txt_barcode.text() == "":
            return None

        producto = self.mainApp.DATA_SYSTEM.SELECT_PRODUCTO(self.txt_barcode.text())
        if producto != None:
            self.label_data.setText("DESCRIPCION: {}\nPRECIO:     {}".format(producto[2], self.mainApp.formato_moneda(float(producto[4]))))
        else:
            self.label_data.setText("ARTICULO INEXISTENTE\nDESCRIPCION:\nPRECIO:")

    def create_widgets(self):
        self.setWindowTitle("CONSULTAR PRODUCTO")
        self.setModal(True)

        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)

        titulo = QtWidgets.QLabel("CONSULTA DE PRECIOS")
        titulo.setFont(self.mainApp.font_g)
        layout_main.addWidget(titulo)
        layout_main.setAlignment(titulo, QtCore.Qt.AlignHCenter)

        form_layout = QtWidgets.QFormLayout()
        layout_main.addLayout(form_layout)

        label_barcode = QtWidgets.QLabel("CODIGO DE BARRA:")
        label_barcode.setFont(self.mainApp.font_m)
        
        self.txt_barcode = QtWidgets.QLineEdit()
        self.txt_barcode.setFont(self.mainApp.font_m)
        self.txt_barcode.enter_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self.txt_barcode, self.enter_barcode, context=QtCore.Qt.WidgetShortcut)
        self.txt_barcode.return_short_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Return'), self.txt_barcode, self.enter_barcode, context=QtCore.Qt.WidgetShortcut)
        form_layout.addRow(label_barcode, self.txt_barcode)

        self.label_data = QtWidgets.QLabel("DESCRIPCION:\nPRECIO:")
        self.label_data.setFont(self.mainApp.font_m)
        layout_main.addWidget(self.label_data)
        layout_main.setAlignment(self.label_data, QtCore.Qt.AlignLeft)

        self.show()
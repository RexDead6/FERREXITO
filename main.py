from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import jpype

from frm_compra import Frame_compra
from frm_facturacion import Frame_facturacion
from frm_login import Frame_login
from frm_tabla_productos import Tabla_productos
from frm_tabla_empleados import Tabla_empleados
from frm_tabla_movimientos import Tabla_movimientos

class windows_main(QtWidgets.QMainWindow):

    DATA_SYSTEM  = None
    id_user      = None
    cargo        = None
    block_change = False

    def __init__(self):
        super(windows_main, self).__init__()
        self.initializate_java_class()
        self.create_widgets()

    def initializate_java_class(self):
        jpype.startJVM(classpath=['java/DATA_SYSTEM.jar'], convertStrings=True)
        self.DATA_SYSTEM = jpype.JClass("core.DATA_CLASS")()

    def formato_moneda(self, monto):
        return "{:,.2f}".format(monto).replace(".", "#").replace(",", ".").replace("#", ",")

    def input_format_number(self, txt):
            new_string = ""
            for num in txt.text():
                try:
                    int(num)
                    new_string = new_string+num
                except ValueError:
                    pass
            txt.setText(new_string)

    def change_frame(self, f):
        if self.block_change:
            return None

        if f == "venta":
            self.stack.setCurrentIndex(1)
            self.frame_facturacion.default_forms()
        elif f == "compra":
            self.stack.setCurrentIndex(2)
            self.frame_compra.default_forms()
        elif f == "productos":
            self.stack.setCurrentIndex(3)
            self.frame_productos.add_data_table()
        elif f == "movimientos":
            self.stack.setCurrentIndex(4)
            self.frame_movimientos.add_data_table()
        elif f == "empleados":
            self.stack.setCurrentIndex(5)
            self.frame_personal.add_data_table()

    def create_widgets(self):
        self.setWindowTitle("FERREXITO")

        cw = QtWidgets.QWidget()
        self.setCentralWidget(cw)
        layout_main = QtWidgets.QVBoxLayout()
        cw.setLayout(layout_main)

        # FUENTES
        self.font_p = QtGui.QFont()
        self.font_p.setPointSize(10)

        self.font_m = QtGui.QFont()
        self.font_m.setPointSize(15)

        self.font_g = QtGui.QFont()
        self.font_g.setBold(True)
        self.font_g.setPointSize(20)

        # FRAMES/PANTALLAS DE LA VENTANA
        self.frame_login       = Frame_login(args=self)
        self.frame_facturacion = Frame_facturacion(args=self)
        self.frame_compra      = Frame_compra(args=self)
        self.frame_productos   = Tabla_productos(args=self)
        self.frame_movimientos = Tabla_movimientos(args=self)
        self.frame_personal    = Tabla_empleados(args=self)

        # STACK DE CADA FRAME
        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.frame_login)       # 0
        self.stack.addWidget(self.frame_facturacion) # 1
        self.stack.addWidget(self.frame_compra)      # 2
        self.stack.addWidget(self.frame_productos)   # 3
        self.stack.addWidget(self.frame_movimientos) # 4
        self.stack.addWidget(self.frame_personal)    # 5
        layout_main.addWidget(self.stack)

        # MENU BAR
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setVisible(False)
        self.setMenuBar(self.menubar)

        action_compra = QtWidgets.QAction("COMPRA (PROVEEDORES)", self)
        action_compra.triggered.connect(lambda: self.change_frame("compra"))

        action_venta = QtWidgets.QAction("VENTA (CLIENTES)", self)
        action_venta.triggered.connect(lambda: self.change_frame("venta"))

        action_inventario = QtWidgets.QAction("AJUSTES DE INV.", self)
        #action_inventario.triggered.connect(lambda: self.stack.setCurrentIndex())

        facturacion_menu = self.menubar.addMenu("FACTURACION")
        facturacion_menu.addAction(action_compra)
        facturacion_menu.addAction(action_venta)
        facturacion_menu.addAction(action_inventario)

        action_productos = QtWidgets.QAction("PRODUCTOS", self)
        action_productos.triggered.connect(lambda: self.change_frame("productos"))
        
        action_empleados = QtWidgets.QAction("EMPLEADOS", self)
        action_empleados.triggered.connect(lambda: self.change_frame("empleados"))

        action_movimientos = QtWidgets.QAction("MOVIMIENTOS", self)
        action_movimientos.triggered.connect(lambda: self.change_frame("movimientos"))

        action_auditoria = QtWidgets.QAction("AUDITORIA", self)
        #action_auditoria.triggered.connect(lambda: self.change_frame("productos"))

        logistica_menu = self.menubar.addMenu("LOGÍSTICA")
        logistica_menu.addAction(action_productos)
        logistica_menu.addAction(action_empleados)
        logistica_menu.addAction(action_movimientos)
        logistica_menu.addAction(action_auditoria)

app = QtWidgets.QApplication([])
application = windows_main()
application.showMaximized()
sys.exit(app.exec())
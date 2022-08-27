from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import jpype

from class_reports import Reports
from frm_compra import Frame_compra
from frm_facturacion import Frame_facturacion
from frm_login import Frame_login
from frm_tabla_productos import Tabla_productos
from frm_tabla_empleados import Tabla_empleados
from frm_tabla_movimientos import Tabla_movimientos
from frm_devolucion import Frame_devolucion
from frm_inventario import Frame_inventario
from frm_auditoria import Tabla_auditoria
from frm_inicio import Frame_inicio
from dialogs.dialog_ajustes import Dialog_ajustes

class windows_main(QtWidgets.QMainWindow):

    DATA_SYSTEM  = None
    id_user      = None
    cargo        = 0
    block_change = False
    nombre       = ""
    temp_user    = ""

    def __init__(self):
        super(windows_main, self).__init__()
        self.initializate_java_class()
        self.create_widgets()

    def reporte_venta(self, num_factura):
        data_raw = self.DATA_SYSTEM.SELECT_FACTURA(num_factura)
        data = {
            "ci": data_raw[0][2],
            "cliente": data_raw[0][3],
            "direccion": data_raw[0][4],
            "n_factura": data_raw[0][0],
            "fecha_factura": self.formato_fecha(data_raw[0][1]),
            "subtotal": self.formato_moneda(float(data_raw[0][11])),
            "iva_porcent": self.formato_moneda(float(data_raw[0][9])),
            "iva": self.formato_moneda(float(data_raw[0][10])),
            "total": self.formato_moneda(float(data_raw[0][12]))
        }

        productos = list()

        for list_data in data_raw:
            producto = {
                "descripcion": list_data[5],
                "cantidad": list_data[7],
                "costo": self.formato_moneda(float(list_data[6])),
                "monto": self.formato_moneda(float(list_data[8]))
            }
            productos.append(producto)

        data["productos"] = productos
        
        return Reports(
        "venta_template.html", 
        data).execute()
        
    def setTempUser(self, id):
        self.temp_user = id

    def initializate_java_class(self):
        jpype.startJVM(classpath=['java/DATA_SYSTEM.jar'], convertStrings=True)
        self.DATA_SYSTEM = jpype.JClass("core.DATA_CLASS")()

    def formato_moneda(self, monto):
        return "{:,.2f}".format(monto).replace(".", "#").replace(",", ".").replace("#", ",")

    def formato_fecha(self, data):
        return "{}/{}/{} {}".format(data[8:10], data[5:7], data[:4], data[11:])

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
            self.setWindowTitle("FACTURACIÓN - {}".format(self.nombre))
        elif f == "compra":
            self.stack.setCurrentIndex(2)
            self.frame_compra.default_forms()
            self.setWindowTitle("COMPRA A PROVEEDORES - {}".format(self.nombre))
        elif f == "productos":
            self.stack.setCurrentIndex(3)
            self.frame_productos.add_data_table()
            self.setWindowTitle("INVENTARIO DE PRODUCTOS - {}".format(self.nombre))
        elif f == "movimientos":
            self.stack.setCurrentIndex(4)
            self.frame_movimientos.add_data_table()
            self.setWindowTitle("MOVIMIENTOS DEL INVENTARIO - {}".format(self.nombre))
        elif f == "empleados":
            self.stack.setCurrentIndex(5)
            self.frame_personal.add_data_table()
            self.setWindowTitle("EMPLEADOS DEL SISTEMA - {}".format(self.nombre))
        elif f == "devolucion":
            self.frame_devolucion.clear_forms()
            self.stack.setCurrentIndex(6)
            self.setWindowTitle("DEVOLUCION DE PRODUCTOS - {}".format(self.nombre))
        elif f == "login":
            self.stack.setCurrentIndex(0)
            self.id_user = 0
            self.cargo   = 0
            self.menubar.setVisible(False)
            self.frame_login.txt_user.setFocus()
            self.setWindowTitle("INICIAR SESION")
        elif f == "inventario":
            self.stack.setCurrentIndex(7)
            self.setWindowTitle("AJUSTE DE INVENTARIO - {}".format(self.nombre))
        elif f == "auditoria":
            self.stack.setCurrentIndex(8)
            self.frame_auditoria.add_data_table()
        elif f == "inicio":
            self.stack.setCurrentIndex(9)
            self.frame_inicio.add_data_table()
        elif f == "ajustes":
            self.dialog_ajustes = Dialog_ajustes(args=self)

    def create_widgets(self):
        self.setWindowTitle("FERREXITO")
        self.setStyleSheet("QPushButton{padding: 10px}")
        self.setWindowIcon(QtGui.QIcon('img/icon.png'))

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
        self.frame_login              = Frame_login(args=self)
        self.frame_facturacion        = Frame_facturacion(args=self)
        self.frame_compra             = Frame_compra(args=self)
        self.frame_productos          = Tabla_productos(args=self)
        self.frame_movimientos        = Tabla_movimientos(args=self)
        self.frame_personal           = Tabla_empleados(args=self)
        self.frame_devolucion         = Frame_devolucion(args=self)
        self.frame_inventario         = Frame_inventario(args=self)
        self.frame_auditoria          = Tabla_auditoria(args=self)
        self.frame_inicio             = Frame_inicio(args=self)

        # STACK DE CADA FRAME
        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.frame_login)              # 0
        self.stack.addWidget(self.frame_facturacion)        # 1
        self.stack.addWidget(self.frame_compra)             # 2
        self.stack.addWidget(self.frame_productos)          # 3
        self.stack.addWidget(self.frame_movimientos)        # 4
        self.stack.addWidget(self.frame_personal)           # 5
        self.stack.addWidget(self.frame_devolucion)         # 6
        self.stack.addWidget(self.frame_inventario)         # 7
        self.stack.addWidget(self.frame_auditoria)          # 8
        self.stack.addWidget(self.frame_inicio)             # 9
        layout_main.addWidget(self.stack)

        # MENU BAR
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setVisible(False)
        self.setMenuBar(self.menubar)

        self.action_compra = QtWidgets.QAction("COMPRA (PROVEEDORES)", self)
        self.action_compra.triggered.connect(lambda: self.change_frame("compra"))

        self.action_venta = QtWidgets.QAction("VENTA (CLIENTES)", self)
        self.action_venta.triggered.connect(lambda: self.change_frame("venta"))

        self.facturacion_menu = self.menubar.addMenu("FACTURACION")
        self.facturacion_menu.addAction(self.action_compra)
        self.facturacion_menu.addAction(self.action_venta)

        self.action_inicio = QtWidgets.QAction("INICIO", self)
        self.action_inicio.triggered.connect(lambda: self.change_frame("inicio"))

        self.action_productos = QtWidgets.QAction("PRODUCTOS", self)
        self.action_productos.triggered.connect(lambda: self.change_frame("productos"))

        self.action_movimientos = QtWidgets.QAction("MOVIMIENTOS", self)
        self.action_movimientos.triggered.connect(lambda: self.change_frame("movimientos"))

        self.logistica_menu = self.menubar.addMenu("LOGÍSTICA")
        self.logistica_menu.addAction(self.action_inicio)
        self.logistica_menu.addAction(self.action_productos)
        self.logistica_menu.addAction(self.action_movimientos)

        self.action_empleados = QtWidgets.QAction("EMPLEADOS", self)
        self.action_empleados.triggered.connect(lambda: self.change_frame("empleados"))

        self.action_auditoria = QtWidgets.QAction("AUDITORIA", self)
        self.action_auditoria.triggered.connect(lambda: self.change_frame("auditoria"))

        self.action_inventario = QtWidgets.QAction("AJUSTES DE INV.", self)
        self.action_inventario.triggered.connect(lambda: self.change_frame("inventario"))

        self.action_ajustes = QtWidgets.QAction("AJUSTES GENERALES", self)
        self.action_ajustes.triggered.connect(lambda: self.change_frame("ajustes"))

        self.administracion_menu = self.menubar.addMenu("ADMINISTRACION")
        self.administracion_menu.addAction(self.action_empleados)
        self.administracion_menu.addAction(self.action_auditoria)
        self.administracion_menu.addAction(self.action_inventario)
        self.administracion_menu.addAction(self.action_ajustes)

        self.action_cerrar_sesion = QtWidgets.QAction("CERRAR SESIÓN", self)
        self.action_cerrar_sesion.triggered.connect(lambda: self.change_frame("login"))

        self.action_cerrar_app = QtWidgets.QAction("CERRAR", self)
        self.action_cerrar_app.triggered.connect(self.close)

        self.sesion_menu = self.menubar.addMenu("SESIÓN")
        self.sesion_menu.addAction(self.action_cerrar_sesion)
        self.sesion_menu.addAction(self.action_cerrar_app)

app = QtWidgets.QApplication([])
application = windows_main()
application.showMaximized()
sys.exit(app.exec())
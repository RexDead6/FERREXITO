package core;

import java.sql.*;
import java.io.File;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * CLASS TO MANAGE DATA BASE
 *
 * @author Alba
 */
public final class DATA_BASE {

    public Connection con = null;

    /*public static void main(String[] args){
        DATA_BASE a = new DATA_BASE();
    }*/
    public DATA_BASE() {
        //OPEN_MYSQL();
        OPEN_DB();
        if (!CHEK_TABLES()){
            CREATE_DATA_BASE();
        }

    }

    public void OPEN_MYSQL() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver"); 
            con = DriverManager.getConnection("jdbc:mysql://localhost/venmark_system", "root", "");
            con.setAutoCommit(false);
        } catch (SQLException | ClassNotFoundException e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
        }
        System.out.println("Opened database successfully");
    }

    /**
     * METHOD TO OPEN AND CREATE THE DATA BASE (.db FILE)
     */
    public void OPEN_DB() {
        try {
            Class.forName("org.sqlite.JDBC");
            con = DriverManager.getConnection("jdbc:sqlite:data/DATA_SYSTEM.db");
            con.setAutoCommit(false);
        } catch (ClassNotFoundException | SQLException e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
        }
        System.out.println("Opened database successfully");
    }

    public boolean CHEK_TABLES() {

        Statement stmt = null;
        try {
            stmt = con.createStatement();
            ResultSet rs;

            rs = stmt.executeQuery("SELECT * FROM cliente;");
            rs = stmt.executeQuery("SELECT * FROM compra;");
            rs = stmt.executeQuery("SELECT * FROM cuerpo;");
            rs = stmt.executeQuery("SELECT * FROM cuerpo_productos;");
            rs = stmt.executeQuery("SELECT * FROM devolucion;");
            rs = stmt.executeQuery("SELECT * FROM inventario;");
            rs = stmt.executeQuery("SELECT * FROM pago;");
            rs = stmt.executeQuery("SELECT * FROM personal;");
            rs = stmt.executeQuery("SELECT * FROM producto;");
            rs = stmt.executeQuery("SELECT * FROM proveedor;");
            rs = stmt.executeQuery("SELECT * FROM venta;");
            rs = stmt.executeQuery("SELECT * FROM auditoria;");
            rs = stmt.executeQuery("SELECT * FROM cierres;");
            rs = stmt.executeQuery("SELECT * FROM preguntas_seguridad;");
            rs = stmt.executeQuery("SELECT * FROM respuestas_seguridad;");

        } catch (SQLException ex) {
            if (ex.toString().substring(74, 87).equals("no such table")) {
                return false;
            } else {
                System.out.println(ex);
                return false;
            }
        }
        return true;
    }

    /**
     * METHOD TO CREATE TABLES, ROW AND COLUMNS IN ALL DATA BASE FILE
     *
     * @return TRUE IF CREATE EVERYTHING FINISH GOOD ELSE FALSE
     */
    private boolean CREATE_DATA_BASE() {
        try {
            con.close();
        } catch (SQLException ex) {
            Logger.getLogger(DATA_BASE.class.getName()).log(Level.SEVERE, null, ex);
        }
        con = null;

        File data = new File("data/DATA_SYSTEM.db");
        data.delete();

        OPEN_DB();

        try {
            Statement stmt = con.createStatement();

            String sql = "CREATE TABLE `producto` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`codigo` VARCHAR(20) NOT NULL DEFAULT '0',\n"
                    + "	`descripcion` VARCHAR(50) NOT NULL DEFAULT '',\n"
                    + "	`existencia` INT(11) NOT NULL DEFAULT '0',\n"
                    + "	`costo_venta` VARCHAR(50) NOT NULL DEFAULT '0.0',\n"
                    + "	`cantidad_min` INT(11) NOT NULL DEFAULT '10',\n"
                    + "	`cantidad_max` INT(11) NOT NULL DEFAULT '10');\n"
                    + "INSERT INTO producto (codigo, descripcion, existencia, costo_venta, cantidad_min, cantidad_max) VALUES ('01', 'MARTILLO', 200, '20.0', 10, 500);"
                    + "INSERT INTO producto (codigo, descripcion, existencia, costo_venta, cantidad_min, cantidad_max) VALUES ('02', 'ESMERIL', 30, '300.0', 5, 800);"
                    + "INSERT INTO producto (codigo, descripcion, existencia, costo_venta, cantidad_min, cantidad_max) VALUES ('03', 'TORNILLO', 1000, '0.96', 100, 1500);"
                    + "CREATE TABLE `proveedor` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`RIF` VARCHAR(50) NOT NULL DEFAULT '0',\n"
                    + "	`razon_social` VARCHAR(50) NOT NULL DEFAULT '0',\n"
                    + "	`telefono` VARCHAR(15) NULL);\n"
                    + "INSERT INTO `proveedor` (RIF, razon_social, telefono) VALUES ('001', 'RAZON SOCIAL 1', '00000000000');\n"
                    + "CREATE TABLE `personal` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`C.I.` INT(11) NOT NULL DEFAULT '0',\n"
                    + "	`nombre` VARCHAR(50) NOT NULL DEFAULT '0',\n"
                    + "	`cargo` INT(11) NOT NULL DEFAULT '0',\n"
                    + "	`clave` VARCHAR(50) NOT NULL);\n"
                    + "INSERT INTO `personal` (`C.I.`, nombre, cargo, clave) VALUES ('27863198', 'ADMINISTRADOR', 0, 'ADMIN');"
                    + "CREATE TABLE `cliente` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	CI VARCHAR(50) NOT NULL,\n"
                    + "	`nombre` VARCHAR(50) NOT NULL DEFAULT '',\n"
                    + "	`telefono` VARCHAR(15) NOT NULL DEFAULT '0',\n"
                    + "	`direccion` VARCHAR(50) NULL DEFAULT NULL);\n"
                    + "INSERT INTO `cliente` (CI, nombre, telefono, direccion) VALUES ('0', 'CLIENTE GENERAL', '00000000000', '');\n"
                    + "CREATE TABLE `compra` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`estatus` INT(1) DEFAULT 0,\n"
                    + "	`proveedor` INT(11) NOT NULL,\n"
                    + " `factura` VARCHAR(50) NOT NULL,\n"
                    + "	`personal` INT(11) NOT NULL,\n"
                    + "	`referencia` VARCHAR(11) NULL,\n"
                    + "	`fecha` DATETIME DEFAULT CURRENT_TIMESTAMP);\n"
                    + "CREATE TABLE `devolucion` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`estatus` INT(1) DEFAULT 0,\n"
                    + "	`cliente` INT(11) NOT NULL,\n"
                    + "	`personal` INT(11) NOT NULL,\n"
                    + "	`ID_venta` INT(11) NOT NULL,\n"
                    + "	`referencia` VARCHAR(11) NULL,\n"
                    + " `detalle` VARCHAR(20) NOT NULL,\n"
                    + "	`fecha` DATETIME DEFAULT CURRENT_TIMESTAMP);\n"
                    + "CREATE TABLE `inventario` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`estatus` INT(1) DEFAULT 0,\n"
                    + "	`referencia` VARCHAR(11) NULL,\n"
                    + "	`personal` INT(11) NOT NULL,\n"
                    + "	`detalle` VARCHAR(20) NOT NULL DEFAULT '',\n"
                    + "	`fecha` DATETIME DEFAULT CURRENT_TIMESTAMP);\n"
                    + "CREATE TABLE `venta` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`estatus` INT(1) DEFAULT 0,\n"
                    + "	`referencia` VARCHAR(11) NULL,\n"
                    + "	`personal` INT(11) NOT NULL,\n"
                    + "	`cliente` INT(11) NOT NULL,\n"
                    + "	`fecha` DATETIME DEFAULT CURRENT_TIMESTAMP,\n"
                    + "   `cierre` INT(11) DEFAULT 0);\n"
                    + "CREATE TABLE `cuerpo` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`estatus` INT(1) DEFAULT 0,\n"
                    + "   `tipo` INT(1) NOT NULL,\n"
                    + "	`ID_encabezado` INT(11) NOT NULL,\n"
                    + "	`referencia` VARCHAR(11) NULL,\n"
                    + "	`subtotal` VARCHAR(50) NOT NULL DEFAULT '0',\n"
                    + "	`porcent_IVA` VARCHAR(50) NOT NULL DEFAULT '0',\n"
                    + "	`IVA` VARCHAR(50) NOT NULL DEFAULT '0',\n"
                    + "	`total` VARCHAR(50) NOT NULL DEFAULT '0');\n"
                    + "CREATE TABLE `cuerpo_productos` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`ID_producto` INT(11) NOT NULL DEFAULT '0',\n"
                    + "	`ID_cuerpo` INT(11) NOT NULL DEFAULT '0',\n"
                    + "   `precio_unitario` VARCHAR(50) NOT NULL,\n"
                    + "	`cantidad` INT(11) NOT NULL DEFAULT '0',\n"
                    + "   `precio_total` VARCHAR(50) NOT NULL DEFAULT '0');"
                    + "CREATE TABLE `pago` (\n"
                    + "	`ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "	`ID_cuerpo` INT(11) NOT NULL,\n"
                    + "	`metodo_pago` VARCHAR(50) NOT NULL DEFAULT '',\n"
                    + "	`referencia` VARCHAR(50) NOT NULL DEFAULT '',\n"
                    + "	`monto` VARCHAR(50) NOT NULL DEFAULT '');\n"
                    + "CREATE TABLE `ajustes` (\n"
                    + "   `clave` VARCHAR(50) NOT NULL,\n"
                    + "   `valor` VARCHAR(50) NOT NULL);\n"
                    + "INSERT INTO ajustes (clave, valor) VALUES ('IVA', '16');\n"
                    + "INSERT INTO ajustes (clave, valor) VALUES ('AUMENTO_VENTA', '45');\n"
                    + "INSERT INTO ajustes (clave, valor) VALUES ('path_pdf', 'reportes');\n"
                    + "INSERT INTO ajustes (clave, valor) VALUES ('tasa', '27.95');\n"
                    + "CREATE TABLE `auditoria` (\n"
                    + "   `ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "   `descripcion` VARCHAR(50) NOT NULL DEFAULT '',\n"
                    + "   `fecha` DATETIME DEFAULT CURRENT_TIMESTAMP,\n"
                    + "   `ID_personal` INT(11) NOT NULL);"
                    + "CREATE TABLE `cierres`(\n"
                    + "   `ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "   `fecha` DATETIME DEFAULT CURRENT_TIMESTAMP,\n"
                    + "   `id_personal` INTEGER NOT NULL);\n"
                    + "CREATE TABLE `preguntas_seguridad`(\n"
                    + "   `ID` INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "   `pregunta` VARCHAR(250) NOT NULL);\n"
                    + "CREATE TABLE `respuestas_seguridad`("
                    + "   `pregunta` VARCHAR(250) NOT NULL,"
                    + "   `respuesta` VARCHAR(100) NOT NULL,"
                    + "   `id_personal` INT(11) NOT NULL);"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Primer nombre de su madre?');\n"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Ciudad de Nacimiento?');\n"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Fecha de nacimiento de su padre?');\n"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Lugar que le gustaria visitar?');\n"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Comida favorita?');\n"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Segundo nombre de su hermano/a?');\n"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Materia favorita del bachillerato?');\n"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Nombre de su segunda mascota?');\n"
                    + "INSERT INTO preguntas_seguridad (pregunta) VALUES ('¿Ciudad de nacimiento de su abuela?');\n";

            System.out.println(sql);
            stmt.executeUpdate(sql);
            con.commit();
            stmt.close();
        } catch (SQLException ex) {
            System.out.println(ex);
            return false;
        }
        return true;
    }
}

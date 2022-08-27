package core;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.sql.*;
import java.text.DecimalFormat;
import java.util.ArrayList;

/**
 * CLASS TO MAKE A BRIGE BETWEEN DATA BASE AND PYTHON SYSTEM
 * @author Alba
 */
public final class DATA_CLASS {
    
    private final DATA_BASE DB = new DATA_BASE();
    
    public static void main(String[] args){
        DATA_CLASS a = new DATA_CLASS();
    }
    
    public DATA_CLASS(){
        //MOVIMIENTO(1, 1, 1, "1000.00");
    }
    
    public String SELECT_AJUSTE(String clave){
        try {
            try (Statement stmt = DB.con.createStatement()){
                String query = "SELECT valor FROM ajustes WHERE clave = '"+clave+"';";
                ResultSet rs = stmt.executeQuery(query);
                
                return rs.getString("valor");
            }
        } catch (SQLException e) {
            System.out.println("ERROR SELECT_AJUSTE: "+e);
            return null;
        }
    }
    
    
    public boolean UPDATE_AJUSTE(String clave, String valor){
        try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "UPDATE ajustes SET valor = '"+valor+"' WHERE clave = '"+clave+"'";
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            return true;
        }catch(SQLException e){
            System.out.println("ERROR UPATE_AJUSTE: "+e);
            return false;
        }
    }
    
    public boolean UPDATE_USER_ADMIN(String CI, String clave){
        try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "UPDATE personal SET `C.I.` = "+CI+" AND clave = '"+clave+"' WHERE cargo = 0;";
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            return true;
        }catch(SQLException e){
            System.out.println("ERROR UPDATE_USER_ADMIN: "+e);
            return false;
        }
    }
    
    public boolean INSERT_USER(String ci, String nombre, int cargo, String clave){
        try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "INSERT INTO personal (`C.I.`, nombre, cargo, clave) VALUES ("+ci+", '"+nombre+"', "+cargo+", '"+clave+"');";
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            return true;
        }catch(SQLException e){
            System.out.println("ERROR INSERT_USER: "+e);
            return false;
        }
    }

    public String[] SELECT_USER(String ci, String clave){
        try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "SELECT * FROM personal WHERE `C.I.` = "+ci+" AND clave = '"+clave+"'";
                ResultSet rs = stmt.executeQuery(query);
                
                String[] data = new String[4];
                data[0] = rs.getString("ID");
                data[1] = rs.getString("C.I.");
                data[2] = rs.getString("nombre");
                data[3] = rs.getString("cargo");
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR SELECT_USER: "+e);
            return null;
        }
    }
    
    public String[] SELECT_USER_BY_ID(String id){
                try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "SELECT * FROM personal WHERE ID = "+id;
                ResultSet rs = stmt.executeQuery(query);
                
                String[] data = new String[4];
                data[0] = rs.getString("ID");
                data[1] = rs.getString("C.I.");
                data[2] = rs.getString("nombre");
                data[3] = rs.getString("cargo");
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR SELECT_USER: "+e);
            return null;
        }
    }
    
    public String[] SELECT_USER(String ci){
                try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "SELECT * FROM personal WHERE `C.I.` = "+ci;
                ResultSet rs = stmt.executeQuery(query);
                
                String[] data = new String[4];
                data[0] = rs.getString("ID");
                data[1] = rs.getString("C.I.");
                data[2] = rs.getString("nombre");
                data[3] = rs.getString("cargo");
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR SELECT_USER: "+e);
            return null;
        }
    }

    public ArrayList<String[]> SELECT_ALL_USER(){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String query = "SELECT * FROM personal;";
                ResultSet rs = stmt.executeQuery(query);
                
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[4];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("C.I.");
                    data[2] = rs.getString("nombre");
                    data[3] = rs.getString("cargo");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_ALL_PRODUCTO: "+e);
            return null;
        }
    }

    public boolean INSERT_PROVEEDOR(String rif, String razon_social, String telefono){
        try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "INSERT INTO proveedor (RIF, razon_social, telefono) VALUES ('"+rif+"', '"+razon_social+"', '"+telefono+"')";
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            return true;
        }catch(SQLException e){
            System.out.println("ERROR INSERT_PROVEEDOR: "+e);
            return false;
        }
    }
    
    public String[] SELECT_PROVEEDOR_BY_ID(String id){
        try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "SELECT * FROM proveedor WHERE ID = "+id+";";
                ResultSet rs = stmt.executeQuery(query);
                
                String[] data = new String[4];
                data[0] = rs.getString("ID");
                data[1] = rs.getString("RIF");
                data[2] = rs.getString("razon_social");
                data[3] = rs.getString("telefono");
                return data;
            }
        } catch(SQLException e){
            System.out.println("ERROR SELECT_PROVEEDOR: "+e);
            return null;
        }
    }
    
    public String[] SELECT_PROVEEDOR(String rif){
        try{
            try (Statement stmt = DB.con.createStatement()){
                String query = "SELECT * FROM proveedor WHERE `RIF` = '"+rif+"';";
                ResultSet rs = stmt.executeQuery(query);
                
                String[] data = new String[4];
                data[0] = rs.getString("ID");
                data[1] = rs.getString("RIF");
                data[2] = rs.getString("razon_social");
                data[3] = rs.getString("telefono");
                return data;
            }
        } catch(SQLException e){
            System.out.println("ERROR SELECT_PROVEEDOR: "+e);
            return null;
        }
    }

    public boolean INSERT_PRODUCTO(String codigo, String descripcion, String cantidad_alerta){
        try{
            try (Statement stmt = DB.con.createStatement()) {
                String query = "INSERT INTO producto (codigo, descripcion, cantidad_alerta) VALUES ('"+codigo+"', '"+descripcion+"', "+cantidad_alerta+")";
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            return true;
        }catch(SQLException e){
            System.out.println("ERROR IN INSERT_PRODUCTO: "+e);
            return false;
        }
    }
    
    public boolean UPDATE_PRODUCTO(String codigo, String column, String value){
        try{
            try (Statement stmt = DB.con.createStatement()) {
                String query = "UPDATE producto SET "+column+" = '"+value+"' WHERE ID = "+codigo+";";
                System.out.println(query);
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            return true;
        }catch(SQLException e){
            System.out.println("ERROR IN UPDATE_PRODUCTO: "+e);
            return false;
        }
    }
    
    public ArrayList<String[]> SELECT_ALL_PRODUCTO(){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String query = "SELECT * FROM producto;";
                ResultSet rs = stmt.executeQuery(query);
                
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[6];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("codigo");
                    data[2] = rs.getString("descripcion");
                    data[3] = rs.getString("existencia");
                    data[4] = rs.getString("costo_venta");
                    data[5] = rs.getString("cantidad_alerta");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_ALL_PRODUCTO: "+e);
            return null;
        }
    }
    
    public String[] SELECT_PRODUCTO_BY_ID(String id){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String[] data = new String[6];
                
                String query = "SELECT * FROM producto WHERE ID = "+id+"";
                ResultSet rs = stmt.executeQuery(query);
                
                data[0] = rs.getString("ID");
                data[1] = rs.getString("codigo");
                data[2] = rs.getString("descripcion");
                data[3] = rs.getString("existencia");
                data[4] = rs.getString("costo_venta");
                data[5] = rs.getString("cantidad_alerta");
                
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_PRODUCTO: "+e);
            return null;
        }
    }
    
    public String[] SELECT_PRODUCTO(String codigo){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String[] data = new String[6];
                
                String query = "SELECT * FROM producto WHERE codigo = '"+codigo+"'";
                ResultSet rs = stmt.executeQuery(query);
                
                data[0] = rs.getString("ID");
                data[1] = rs.getString("codigo");
                data[2] = rs.getString("descripcion");
                data[3] = rs.getString("existencia");
                data[4] = rs.getString("costo_venta");
                data[5] = rs.getString("cantidad_alerta");
                
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_PRODUCTO: "+e);
            return null;
        }
    }
    
    public String[] SELECT_CLIENTE_BY_ID(String id){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String[] data = new String[5];
                
                String query = "SELECT * FROM cliente WHERE ID = "+id+";";
                ResultSet rs = stmt.executeQuery(query);
                
                data[0] = rs.getString("ID");
                data[1] = rs.getString("CI");
                data[2] = rs.getString("nombre");
                data[3] = rs.getString("telefono");
                data[4] = rs.getString("direccion");
                
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_CLIENTE: "+e);
            return null;
        }
    }
    
    public String[] SELECT_CLIENTE(String ci){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String[] data = new String[5];
                
                String query = "SELECT * FROM cliente WHERE CI = '"+ci+"';";
                ResultSet rs = stmt.executeQuery(query);
                
                data[0] = rs.getString("ID");
                data[1] = rs.getString("CI");
                data[2] = rs.getString("nombre");
                data[3] = rs.getString("telefono");
                data[4] = rs.getString("direccion");
                
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_CLIENTE: "+e);
            return null;
        }
    }
    
    public boolean INSERT_CLIENTE(String ci, String nombre, String telefono, String direccion){
        try{
            try (Statement stmt = DB.con.createStatement()) {
                String query = "INSERT INTO cliente (CI, nombre, telefono, direccion) "
                        + "VALUES ('"+ci+"', '"+nombre+"', '"+telefono+"', '"+direccion+"')";
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            return true;
        }catch(SQLException e){
            System.out.println("ERROR IN INSERT_CLIENTE: "+e);
            return false;
        }
    }
    
    public ArrayList<String[]> SELECT_ALL_MOVIMIENTOS(){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String query = "SELECT * FROM cuerpo;";
                ResultSet rs = stmt.executeQuery(query);
                
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[9];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("estatus");
                    data[2] = rs.getString("tipo");
                    data[3] = rs.getString("ID_encabezado");
                    data[4] = rs.getString("referencia");
                    data[5] = rs.getString("subtotal");
                    data[6] = rs.getString("porcent_IVA");
                    data[7] = rs.getString("IVA");
                    data[8] = rs.getString("total");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_ALL_MOVIMIENTOS: "+e);
            return null;
        }
    }
    
    public String[] SELECT_FACTURA_VENTA(String id){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String[] data = new String[7];
                
                String query = "SELECT * FROM venta WHERE ID = "+id+";";
                ResultSet rs = stmt.executeQuery(query);
                
                data[0] = rs.getString("ID");
                data[1] = rs.getString("estatus");
                data[2] = rs.getString("referencia");
                data[3] = rs.getString("personal");
                data[4] = rs.getString("cliente");
                data[5] = rs.getString("fecha");
                data[6] = rs.getString("cierre");
                
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_FACTURA: "+e);
            return null;
        }
    }
    
    public String[] SELECT_CABECERA(String tipo,String ref){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String[] data = new String[11];
                
                String query = "SELECT * FROM "+tipo+" WHERE referencia = '"+ref+"';";
                ResultSet rs = stmt.executeQuery(query);
                
                data[0] = rs.getString("ID");
                data[1] = rs.getString("estatus");
                data[2] = rs.getString("referencia");
                data[3] = rs.getString("personal");
                data[4] = rs.getString("fecha");
                try{
                    data[5] = rs.getString("cierre");
                }catch(Exception e){}
                
                try{
                    data[6] = rs.getString("detalle");
                }catch(Exception e){}
                
                try{
                    data[7] = rs.getString("ID_venta");
                }catch(Exception e){}
                
                try{
                    data[8] = rs.getString("proveedor");
                }catch(Exception e){}
                
                try{
                    data[9] = rs.getString("cliente");
                }catch(Exception e){}
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_FACTURA: "+e);
            return null;
        }
    }
    
    public String[] SELECT_MOVIMIENTO(String ref){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String[] data = new String[9];
                
                String query = "SELECT * FROM cuerpo WHERE ID = "+ref;
                ResultSet rs = stmt.executeQuery(query);
                
                data[0] = rs.getString("ID");
                data[1] = rs.getString("estatus");
                data[2] = rs.getString("tipo");
                data[3] = rs.getString("ID_encabezado");
                data[4] = rs.getString("referencia");
                data[5] = rs.getString("subtotal");
                data[6] = rs.getString("porcent_IVA");
                data[7] = rs.getString("IVA");
                data[8] = rs.getString("total");
                
                return data;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_FACTURA: "+e);
            return null;
        }
    }
    
    public ArrayList<String[]> SELECT_CUERPO_PRODUCTOS(String id_cuerpo){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String query = "SELECT * FROM cuerpo_productos WHERE ID_cuerpo = "+id_cuerpo;
                ResultSet rs = stmt.executeQuery(query);
                
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[6];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("ID_producto");
                    data[2] = rs.getString("ID_cuerpo");
                    data[3] = rs.getString("precio_unitario");
                    data[4] = rs.getString("cantidad");
                    data[5] = rs.getString("precio_total");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_FACTURA: "+e);
            return null;
        }
    }
    
    public String MOVIMIENTO(int tipo, String entidad, String personal, String TOTAL_STR, int[] productos, int[] cantidades, float[] precios, int[] metodo_pago, int[] ref, float[] monto){
        String referencia = MOVIMIENTO(tipo, entidad, personal, TOTAL_STR, productos, cantidades, precios);
        if (!"false".equals(referencia)){
            try{
                Statement stmt = DB.con.createStatement();
                ResultSet rs = null;
                String query = "";
                
                query = "SELECT * FROM cuerpo WHERE ID = (SELECT MAX(ID) FROM cuerpo)";
                rs = stmt.executeQuery(query);
                int id_cuerpo = rs.getInt("ID");
            
                for(int i = 0; i < metodo_pago.length; i++){
                    query = "INSERT INTO pago (ID_cuerpo, metodo_pago, referencia, monto)"
                            + "VALUES ("+id_cuerpo+", '"+format_type_meth(metodo_pago[i])+"', '"+ref[i]+"', '"+monto[i]+"');";
                    stmt.executeUpdate(query);
                    DB.con.commit();
                }
                return referencia;
            }catch(SQLException e){
                System.out.println("ERROR IN MOVIMIENTO_PAGO: "+e);
                return "false";
            }
        } else {
            return "false";
        }
    }
    
    public ArrayList<String[]> SELECT_VENTA_CIERRE(){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String query = "SELECT * FROM venta WHERE estatus = 0 AND cierre = 0";
                ResultSet rs = stmt.executeQuery(query);
                
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[7];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("estatus");
                    data[2] = rs.getString("referencia");
                    data[3] = rs.getString("personal");
                    data[4] = rs.getString("cliente");
                    data[5] = rs.getString("fecha");
                    data[6] = rs.getString("cierre");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_VENTA_CIERRE: "+e);
            return null;
        }
    }
    
    public int UPDATE_VENTA_CIERRE(String id_personal){
        try{
            int id_cierre = 0;
            try (Statement stmt = DB.con.createStatement()) {
                String query = "INSERT INTO cierres (id_personal) VALUES ("+id_personal+")";
                stmt.executeUpdate(query);
                DB.con.commit();
                
                query = "SELECT * FROM cierres WHERE ID = (SELECT MAX(ID) FROM cierres);";
                ResultSet rs = stmt.executeQuery(query);
                id_cierre = rs.getInt("ID");
                
                query = "UPDATE venta SET cierre = "+id_cierre+" WHERE estatus = 0 AND cierre = 0";
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            return id_cierre;
        }catch(SQLException e){
            System.out.println("ERROR IN UPDATE_PRODUCTO: "+e);
            return 0;
        }
    }
    
    public ArrayList<String[]> SELECT_FACTURA(String num_factura){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                String query = "SELECT \n" +
                               "       AA.referencia,\n" +
                               "       AA.fecha,\n" +
                               "       CC.CI,\n" +
                               "       CC.nombre,\n" +
                               "       CC.direccion,\n" +
                               "       EE.descripcion,\n" +
                               "       DD.precio_unitario,\n" +
                               "       DD.cantidad,\n" +
                               "       DD.precio_total as precio_producto,\n" +
                               "       BB.porcent_IVA,\n" +
                               "       BB.IVA,\n" +
                               "       BB.subtotal,\n" +
                               "       BB.total\n" +
                               "FROM venta AS AA\n" +
                               "INNER JOIN cuerpo AS BB ON BB.ID_encabezado = AA.ID\n" +
                               "INNER JOIN cliente AS CC ON AA.cliente = CC.ID\n" +
                               "INNER JOIN cuerpo_productos AS DD ON DD.ID_cuerpo = BB.ID\n" +
                               "INNER JOIN producto AS EE ON DD.ID_producto = EE.ID\n" +
                               "WHERE AA.referencia = '"+num_factura+"';";
                ResultSet rs = stmt.executeQuery(query);
                
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[13];
                    data[0] = rs.getString("referencia");
                    data[1] = rs.getString("fecha");
                    data[2] = rs.getString("CI");
                    data[3] = rs.getString("nombre");
                    data[4] = rs.getString("direccion");
                    data[5] = rs.getString("descripcion");
                    data[6] = rs.getString("precio_unitario");
                    data[7] = rs.getString("cantidad");
                    data[8] = rs.getString("precio_producto");
                    data[9] = rs.getString("porcent_IVA");
                    data[10] = rs.getString("IVA");
                    data[11] = rs.getString("subtotal");
                    data[12] = rs.getString("total");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN SELECT_VENTA_CIERRE: "+e);
            return null;
        }
    }
    
    public String MOVIMIENTO(int tipo, String entidad, String personal, String TOTAL_STR, int[] productos, int[] cantidades, float[] precios){
        try{
            Statement stmt = DB.con.createStatement();
            ResultSet rs = null;
            String query = "";
            String referencia = "";
            String id_entidad = "";
            int id_movimiento = 0;
            String descripcion_auditoria = "";
            
            switch(tipo){
                // VENTA
                case 1:
                    query = "SELECT ID FROM cliente WHERE CI = '"+entidad+"';";
                    rs = stmt.executeQuery(query);
                    id_entidad = rs.getString("ID");
                    
                    query = "INSERT INTO venta (personal, cliente) VALUES ("+personal+", "+id_entidad+");";
                    stmt.executeUpdate(query);
                    DB.con.commit();
                    
                    query = "SELECT * FROM venta WHERE ID = (SELECT MAX(ID) FROM venta);";
                    rs = stmt.executeQuery(query);
                    id_movimiento = rs.getInt("ID");
                    
                    descripcion_auditoria = "VENTA DE PRODUCTOS";
                    break;
                
                // COMPRA
                case 2:
                    query = "SELECT ID FROM proveedor WHERE RIF = '"+entidad+"';";
                    rs = stmt.executeQuery(query);
                    id_entidad = rs.getString("ID");
                                        
                    query = "INSERT INTO compra (proveedor, personal) VALUES ("+id_entidad+", "+personal+");";
                    stmt.executeUpdate(query);
                    DB.con.commit();
                    
                    query = "SELECT * FROM compra WHERE ID = (SELECT MAX(ID) FROM compra);";
                    rs = stmt.executeQuery(query);
                    id_movimiento = rs.getInt("ID");
                    
                    descripcion_auditoria = "COMPRA DE PRODUCTOS";
                    break;
                // DEVOLUCION
                case 3:
                    query = "SELECT * FROM venta WHERE ID = "+entidad;
                    rs = stmt.executeQuery(query);
                    String id_cliente = rs.getString("cliente");
                    id_entidad = rs.getString("ID");
                    
                    query = "INSERT INTO devolucion (cliente, personal, ID_venta) VALUES ("+id_cliente+", "+personal+", "+id_entidad+")";
                    stmt.executeUpdate(query);
                    DB.con.commit();
                    
                    query = "SELECT * FROM devolucion WHERE ID = (SELECT MAX(ID) FROM devolucion);";
                    rs = stmt.executeQuery(query);
                    id_movimiento = rs.getInt("ID");
                    
                    descripcion_auditoria = "DEVOLUCIÓN DE PRODUCTOS";
                    break;
                // AJUSTES DE INVENTARIO ++
                case 4:
                case 5:
                    query = "INSERT INTO inventario (personal, detalle) VALUES ("+personal+", '"+entidad+"')";
                    stmt.executeUpdate(query);
                    DB.con.commit();
                    
                    query = "SELECT * FROM inventario WHERE ID = (SELECT MAX(ID) FROM inventario);";
                    rs = stmt.executeQuery(query);
                    id_movimiento = rs.getInt("ID");
                    
                    String conf = "";
                    if (tipo == 5){
                        conf = "(+)";
                    }else {
                        conf = "(-)";
                    }
                    descripcion_auditoria = "AJUSTES DE INVENTARIO"+conf;
                    break;
            }
            
            query = "SELECT * FROM ajustes WHERE clave = 'IVA'";
            rs = stmt.executeQuery(query);
            String iva_str = rs.getString("valor");
                        
            BigDecimal TOTAL     = new BigDecimal(TOTAL_STR);
            BigDecimal SUBTOTAL = TOTAL.divide(new BigDecimal(iva_str).multiply(new BigDecimal("0.01")).add(new BigDecimal("1.0")), 2, RoundingMode.HALF_DOWN);
            BigDecimal TOTAL_IVA  = TOTAL.subtract(SUBTOTAL);
                        
            query = "INSERT INTO cuerpo (ID_encabezado, tipo, subtotal, porcent_IVA, IVA, total) "
                    + "VALUES ("+id_movimiento+", "+tipo+", '"+format_decimal(SUBTOTAL)+"', '"+iva_str+"', '"+format_decimal(TOTAL_IVA)+"', '"+format_decimal(TOTAL)+"');";
            stmt.executeUpdate(query);
            DB.con.commit();
                                    
            query = "SELECT * FROM cuerpo WHERE ID = (SELECT MAX(ID) FROM cuerpo)";
            rs = stmt.executeQuery(query);
            int id_cuerpo = rs.getInt("ID");
            referencia = String.format("%011d", id_cuerpo);
            
            query = "UPDATE "+format_type_mov(tipo)+" SET referencia = '"+referencia+"' WHERE ID = "+id_movimiento+";";
            stmt.executeUpdate(query);
            DB.con.commit();
            
            query = "UPDATE cuerpo SET referencia = '"+referencia+"' WHERE ID = "+id_cuerpo+";";
            stmt.executeUpdate(query);
            DB.con.commit();
            
            if(productos != null){
                for (int i = 0; i < productos.length; i++){
                    BigDecimal precio       = new BigDecimal(precios[i]);
                    BigDecimal cantidad     = new BigDecimal(cantidades[i]);
                    BigDecimal total_cuerpo = precio.multiply(cantidad);
                    query = "INSERT INTO cuerpo_productos (ID_producto, ID_cuerpo, precio_unitario, cantidad, precio_total)"
                            + " VALUES ("+productos[i]+", "+id_cuerpo+", '"+format_decimal(precio)+"', "+format_decimal(cantidad)+", '"+format_decimal(total_cuerpo)+"')";
                    stmt.executeUpdate(query);
                    DB.con.commit();
                    
                    query = "SELECT existencia FROM producto WHERE ID = "+productos[i]+";";
                    rs = stmt.executeQuery(query);
                    int existencia_anterior  = rs.getInt("existencia");
                    int existencia_actual = 0;
                    switch(tipo){
                        case 1: 
                        case 4:
                            existencia_actual = existencia_anterior - cantidades[i]; break;
                        case 2: 
                        case 3:
                        case 5:
                            existencia_actual = existencia_anterior + cantidades[i]; break;
                    }
                    
                    query = "UPDATE producto SET existencia = "+existencia_actual+" WHERE ID = "+productos[i]+";";
                    stmt.executeUpdate(query);
                    DB.con.commit();
                }
            }
            
            if (tipo == 3){
                query = "UPDATE venta SET estatus = 1 WHERE ID = "+id_entidad;
                stmt.executeUpdate(query);
                DB.con.commit();
                
                query = "UPDATE cuerpo SET estatus = 1 WHERE referencia = "+referencia;
                stmt.executeUpdate(query);
                DB.con.commit();
            }
            
            INSERT_AUDITORIA(descripcion_auditoria, "(REF: "+referencia+")", personal);
            return referencia;
        }catch(SQLException e){
            System.out.println("ERROR IN MOVIMIENTO: "+e);
            return "false";
        }
    }
    
    public ArrayList<String[]> LIKE_SENTENCE_PRODUCTO(String query){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                ResultSet rs = stmt.executeQuery(query);     
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[6];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("codigo");
                    data[2] = rs.getString("descripcion");
                    data[3] = rs.getString("existencia");
                    data[4] = rs.getString("costo_venta");
                    data[5] = rs.getString("cantidad_alerta");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN LIKE_SENTENCE: "+e);
            return null;
        }
    }
    
    public ArrayList<String[]> LIKE_SENTENCE_MOVIMIENTOS(String query){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                ResultSet rs = stmt.executeQuery(query);     
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[9];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("estatus");
                    data[2] = rs.getString("tipo");
                    data[3] = rs.getString("ID_encabezado");
                    data[4] = rs.getString("referencia");
                    data[5] = rs.getString("subtotal");
                    data[6] = rs.getString("porcent_IVA");
                    data[7] = rs.getString("IVA");
                    data[8] = rs.getString("total");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN LIKE_SENTENCE: "+e);
            return null;
        }
    }
    
    public ArrayList<String[]> LIKE_SENTENCE_USER(String query){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                ResultSet rs = stmt.executeQuery(query);     
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[4];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("C.I.");
                    data[2] = rs.getString("nombre");
                    data[3] = rs.getString("cargo");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN LIKE_SENTENCE: "+e);
            return null;
        }
    }
    
    public ArrayList<String[]> LIKE_SENTENCE_AUDITORIA(String query){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                ResultSet rs = stmt.executeQuery(query);     
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[4];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("descripcion");
                    data[2] = rs.getString("fecha");
                    data[3] = rs.getString("cargo");
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN LIKE_SENTENCE: "+e);
            return null;
        }
    }
    
    private void INSERT_AUDITORIA(String descripcion, String ref, String id_usuario){
        try{
            try (Statement stmt = DB.con.createStatement()) {
                String query = "INSERT INTO auditoria (descripcion, ID_personal) "
                        + "VALUES ('"+descripcion+" "+ref+"', "+id_usuario+")";
                stmt.executeUpdate(query);
                DB.con.commit();
            }
        }catch(SQLException e){
            System.out.println("ERROR IN INSERT_AUDITORIA: "+e);
        }
    }
    
    public ArrayList<String[]> SELECT_AUDITORIA(){
        try{
            try (Statement stmt = DB.con.createStatement()){
                
                ResultSet rs = stmt.executeQuery("SELECT * FROM auditoria");
                ArrayList<String[]> data_raw = new ArrayList<>();
                
                while(rs.next()){
                    String[] data = new String[9];
                    data[0] = rs.getString("ID");
                    data[1] = rs.getString("descripcion");
                    data[2] = rs.getString("fecha");
                    data[3] = rs.getString("id_personal");
                    
                    data_raw.add(data);
                }
                return data_raw;
            }
        }catch(SQLException e){
            System.out.println("ERROR IN LIKE_SENTENCE: "+e);
            return null;
        }
    }
    
//-----------------------------------------------------------------------------------------------------------------------------//
    
    public String format_decimal(BigDecimal n){
        n = n.setScale(2, BigDecimal.ROUND_DOWN);
        DecimalFormat df = new DecimalFormat();
        df.setMaximumFractionDigits(2);
        df.setGroupingUsed(false);
        return df.format(n);
    }
    
    public String format_type_mov(int mov){
        String mov_str = "venta";
        switch(mov){
            case 1: mov_str = "venta"; break;
            case 2: mov_str = "compra"; break;
            case 3: mov_str = "devolucion"; break;
            case 4: mov_str = "inventario"; break;
            case 5: mov_str = "inventario"; break;
        }
        return mov_str;
    }
    
        public int format_type_mov(String mov){
        int mov_int = 1;
        switch(mov){
            case "venta": mov_int = 1; break;
            case "compra": mov_int = 2; break;
            case "devolucion": mov_int = 3; break;
            case "ajustes_in": mov_int = 4; break;
            case "ajustes_out": mov_int = 5; break;
        }
        return mov_int;
    }

    
    public int format_type_meth(String metodo){
        switch(metodo){
            case "EFECTIVO": return 1;
            case "DEBITO": return 2;
            case "CREDITO": return 3;
            default: return 1;
        }
    }
    
    public String format_type_meth(int metodo){
        switch(metodo){
            case 1: return "EFECTIVO";
            case 2: return "DEBITO";
            case 3: return "CREDITO";
            default: return "EFECTIVO";
        }
    }
    
    public String substract(String a, String b){
        return new BigDecimal(a).subtract(new BigDecimal(b)).toString();
    }
}

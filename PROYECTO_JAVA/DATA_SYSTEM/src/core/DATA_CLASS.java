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
            }
            
            query = "SELECT * FROM ajustes WHERE clave = 'IVA'";
            rs = stmt.executeQuery(query);
            String iva_str = rs.getString("valor");
                        
            BigDecimal TOTAL     = new BigDecimal(TOTAL_STR);
            BigDecimal TOTAL_IVA = TOTAL.divide(new BigDecimal(iva_str).multiply(new BigDecimal("0.01")).add(new BigDecimal("1.0")), 2, RoundingMode.HALF_DOWN);
            BigDecimal SUBTOTAL  = TOTAL.subtract(TOTAL_IVA);
                        
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
            
            INSERT_AUDITORIA(descripcion_auditoria, "REF: "+referencia, personal);
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
            case 4: mov_str = "ajustes"; break;
            case 5: mov_str = "ajustes"; break;
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

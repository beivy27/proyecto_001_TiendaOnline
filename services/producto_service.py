from conexion.conexion import obtener_conexion

def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos

def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto

def insertar_producto(nombre, precio, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
        (nombre, precio, stock)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar_producto(id_producto, nombre, precio, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s",
        (nombre, precio, stock, id_producto)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_reporte_facturas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            f.id_factura,
            c.nombre AS cliente,
            u.nombre AS usuario,
            p.nombre AS producto,
            d.cantidad,
            d.precio_unitario,
            d.subtotal,
            f.total
        FROM facturas f
        INNER JOIN clientes c ON f.id_cliente = c.id_cliente
        INNER JOIN usuarios u ON f.id_usuario = u.id_usuario
        INNER JOIN detalle_factura d ON f.id_factura = d.id_factura
        INNER JOIN productos p ON d.id_producto = p.id_producto
        ORDER BY f.id_factura
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos
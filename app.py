from flask import Flask, render_template, request, redirect, url_for
from conexion.conexion import conectar

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test_db')
def test_db():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SHOW TABLES;")
        tablas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return f"Conexión exitosa. Tablas: {tablas}"
    except Exception as e:
        return f"Error de conexión: {e}"


# =========================
# USUARIOS
# =========================

@app.route('/usuarios_mysql')
def usuarios_mysql():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios;")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('usuarios_mysql.html', usuarios=usuarios)
    except Exception as e:
        return f"Error al consultar usuarios: {e}"


@app.route('/agregar_usuario_mysql', methods=['GET', 'POST'])
def agregar_usuario_mysql():
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        password = request.form['password']

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)"
            valores = (nombre, mail, password)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('usuarios_mysql'))
        except Exception as e:
            return f"Error al insertar usuario: {e}"

    return render_template('agregar_usuario_mysql.html')


@app.route('/editar_usuario_mysql/<int:id_usuario>', methods=['GET', 'POST'])
def editar_usuario_mysql(id_usuario):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        if request.method == 'POST':
            nombre = request.form['nombre']
            mail = request.form['mail']
            password = request.form['password']

            sql = "UPDATE usuarios SET nombre=%s, mail=%s, password=%s WHERE id_usuario=%s"
            valores = (nombre, mail, password, id_usuario)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('usuarios_mysql'))

        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()

        return render_template('editar_usuario_mysql.html', usuario=usuario)

    except Exception as e:
        return f"Error al editar usuario: {e}"


@app.route('/eliminar_usuario_mysql/<int:id_usuario>')
def eliminar_usuario_mysql(id_usuario):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('usuarios_mysql'))
    except Exception as e:
        return f"Error al eliminar usuario: {e}"


# =========================
# PRODUCTOS
# =========================

@app.route('/productos_mysql')
def productos_mysql():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos;")
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('productos_mysql.html', productos=productos)
    except Exception as e:
        return f"Error al consultar productos: {e}"


@app.route('/agregar_producto_mysql', methods=['GET', 'POST'])
def agregar_producto_mysql():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = """
                INSERT INTO productos (nombre, descripcion, precio, stock)
                VALUES (%s, %s, %s, %s)
            """
            valores = (nombre, descripcion, precio, stock)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('productos_mysql'))
        except Exception as e:
            return f"Error al insertar producto: {e}"

    return render_template('agregar_producto_mysql.html')


@app.route('/editar_producto_mysql/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto_mysql(id_producto):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio = request.form['precio']
            stock = request.form['stock']

            sql = """
                UPDATE productos
                SET nombre=%s, descripcion=%s, precio=%s, stock=%s
                WHERE id_producto=%s
            """
            valores = (nombre, descripcion, precio, stock, id_producto)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('productos_mysql'))

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        conexion.close()

        return render_template('editar_producto_mysql.html', producto=producto)

    except Exception as e:
        return f"Error al editar producto: {e}"


@app.route('/eliminar_producto_mysql/<int:id_producto>')
def eliminar_producto_mysql(id_producto):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('productos_mysql'))
    except Exception as e:
        return f"Error al eliminar producto: {e}"


# =========================
# CLIENTES
# =========================

@app.route('/clientes_mysql')
def clientes_mysql():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes;")
        clientes = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('clientes_mysql.html', clientes=clientes)
    except Exception as e:
        return f"Error al consultar clientes: {e}"


@app.route('/agregar_cliente_mysql', methods=['GET', 'POST'])
def agregar_cliente_mysql():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            sql = """
                INSERT INTO clientes (nombre, apellido, correo, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nombre, apellido, correo, telefono, direccion)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('clientes_mysql'))
        except Exception as e:
            return f"Error al insertar cliente: {e}"

    return render_template('agregar_cliente_mysql.html')


@app.route('/editar_cliente_mysql/<int:id_cliente>', methods=['GET', 'POST'])
def editar_cliente_mysql(id_cliente):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            correo = request.form['correo']
            telefono = request.form['telefono']
            direccion = request.form['direccion']

            sql = """
                UPDATE clientes
                SET nombre=%s, apellido=%s, correo=%s, telefono=%s, direccion=%s
                WHERE id_cliente=%s
            """
            valores = (nombre, apellido, correo, telefono, direccion, id_cliente)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('clientes_mysql'))

        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        conexion.close()

        return render_template('editar_cliente_mysql.html', cliente=cliente)

    except Exception as e:
        return f"Error al editar cliente: {e}"


@app.route('/eliminar_cliente_mysql/<int:id_cliente>')
def eliminar_cliente_mysql(id_cliente):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('clientes_mysql'))
    except Exception as e:
        return f"Error al eliminar cliente: {e}"


if __name__ == '__main__':
    app.run(debug=True)
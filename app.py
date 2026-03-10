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


if __name__ == '__main__':
    app.run(debug=True)
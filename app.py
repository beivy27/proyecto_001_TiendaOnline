from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "tienda.db"


# =========================
# CONEXIÓN A BASE DE DATOS
# =========================
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# INICIO + BÚSQUEDA
# =========================
@app.route('/')
def index():
    conn = get_db_connection()
    busqueda = request.args.get('busqueda')

    if busqueda:
        productos = conn.execute(
            "SELECT * FROM productos WHERE nombre LIKE ?",
            ('%' + busqueda + '%',)
        ).fetchall()
    else:
        productos = conn.execute(
            "SELECT * FROM productos"
        ).fetchall()

    conn.close()
    return render_template('index.html', productos=productos)


# =========================
# CREAR PRODUCTO
# =========================
@app.route('/producto/nuevo', methods=['GET', 'POST'])
def producto_nuevo():

    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        # VALIDACIÓN BACKEND
        if not nombre.strip():
            return "El nombre no puede estar vacío", 400

        if int(cantidad) < 0:
            return "La cantidad no puede ser negativa", 400

        if float(precio) < 0:
            return "El precio no puede ser negativo", 400

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
            (nombre, cantidad, precio)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('producto_form.html', producto=None)


# =========================
# EDITAR PRODUCTO
# =========================
@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):

    conn = get_db_connection()
    producto = conn.execute(
        "SELECT * FROM productos WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        # VALIDACIÓN BACKEND
        if not nombre.strip():
            return "El nombre no puede estar vacío", 400

        if int(cantidad) < 0:
            return "La cantidad no puede ser negativa", 400

        if float(precio) < 0:
            return "El precio no puede ser negativo", 400

        conn.execute(
            "UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?",
            (nombre, cantidad, precio, id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn.close()
    return render_template('producto_form.html', producto=producto)


# =========================
# ELIMINAR PRODUCTO
# =========================
@app.route('/producto/eliminar/<int:id>', methods=['POST'])
def producto_eliminar(id):

    conn = get_db_connection()
    conn.execute(
        "DELETE FROM productos WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


# =========================
# EJECUCIÓN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
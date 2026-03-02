import os
import json
import csv

from flask import Flask, render_template, request, redirect, url_for
from inventario.db import db
from inventario.productos import Producto

app = Flask(__name__)

# -------------------------
# CONFIGURACIÓN SQLITE
# -------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "inventario.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave123"

db.init_app(app)

with app.app_context():
    db.create_all()

# -------------------------
# RUTA PRINCIPAL
# -------------------------
@app.route("/")
def index():
    return redirect(url_for("productos"))

# -------------------------
# CRUD SQLITE
# -------------------------
@app.route("/productos", methods=["GET", "POST"])
def productos():

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        cantidad = int(request.form["cantidad"])

        nuevo = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("productos"))

    lista = Producto.query.all()
    return render_template("producto.html", productos=lista)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    producto = Producto.query.get_or_404(id)

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.precio = float(request.form["precio"])
        producto.cantidad = int(request.form["cantidad"])
        db.session.commit()
        return redirect(url_for("productos"))

    return render_template("editar.html", producto=producto)


@app.route("/eliminar/<int:id>")
def eliminar(id):

    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("productos"))


# -------------------------
# PERSISTENCIA TXT / JSON / CSV
# -------------------------
@app.route("/datos", methods=["GET", "POST"])
def datos():

    data_folder = os.path.join(BASE_DIR, "inventario", "data")
    txt_path = os.path.join(data_folder, "datos.txt")
    json_path = os.path.join(data_folder, "datos.json")
    csv_path = os.path.join(data_folder, "datos.csv")

    if request.method == "POST":

        nombre = request.form["nombre"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]
        formato = request.form["formato"]

        registro = {
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad
        }

        if formato == "txt":
            with open(txt_path, "a", encoding="utf-8") as f:
                f.write(f"{nombre},{precio},{cantidad}\n")

        elif formato == "json":
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    datos = json.load(f)
            except:
                datos = []

            datos.append(registro)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4)

        elif formato == "csv":
            with open(csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([nombre, precio, cantidad])

        return redirect(url_for("datos"))

    # ---- LECTURA ----
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            datos_txt = f.read()
    except:
        datos_txt = ""

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            datos_json = json.load(f)
    except:
        datos_json = []

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            datos_csv = f.read()
    except:
        datos_csv = ""

    return render_template("datos.html",
                           datos_txt=datos_txt,
                           datos_json=datos_json,
                           datos_csv=datos_csv)


if __name__ == "__main__":
    app.run(debug=True)
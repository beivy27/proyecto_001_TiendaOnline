import os
import json
import csv

from flask import Flask, render_template, request, redirect, url_for, flash

from inventario.db import db
from inventario.productos import Producto

# =========================
# Config
# =========================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "inventario.db")

DATA_DIR = os.path.join(BASE_DIR, "inventario", "data")
TXT_PATH = os.path.join(DATA_DIR, "datos.txt")
JSON_PATH = os.path.join(DATA_DIR, "datos.json")
CSV_PATH = os.path.join(DATA_DIR, "datos.csv")


def ensure_data_files():
    """Crea carpeta y archivos si no existen."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(TXT_PATH):
        with open(TXT_PATH, "w", encoding="utf-8") as f:
            f.write("")

    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nombre", "precio", "cantidad"])


def read_txt_rows():
    """Lee TXT como líneas tipo: nombre,precio,cantidad"""
    rows = []
    if not os.path.exists(TXT_PATH):
        return rows

    with open(TXT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                continue
            rows.append({"nombre": parts[0], "precio": parts[1], "cantidad": parts[2]})
    return rows


def append_txt_row(nombre: str, precio: str, cantidad: str):
    with open(TXT_PATH, "a", encoding="utf-8") as f:
        f.write(f"{nombre},{precio},{cantidad}\n")


def read_json_rows():
    if not os.path.exists(JSON_PATH):
        return []
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def append_json_row(row: dict):
    data = read_json_rows()
    data.append(row)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_csv_rows():
    rows = []
    if not os.path.exists(CSV_PATH):
        return rows

    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # r ya trae keys nombre, precio, cantidad
            if not r.get("nombre"):
                continue
            rows.append(
                {
                    "nombre": r.get("nombre", ""),
                    "precio": r.get("precio", ""),
                    "cantidad": r.get("cantidad", ""),
                }
            )
    return rows


def append_csv_row(nombre: str, precio: str, cantidad: str):
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nombre, precio, cantidad])


def validate_nombre_precio_cantidad(nombre: str, precio: str, cantidad: str):
    nombre = (nombre or "").strip()
    precio = (precio or "").strip()
    cantidad = (cantidad or "").strip()

    if not nombre or not precio or not cantidad:
        return False, "Completa nombre, precio y cantidad."

    try:
        precio_f = float(precio)
        if precio_f < 0:
            return False, "El precio no puede ser negativo."
    except Exception:
        return False, "Precio inválido. Usa un número (ej: 12.50)."

    try:
        cantidad_i = int(cantidad)
        if cantidad_i < 0:
            return False, "La cantidad no puede ser negativa."
    except Exception:
        return False, "Cantidad inválida. Usa un entero (ej: 5)."

    return True, ""


# =========================
# App
# =========================
app = Flask(__name__)
app.config["SECRET_KEY"] = "clave123"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Crear tablas y archivos al iniciar
with app.app_context():
    ensure_data_files()
    db.create_all()


# =========================
# Rutas generales
# =========================
@app.route("/")
def home():
    return redirect(url_for("productos"))


# =========================
# CRUD Productos (SQLAlchemy)
# =========================
@app.route("/productos", methods=["GET", "POST"])
def productos():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        cantidad = request.form.get("cantidad")

        ok, msg = validate_nombre_precio_cantidad(nombre, precio, cantidad)
        if not ok:
            flash(msg, "error")
            return redirect(url_for("productos"))

        nuevo = Producto(
            nombre=nombre.strip(),
            precio=float(precio),
            cantidad=int(cantidad),
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Producto guardado ✅", "ok")
        return redirect(url_for("productos"))

    lista = Producto.query.order_by(Producto.id.asc()).all()
    return render_template("producto.html", productos=lista)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    prod = Producto.query.get_or_404(id)

    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        cantidad = request.form.get("cantidad")

        ok, msg = validate_nombre_precio_cantidad(nombre, precio, cantidad)
        if not ok:
            flash(msg, "error")
            return redirect(url_for("editar", id=id))

        prod.nombre = nombre.strip()
        prod.precio = float(precio)
        prod.cantidad = int(cantidad)

        db.session.commit()
        flash("Producto actualizado ✅", "ok")
        return redirect(url_for("productos"))

    return render_template("editar.html", producto=prod)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    prod = Producto.query.get_or_404(id)
    db.session.delete(prod)
    db.session.commit()
    flash("Producto eliminado ✅", "ok")
    return redirect(url_for("productos"))


# =========================
# Persistencia TXT / JSON / CSV
# =========================
@app.route("/datos", methods=["GET", "POST"])
def datos():
    ensure_data_files()

    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        cantidad = request.form.get("cantidad")
        formato = (request.form.get("formato") or "").lower().strip()

        ok, msg = validate_nombre_precio_cantidad(nombre, precio, cantidad)
        if not ok:
            flash(msg, "error")
            return redirect(url_for("datos"))

        row = {"nombre": nombre.strip(), "precio": str(precio).strip(), "cantidad": str(cantidad).strip()}

        if formato == "txt":
            append_txt_row(row["nombre"], row["precio"], row["cantidad"])
            flash("Guardado en TXT ✅", "ok")
        elif formato == "json":
            append_json_row(row)
            flash("Guardado en JSON ✅", "ok")
        elif formato == "csv":
            append_csv_row(row["nombre"], row["precio"], row["cantidad"])
            flash("Guardado en CSV ✅", "ok")
        else:
            flash("Selecciona un formato (TXT/JSON/CSV).", "error")

        return redirect(url_for("datos"))

    # GET: leer todo y mostrar
    datos_txt = read_txt_rows()
    datos_json = read_json_rows()
    datos_csv = read_csv_rows()

    return render_template(
        "datos.html",
        datos_txt=datos_txt,
        datos_json=datos_json,
        datos_csv=datos_csv,
    )


# =========================
# Run
# =========================
if __name__ == "__main__":
    # Si te vuelve a salir "Port 5000 in use", cambia a 5001:
    # app.run(debug=True, port=5001)
    app.run(debug=True)
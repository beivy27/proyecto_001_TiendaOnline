import os
from flask import Flask, render_template, request, redirect, url_for
from database import init_db, fetch_all, fetch_one, insert, update, delete

app = Flask(__name__)

# 🔴 CREA LA TABLA AL INICIAR (esto elimina el error en Render)
init_db()

@app.route("/")
def index():
    productos = fetch_all()
    return render_template("index.html", productos=productos)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])
        insert(nombre, cantidad, precio)
        return redirect(url_for("index"))
    return render_template("producto.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    producto = fetch_one(id)
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])
        update(id, nombre, cantidad, precio)
        return redirect(url_for("index"))
    return render_template("editar.html", producto=producto)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    delete(id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
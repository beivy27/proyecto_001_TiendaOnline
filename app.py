from flask import Flask, render_template

app = Flask(__name__)

# Datos (catálogo)
productos = [
    {"nombre": "Camiseta", "precio": 12.50, "stock": 10},
    {"nombre": "Pantalón", "precio": 25.00, "stock": 5},
    {"nombre": "Zapatos", "precio": 40.00, "stock": 8},
    {"nombre": "Gorra", "precio": 8.00, "stock": 20},
]

@app.route("/")
def index():
    return render_template("index.html", productos=productos)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/producto/<nombre>")
def producto(nombre):
    prod = next((p for p in productos if p["nombre"].lower() == nombre.lower()), None)
    return render_template("producto.html", producto=prod, nombre=nombre)

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

if __name__ == "__main__":
    app.run(debug=True)
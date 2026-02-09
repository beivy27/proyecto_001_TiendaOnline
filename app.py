from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bienvenido a Tienda Online – Catálogo y ofertas"

@app.route("/producto/<nombre>")
def producto(nombre):
    return f"Producto: {nombre} – disponible."

if __name__ == "__main__":
    app.run(debug=True)

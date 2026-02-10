from flask import Flask,render_template


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    

@app.route("/producto/<nombre>")
def producto(nombre):
    return f"Producto: {nombre} – disponible."

if __name__ == "__main__":
    app.run(debug=True)

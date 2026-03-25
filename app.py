from flask import Flask, render_template, request, redirect, url_for, make_response
from fpdf import FPDF

from services.producto_service import (
    listar_productos,
    obtener_producto_por_id,
    insertar_producto,
    actualizar_producto,
    eliminar_producto,
    obtener_reporte_facturas
)

app = Flask(__name__)

@app.route("/")
def inicio():
    return redirect(url_for("ver_productos"))

@app.route("/productos")
def ver_productos():
    productos = listar_productos()
    return render_template("productos/listar.html", productos=productos)

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        insertar_producto(nombre, precio, stock)
        return redirect(url_for("ver_productos"))
    return render_template("productos/formulario.html", producto=None)

@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
def editar_producto(id_producto):
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        actualizar_producto(id_producto, nombre, precio, stock)
        return redirect(url_for("ver_productos"))

    producto = obtener_producto_por_id(id_producto)
    return render_template("productos/formulario.html", producto=producto)

@app.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
def borrar_producto(id_producto):
    eliminar_producto(id_producto)
    return redirect(url_for("ver_productos"))

@app.route("/productos/pdf")
def reporte_productos_pdf():
    datos = obtener_reporte_facturas()

    pdf = FPDF(orientation="L")
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(280, 10, "Reporte de Facturas y Productos", 0, 1, "C")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 9)
    pdf.cell(20, 10, "Factura", 1)
    pdf.cell(35, 10, "Cliente", 1)
    pdf.cell(35, 10, "Usuario", 1)
    pdf.cell(55, 10, "Producto", 1)
    pdf.cell(20, 10, "Cant.", 1)
    pdf.cell(30, 10, "P. Unit.", 1)
    pdf.cell(30, 10, "Subtotal", 1)
    pdf.cell(25, 10, "Total", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 9)
    for fila in datos:
        pdf.cell(20, 10, str(fila["id_factura"]), 1)
        pdf.cell(35, 10, str(fila["cliente"]), 1)
        pdf.cell(35, 10, str(fila["usuario"]), 1)
        pdf.cell(55, 10, str(fila["producto"]), 1)
        pdf.cell(20, 10, str(fila["cantidad"]), 1)
        pdf.cell(30, 10, str(fila["precio_unitario"]), 1)
        pdf.cell(30, 10, str(fila["subtotal"]), 1)
        pdf.cell(25, 10, str(fila["total"]), 1)
        pdf.ln()

    response = make_response(pdf.output(dest="S").encode("latin-1"))
    response.headers.set("Content-Type", "application/pdf")
    response.headers.set("Content-Disposition", "inline; filename=reporte_facturas.pdf")
    return response

if __name__ == "__main__":
    app.run(debug=True)
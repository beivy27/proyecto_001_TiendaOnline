import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="flaskuser",
        password="1234",
        database="tienda_online"
    )
    return conexion
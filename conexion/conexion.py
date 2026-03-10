import mysql.connector


def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root1234*",
        database="tienda_online"
    )
    return conexion
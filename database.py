import sqlite3

def get_connection():
    conn = sqlite3.connect("tienda.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def fetch_all():
    conn = get_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return productos

def fetch_one(id):
    conn = get_connection()
    producto = conn.execute("SELECT * FROM productos WHERE id = ?", (id,)).fetchone()
    conn.close()
    return producto

def insert(nombre, cantidad, precio):
    conn = get_connection()
    conn.execute(
        "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
        (nombre, cantidad, precio)
    )
    conn.commit()
    conn.close()

def update(id, nombre, cantidad, precio):
    conn = get_connection()
    conn.execute(
        "UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?",
        (nombre, cantidad, precio, id)
    )
    conn.commit()
    conn.close()

def delete(id):
    conn = get_connection()
    conn.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
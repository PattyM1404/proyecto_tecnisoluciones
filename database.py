import sqlite3

def conectar():
    return sqlite3.connect("tecnisoluciones.db")

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        precio REAL NOT NULL,
        duracion TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
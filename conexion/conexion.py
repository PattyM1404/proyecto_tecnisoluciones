import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="tecnisoluciones",
        port=3307
    )
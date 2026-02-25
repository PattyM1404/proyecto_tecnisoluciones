from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Bienvenido al Sistema de Ventas – TecniSoluciones EC"

@app.route('/cliente/<nombre>')
def cliente(nombre):
    return f"Cliente {nombre} registrado correctamente."

@app.route('/orden/<int:id>')
def orden(id):
    return f"Orden de trabajo #{id} generada con éxito."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
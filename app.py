from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/cliente/<nombre>')
def cliente(nombre):
    return f"Cliente {nombre} registrado correctamente."

@app.route('/orden/<int:id>')
def orden(id):
    return f"Orden de trabajo #{id} generada con éxito."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
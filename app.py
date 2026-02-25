from flask import Flask, render_template, request, redirect, url_for
from database import crear_tablas
from models import Servicio, GestorServicios
import os

app = Flask(__name__)

crear_tablas()
gestor = GestorServicios()

# =========================
# Rutas principales
# =========================

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')


# =========================
# CRUD SERVICIOS
# =========================

@app.route('/servicios')
def ver_servicios():
    servicios = gestor.obtener_todos()
    return render_template('servicios.html', servicios=servicios)


@app.route('/agregar_servicio', methods=['POST'])
def agregar_servicio():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = float(request.form['precio'])
    duracion = request.form['duracion']

    servicio = Servicio(nombre, descripcion, precio, duracion)
    servicio.guardar()

    return redirect(url_for('ver_servicios'))


@app.route('/eliminar_servicio/<int:id>')
def eliminar_servicio(id):
    gestor.eliminar(id)
    return redirect(url_for('ver_servicios'))


@app.route('/editar_servicio/<int:id>')
def editar_servicio(id):
    servicio = gestor.obtener_por_id(id)
    return render_template('editar_servicio.html', servicio=servicio)


@app.route('/actualizar_servicio/<int:id>', methods=['POST'])
def actualizar_servicio(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = float(request.form['precio'])
    duracion = request.form['duracion']

    gestor.actualizar(id, nombre, descripcion, precio, duracion)

    return redirect(url_for('ver_servicios'))


@app.route('/buscar_servicio', methods=['POST'])
def buscar_servicio():
    nombre = request.form['buscar']
    resultados = gestor.buscar_por_nombre(nombre)
    return render_template('servicios.html', servicios=resultados)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
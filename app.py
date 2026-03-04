from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv

app = Flask(__name__)

# =========================
# CONFIGURACIÓN BASE DE DATOS (ORM)
# =========================

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tecnisoluciones.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# MODELO SERVICIO (ORM)
# =========================

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    duracion = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Servicio {self.nombre}>'

# Crear base de datos automáticamente
with app.app_context():
    db.create_all()

# =========================
# CONFIGURACIÓN CARPETA DATA
# =========================

DATA_FOLDER = os.path.join(basedir, "data")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# =========================
# FUNCIONES DE PERSISTENCIA
# =========================

def guardar_txt(servicio):
    ruta = os.path.join(DATA_FOLDER, "datos.txt")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"{servicio.nombre} | {servicio.descripcion} | {servicio.precio} | {servicio.duracion}\n")


def guardar_json(servicio):
    ruta = os.path.join(DATA_FOLDER, "datos.json")

    datos = []

    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
            except:
                datos = []

    nuevo = {
        "nombre": servicio.nombre,
        "descripcion": servicio.descripcion,
        "precio": servicio.precio,
        "duracion": servicio.duracion
    }

    datos.append(nuevo)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)


def guardar_csv(servicio):
    ruta = os.path.join(DATA_FOLDER, "datos.csv")
    archivo_existe = os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not archivo_existe:
            writer.writerow(["nombre", "descripcion", "precio", "duracion"])

        writer.writerow([servicio.nombre, servicio.descripcion, servicio.precio, servicio.duracion])


# =========================
# RUTAS PRINCIPALES
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
# CRUD SERVICIOS (ORM)
# =========================

@app.route('/servicios')
def ver_servicios():
    servicios = Servicio.query.all()
    return render_template('servicios.html', servicios=servicios)


@app.route('/agregar_servicio', methods=['POST'])
def agregar_servicio():
    nuevo = Servicio(
        nombre=request.form['nombre'],
        descripcion=request.form['descripcion'],
        precio=float(request.form['precio']),
        duracion=request.form['duracion']
    )

    db.session.add(nuevo)
    db.session.commit()

    # Guardar también en archivos
    guardar_txt(nuevo)
    guardar_json(nuevo)
    guardar_csv(nuevo)

    return redirect(url_for('ver_servicios'))


@app.route('/eliminar_servicio/<int:id>')
def eliminar_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    db.session.delete(servicio)
    db.session.commit()
    return redirect(url_for('ver_servicios'))


@app.route('/editar_servicio/<int:id>')
def editar_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    return render_template('editar_servicio.html', servicio=servicio)


@app.route('/actualizar_servicio/<int:id>', methods=['POST'])
def actualizar_servicio(id):
    servicio = Servicio.query.get_or_404(id)

    servicio.nombre = request.form['nombre']
    servicio.descripcion = request.form['descripcion']
    servicio.precio = float(request.form['precio'])
    servicio.duracion = request.form['duracion']

    db.session.commit()
    return redirect(url_for('ver_servicios'))


@app.route('/buscar_servicio', methods=['POST'])
def buscar_servicio():
    nombre = request.form['buscar']
    resultados = Servicio.query.filter(Servicio.nombre.like(f"%{nombre}%")).all()
    return render_template('servicios.html', servicios=resultados)


# =========================
# RUTA PARA VER DATOS EN ARCHIVOS
# =========================

@app.route('/datos')
def ver_datos():

    # Leer TXT
    ruta_txt = os.path.join(DATA_FOLDER, "datos.txt")
    datos_txt = []
    if os.path.exists(ruta_txt):
        with open(ruta_txt, "r", encoding="utf-8") as f:
            datos_txt = f.readlines()

    # Leer JSON
    ruta_json = os.path.join(DATA_FOLDER, "datos.json")
    datos_json = []
    if os.path.exists(ruta_json):
        with open(ruta_json, "r", encoding="utf-8") as f:
            try:
                datos_json = json.load(f)
            except:
                datos_json = []

    # Leer CSV
    ruta_csv = os.path.join(DATA_FOLDER, "datos.csv")
    datos_csv = []
    if os.path.exists(ruta_csv):
        with open(ruta_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            datos_csv = list(reader)

    return render_template("datos.html",
                           datos_txt=datos_txt,
                           datos_json=datos_json,
                           datos_csv=datos_csv)


# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
from conexion.conexion import conectar
from models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from services.servicio_service import obtener_servicios, insertar_servicio, eliminar_servicio
from services.servicio_service import obtener_servicio_por_id, actualizar_servicio
from services.pdf_service import generar_pdf_servicios
from flask import send_file

app = Flask(__name__)
app.secret_key = "secreto"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ==========================
# CARGAR USUARIO
# ==========================
@login_manager.user_loader
def load_user(user_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conexion.close()

    if user:
        return Usuario(user[0], user[1], user[2], user[3])
    return None

# ==========================
# INICIO
# ==========================
@app.route('/')
def inicio():
    return redirect('/login')

# ==========================
# LOGIN
# ==========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE mail=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conexion.close()

        if user and check_password_hash(user[3], password):
            usuario = Usuario(user[0], user[1], user[2], user[3])
            login_user(usuario)
            return redirect('/panel')

        return "Credenciales incorrectas"

    return render_template('login.html')

# ==========================
# REGISTRO
# ==========================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s,%s,%s)",
            (nombre, email, password)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        return redirect('/login')

    return render_template('registro.html')

# ==========================
# PANEL
# ==========================
@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

# ==========================
# LOGOUT
# ==========================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# ==========================
# USUARIOS
# ==========================
@app.route('/usuarios')
@login_required
def usuarios():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios")
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('usuarios.html', usuarios=datos)

@app.route('/agregar_usuario', methods=['POST'])
@login_required
def agregar_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO usuarios (nombre, mail, password) VALUES (%s,%s,%s)",
        (nombre, email, password)
    )

    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect('/usuarios')

@app.route('/eliminar_usuario/<int:id>')
@login_required
def eliminar_usuario(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect('/usuarios')

# ==========================
# SERVICIOS
# ==========================
# ==========================
# SERVICIOS (USANDO SERVICES)
# ==========================
@app.route('/servicios')
@login_required
def servicios():
    datos = obtener_servicios()
    return render_template('servicios.html', servicios=datos)


@app.route('/agregar_servicio', methods=['POST'])
@login_required
def agregar_servicio():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    duracion = request.form['duracion']

    insertar_servicio(nombre, descripcion, precio, duracion)

    return redirect('/servicios')


@app.route('/eliminar_servicio/<int:id>')
@login_required
def eliminar_servicio_route(id):
    eliminar_servicio(id)
    return redirect('/servicios')
@app.route('/editar_servicio/<int:id>')
@login_required
def editar_servicio(id):
    servicio = obtener_servicio_por_id(id)
    return render_template('editar_servicio.html', servicio=servicio)


@app.route('/actualizar_servicio/<int:id>', methods=['POST'])
@login_required
def actualizar_servicio_route(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    duracion = request.form['duracion']

    actualizar_servicio(id, nombre, descripcion, precio, duracion)

    return redirect('/servicios')

# ==========================
# CLIENTES (SIMPLE)
# ==========================
# ==========================
# CLIENTES (CRUD COMPLETO)
# ==========================
@app.route('/clientes')
@login_required
def clientes():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM clientes")
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('clientes.html', clientes=datos)


@app.route('/agregar_cliente', methods=['POST'])
@login_required
def agregar_cliente():
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO clientes (nombre, email, telefono) VALUES (%s,%s,%s)",
        (nombre, email, telefono)
    )

    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect('/clientes')


@app.route('/eliminar_cliente/<int:id>')
@login_required
def eliminar_cliente(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect('/clientes')
@app.route('/editar_cliente/<int:id>')
@login_required
def editar_cliente(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template('editar_cliente.html', cliente=cliente)


@app.route('/actualizar_cliente/<int:id>', methods=['POST'])
@login_required
def actualizar_cliente(id):
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE clientes 
        SET nombre=%s, email=%s, telefono=%s
        WHERE id=%s
    """, (nombre, email, telefono, id))

    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect('/clientes')

# ==========================
# reporte de servicios
# ==========================

@app.route('/reporte_servicios')
@login_required
def reporte_servicios():

    datos = obtener_servicios()

    generar_pdf_servicios(datos)

    return send_file("reporte_servicios.pdf", as_attachment=True)

# ==========================
# RUN
# ==========================
if __name__ == '__main__':
    app.run(debug=True)
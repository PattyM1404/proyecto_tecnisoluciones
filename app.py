from flask import Flask, render_template, request, redirect
from conexion.conexion import conectar
from models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

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
@app.route('/servicios')
@login_required
def servicios():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM servicios")
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('servicios.html', servicios=datos)

@app.route('/agregar_servicio', methods=['POST'])
@login_required
def agregar_servicio():

    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    duracion = request.form['duracion']

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO servicios (nombre, descripcion, precio, duracion) VALUES (%s,%s,%s,%s)",
        (nombre, descripcion, precio, duracion)
    )

    conexion.commit()
    cursor.close()
    conexion.close()

    return redirect('/servicios')

@app.route('/eliminar_servicio/<int:id>')
@login_required
def eliminar_servicio(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM servicios WHERE id=%s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect('/servicios')

# ==========================
# CLIENTES (SIMPLE)
# ==========================
@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html')

# ==========================
# RUN
# ==========================
if __name__ == '__main__':
    app.run(debug=True)
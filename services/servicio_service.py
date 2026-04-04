from conexion.conexion import conectar

# ==========================
# OBTENER TODOS LOS SERVICIOS (CON CLIENTE)
# ==========================
def obtener_servicios():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT s.id, s.nombre, s.descripcion, s.precio, s.duracion, c.nombre
        FROM servicios s
        JOIN clientes c ON s.id_cliente = c.id
    """)
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return datos


# ==========================
# AGREGAR SERVICIO
# ==========================
def insertar_servicio(nombre, descripcion, precio, duracion, id_cliente):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO servicios (nombre, descripcion, precio, duracion, id_cliente)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, descripcion, precio, duracion, id_cliente))

    conexion.commit()
    cursor.close()
    conexion.close()


# ==========================
# ELIMINAR SERVICIO
# ==========================
def eliminar_servicio(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM servicios WHERE id=%s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()


# ==========================
# OBTENER UN SERVICIO POR ID
# ==========================
def obtener_servicio_por_id(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT s.id, s.nombre, s.descripcion, s.precio, s.duracion, s.id_cliente
        FROM servicios s
        WHERE s.id=%s
    """, (id,))
    dato = cursor.fetchone()

    cursor.close()
    conexion.close()

    return dato


# ==========================
# ACTUALIZAR SERVICIO
# ==========================
def actualizar_servicio(id, nombre, descripcion, precio, duracion, id_cliente):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE servicios 
        SET nombre=%s, descripcion=%s, precio=%s, duracion=%s, id_cliente=%s
        WHERE id=%s
    """, (nombre, descripcion, precio, duracion, id_cliente, id))

    conexion.commit()
    cursor.close()
    conexion.close()
from database import conectar

# =========================
# Clase Servicio (POO)
# =========================

class Servicio:
    def __init__(self, nombre, descripcion, precio, duracion, id=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.duracion = duracion

    def guardar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO servicios (nombre, descripcion, precio, duracion) VALUES (?, ?, ?, ?)",
            (self.nombre, self.descripcion, self.precio, self.duracion)
        )

        conn.commit()
        conn.close()


# =========================
# Clase GestorServicios
# =========================

class GestorServicios:

    def obtener_todos(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM servicios")
        filas = cursor.fetchall()
        conn.close()

        servicios = []
        for fila in filas:
            servicio = {
                "id": fila[0],
                "nombre": fila[1],
                "descripcion": fila[2],
                "precio": fila[3],
                "duracion": fila[4]
            }
            servicios.append(servicio)

        return servicios

    def eliminar(self, id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM servicios WHERE id=?", (id,))
        conn.commit()
        conn.close()

    def actualizar(self, id, nombre, descripcion, precio, duracion):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE servicios 
            SET nombre=?, descripcion=?, precio=?, duracion=? 
            WHERE id=?
        """, (nombre, descripcion, precio, duracion, id))

        conn.commit()
        conn.close()

    def buscar_por_nombre(self, nombre):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM servicios WHERE nombre LIKE ?",
            ('%' + nombre + '%',)
        )

        filas = cursor.fetchall()
        conn.close()

        resultados = []
        for fila in filas:
            servicio = {
                "id": fila[0],
                "nombre": fila[1],
                "descripcion": fila[2],
                "precio": fila[3],
                "duracion": fila[4]
            }
            resultados.append(servicio)

        return resultados

    def obtener_por_id(self, id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM servicios WHERE id=?", (id,))
        fila = cursor.fetchone()
        conn.close()

        if fila:
            return {
                "id": fila[0],
                "nombre": fila[1],
                "descripcion": fila[2],
                "precio": fila[3],
                "duracion": fila[4]
            }
        return None
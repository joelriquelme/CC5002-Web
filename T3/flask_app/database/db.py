import pymysql
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

# -- conn ---

def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn

# -- querys --

def create_contact(nombre, email, celular, comuna_id, fecha_creacion):
    query = "INSERT INTO contacto (nombre, email, celular, comuna_id, fecha_creacion) VALUES (%s, %s, %s, %s, %s)"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (nombre, email, celular, comuna_id, fecha_creacion))
    contact_id = cursor.lastrowid
    conn.commit()
    return contact_id

def create_device(contacto_id, nombre, descripcion, tipo, anos_uso, estado):
    query = "INSERT INTO dispositivo (contacto_id, nombre, descripcion, tipo, anos_uso, estado) VALUES (%s, %s, %s, %s, %s, %s)"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (contacto_id, nombre, descripcion, tipo, anos_uso, estado))
    conn.commit()
    return cursor.lastrowid

def create_image(ruta_archivo, nombre_archivo, dispositivo_id):
    query = "INSERT INTO archivo (ruta_archivo, nombre_archivo, dispositivo_id) VALUES (%s, %s, %s)"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (ruta_archivo, nombre_archivo, dispositivo_id))
    conn.commit()
    return cursor.lastrowid

def create_comment(nombre, texto, fecha, dispositivo_id):
    query = "INSERT INTO comentario (nombre, texto, fecha, dispositivo_id) VALUES (%s, %s, %s, %s)"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (nombre, texto, fecha, dispositivo_id))
    conn.commit()
    return cursor.lastrowid

def get_contactos():
    query = "SELECT id, nombre, email, celular, comuna_id, fecha_creacion FROM contacto ORDER BY id DESC"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    contactos = cursor.fetchall()
    return contactos

def get_dispositivos(contacto_id):
    query = "SELECT id, contacto_id, nombre, descripcion, tipo, anos_uso, estado FROM dispositivo WHERE contacto_id=%s"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (contacto_id,))
    dispositivos = cursor.fetchall()
    return dispositivos

def get_archivos(dispositivo_id):
    query = "SELECT id, ruta_archivo, nombre_archivo FROM archivo WHERE dispositivo_id=%s"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (dispositivo_id,))
    archivos = cursor.fetchall()
    return archivos

def get_five_dispositivos(desde):
    query = "SELECT id, contacto_id, nombre, descripcion, tipo, anos_uso, estado FROM dispositivo ORDER BY id DESC LIMIT %s, 5"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (desde))
    dispositivos = cursor.fetchall()
    return dispositivos

def get_five_dispositivos_comuna(desde):
    query = """
        SELECT d.id, d.contacto_id, d.nombre, d.descripcion, d.tipo, d.estado, c.nombre AS comuna_nombre
        FROM dispositivo d
        JOIN contacto co ON d.contacto_id = co.id
        JOIN comuna c ON co.comuna_id = c.id
        ORDER BY d.id DESC
        LIMIT %s, 5
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (desde,))
    dispositivos = cursor.fetchall()
    return dispositivos

def get_contacto_by_dispositivo_id(dispositivo_id):
    query = "SELECT contacto_id FROM dispositivo WHERE id=%s"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (dispositivo_id,))
    contacto_id = cursor.fetchone()
    return contacto_id

def get_contacto_by_id(contacto_id):
    query = "SELECT id, nombre, email, celular, comuna_id, fecha_creacion FROM contacto WHERE id=%s"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (contacto_id,))
    contacto = cursor.fetchone()
    return contacto

def get_dispositivo_by_id(dispositivo_id):
    query = "SELECT id, contacto_id, nombre, descripcion, tipo, anos_uso, estado FROM dispositivo WHERE id=%s"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (dispositivo_id,))
    dispositivo = cursor.fetchone()
    return dispositivo

def get_comentarios(dispositivo_id):
    query ="SELECT id, nombre, texto, fecha FROM comentario WHERE dispositivo_id = %s ORDER BY fecha DESC"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (dispositivo_id,))
    comentarios = cursor.fetchall()
    return comentarios

def get_comuna_by_id(comuna_id):
    query = "SELECT id, nombre FROM comuna WHERE id=%s"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, (comuna_id,))
    comuna = cursor.fetchone()
    return comuna

def get_dispositivos_by_tipo():
    query = """
        SELECT tipo, COUNT(*) AS total
        FROM dispositivo
        GROUP BY tipo
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def get_contactos_by_comuna():
    query = """
        SELECT c.nombre AS comuna, COUNT(*) AS total
        FROM contacto co
        JOIN comuna c ON co.comuna_id = c.id
        GROUP BY c.nombre
    """
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
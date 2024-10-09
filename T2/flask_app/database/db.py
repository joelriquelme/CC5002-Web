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
import pymysql
import json

DB_NAME = "confessions_db"
DB_USERNAME = "dbadmin" #cc5002
DB_PASSWORD = "dbadmin" #programacionweb
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

with open('database/querys.json', 'r') as querys:
	QUERY_DICT = json.load(querys)

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

def get_user_by_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_user_by_id"], (id,))
	user = cursor.fetchone()
	return user

def get_user_by_email(email):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_user_by_email"], (email,))
	user = cursor.fetchone()
	return user

def get_user_by_username(username):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_user_by_username"], (username,))
	user = cursor.fetchone()
	return user

def create_user(username, password, email):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["create_user"], (username, password, email))
	conn.commit()

def get_confessions(page_size):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_confessions"], (page_size,))
	confessions = cursor.fetchall()
	return confessions

def create_confession(conf_text, conf_img, user_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["create_confession"], (conf_text, conf_img, user_id))
	conn.commit()
	

# -- db-related functions --

def register_user(username, password, email):
	# 1. check the email is not in use
	_email_user = get_user_by_email(email)
	if _email_user is not None:
		return False, "El correo ya esta en uso."
	# 2. check the username is not in use
	_username_user = get_user_by_username(username)
	if _username_user is not None:
		return False, "El nombre de usuario esta en uso."
	# 3. create user
	create_user(username, password, email)
	return True, None

def login_user(username, password):
	a_user = get_user_by_username(username)
	if a_user is None:
		return False, "Usuario o contraseña incorrectos."

	a_user_passwd = a_user[3]
	if a_user_passwd != password:
		return False, "Usuario o contraseña incorrectos."
	return True, None


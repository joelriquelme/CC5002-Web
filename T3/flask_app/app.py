from flask import Flask, request, render_template, redirect, url_for
import re
import filetype
from database import db
from datetime import datetime
import hashlib
from werkzeug.utils import secure_filename
import os
from PIL import Image


UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Funciones de validación

def validate_images(images, max_size_mb=5):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}
    MAX_SIZE_BYTES = max_size_mb * 1024 * 1024  # Convertir de MB a Bytes

    for image in images:
        # Check if a file was submitted
        if image is None or image.filename == "":
            return False

        # Check file extension and mimetype
        ftype_guess = filetype.guess(image)
        if ftype_guess is None or ftype_guess.extension not in ALLOWED_EXTENSIONS or ftype_guess.mime not in ALLOWED_MIMETYPES:
            return False

        # Check file size
        if image.content_length > MAX_SIZE_BYTES:
            return False

    return True

def validate_name(name):
    return name and 3 < len(name) < 80

def validate_email(email):
    email_regex = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    return re.match(email_regex, email)

def validate_phone(phone):
    phone_regex = r'^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$'
    if phone:
        return re.match(phone_regex, phone)
    return True

def validate_selection(value):
    return value and value != ''

def validate_device(device, i):
    errors = []
    if not validate_name(device.get('device-name')):
        errors.append(f"Nombre del dispositivo {i+1} inválido.")
    
    if not validate_selection(device.get('device-type')):
        errors.append(f"Debe seleccionar un tipo para el dispositivo {i+1}.")
    
    if not (1 <= int(device.get('device-years', 0)) < 99):
        errors.append(f"Años del dispositivo {i+1} inválidos.")
    
    if not validate_selection(device.get('device-condition')):
        errors.append(f"Debe seleccionar una condición para el dispositivo {i+1}.")

    return errors

@app.route("/")
def index():
    return render_template("donations/index.html")

@app.route("/agregar-donacion", methods=["GET", "POST"])
def agregar_donacion():
    if request.method == "POST":
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        region = request.form.get('region')
        comuna = request.form.get('comuna')

        errores = []  # Variable para almacenar los errores

        # Validaciones de contacto
        if not validate_name(nombre):
            errores.append("Nombre inválido.")
        
        if not validate_email(email):
            errores.append("Email inválido.")
        
        if not validate_phone(celular):
            errores.append("Teléfono inválido.")
        
        if not validate_selection(region):
            errores.append("Debe seleccionar una región.")
        
        if not validate_selection(comuna):
            errores.append("Debe seleccionar una comuna.")

        # Validar datos de dispositivos
        dispositivos_name = [value for key, value in request.form.items() if key.startswith('device-name')]
        dispositivos_description = [value for key, value in request.form.items() if key.startswith('device-description')]
        dispositivos_type = [value for key, value in request.form.items() if key.startswith('device-type')]
        dispositivos_years = [value for key, value in request.form.items() if key.startswith('device-years')]
        dispositivos_condition = [value for key, value in request.form.items() if key.startswith('device-condition')]

        all_images = []
        for i, _ in enumerate(dispositivos_name):
            dispositivo_data = {
                'device-name': dispositivos_name[i],
                'device-type': dispositivos_type[i],
                'device-years': dispositivos_years[i],
                'device-condition': dispositivos_condition[i]
            }
            errores.extend(validate_device(dispositivo_data, i))

            # Validar imágenes
            if i == 0:
                device_photos = request.files.getlist("device-photos[]")
            else:
                device_photos = request.files.getlist(f"device-photos[{i}]")

            if not validate_images(device_photos):
                if i == 0:
                    errores.append("Las imágenes del dispositivo 1 no son válidas.")
                errores.append(f"Las imágenes del dispositivo {i+1} no son válidas.")
            else:
                all_images.append(device_photos)
        # Si hay errores, renderizar el formulario con los errores
        if errores:
            return render_template("donations/agregar-donacion.html", errores=errores)

        else:
            # Crear contacto
            contacto_id = db.create_contact(nombre, email, celular, comuna, datetime.now())

            # Crear dispositivos
            all_ids_dispositivos = []
            for i, _ in enumerate(dispositivos_name):
                id_dispositivo = db.create_device(contacto_id, dispositivos_name[i], dispositivos_description[i], dispositivos_type[i], dispositivos_years[i], dispositivos_condition[i].replace("-", " "))
                all_ids_dispositivos.append(id_dispositivo)

            # Crear imágenes
            for i, images in enumerate(all_images):
                for image in images:
                    # 1. generate random name for img
                    _filename = hashlib.sha256(
                        secure_filename(image.filename) # nombre del archivo
                        .encode("utf-8") # encodear a bytes
                        ).hexdigest()
                    _extension = filetype.guess(image).extension
                    img_filename = f"{_filename}.{_extension}"

                    # 2. save img as a file
                    file_extension = os.path.splitext(img_filename)[1]

                    # image original
                    image.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
                    # image in 1280x1024
                    img = Image.open(image)
                    img = img.resize((1280, 1024), Image.Resampling.LANCZOS)
                    img.save(os.path.join(app.config["UPLOAD_FOLDER"], (os.path.splitext(img_filename)[0]+"_1280x1024"+file_extension)))
                    # image in 640x480
                    img = Image.open(image)
                    img = img.resize((640, 480), Image.Resampling.LANCZOS)
                    img.save(os.path.join(app.config["UPLOAD_FOLDER"], (os.path.splitext(img_filename)[0]+"_640x480"+file_extension)))
                    # image in 120x120
                    img = Image.open(image)
                    img = img.resize((120, 120), Image.Resampling.LANCZOS)
                    img.save(os.path.join(app.config["UPLOAD_FOLDER"], (os.path.splitext(img_filename)[0]+"_120x120"+file_extension)))

                    # 3. save image in db
                    ruta_archivo = f"{UPLOAD_FOLDER}/{img_filename}"
                    db.create_image(ruta_archivo, img_filename, all_ids_dispositivos[i])

            
            return render_template("donations/index.html", success=True)
        
    return render_template("donations/agregar-donacion.html")

@app.route("/ver-dispositivos", methods=["GET", "POST"])
def ver_dispositivos():
    desde = request.args.get('desde', 0, type=int)
    dispositivos = db.get_five_dispositivos_comuna(desde)

    dispositivos_con_imagenes = []
    for dispositivo in dispositivos:
        archivos = db.get_archivos(dispositivo[0]) 
        imagen = archivos[0] if archivos else None 
        #agregar _120x120 a la ruta de la imagen
        if imagen:
            imagen = (imagen[0], imagen[1].replace(".", "_120x120."))
        dispositivos_con_imagenes.append((dispositivo, imagen))

    return render_template("donations/ver-dispositivos.html", dispositivos=dispositivos_con_imagenes, desde=desde)

@app.route("/informacion-dispositivo/<int:dispositivo_id>", methods=["GET"])
def informacion_dispositivo(dispositivo_id):
    dispositivo = db.get_dispositivo_by_id(dispositivo_id)
    print(dispositivo)
    archivos_tuplas = db.get_archivos(dispositivo_id)
    archivos = [archivo[2] for archivo in archivos_tuplas]
    contacto_id = db.get_contacto_by_dispositivo_id(dispositivo_id)
    contacto = db.get_contacto_by_id(contacto_id)
    comentarios = db.get_comentarios(dispositivo_id)
    comuna = db.get_comuna_by_id(contacto[4])

    return render_template("donations/informacion-dispositivo.html", 
                           comuna=comuna,
                           dispositivo=dispositivo, 
                           archivos=archivos, 
                           contacto=contacto,
                           comentarios=comentarios)

@app.route("/agregar-comentario", methods=["POST"])
def agregar_comentario():
    nombre = request.form.get("nombre")
    texto = request.form.get("texto")
    dispositivo_id = request.args.get("dispositivo_id")

    dispositivo = db.get_dispositivo_by_id(dispositivo_id)
    archivos_tuplas = db.get_archivos(dispositivo_id)
    archivos = [archivo[2] for archivo in archivos_tuplas]
    contacto_id = db.get_contacto_by_dispositivo_id(dispositivo_id)
    contacto = db.get_contacto_by_id(contacto_id)
    comentarios = db.get_comentarios(dispositivo_id)
    comuna = db.get_comuna_by_id(contacto[3])

    errores = []

    if not nombre or len(nombre) < 3 or len(nombre) > 80:
        errores.append("El nombre debe tener entre 3 y 80 caracteres.")
    if not texto or len(texto) < 5:
        errores.append("El comentario debe tener al menos 5 caracteres.")
    if not dispositivo_id:
        errores.append("ID de dispositivo inválido.")

    if errores:
        return render_template("donations/informacion-dispositivo.html", 
                                comuna=comuna,
                                errores=errores,
                                dispositivo=dispositivo, 
                                archivos=archivos, 
                                contacto=contacto,
                                comentarios=comentarios)

    db.create_comment(nombre, texto, datetime.now(), dispositivo_id)
    comentarios = db.get_comentarios(dispositivo_id)

    return render_template("donations/informacion-dispositivo.html",
                           comuna=comuna,
                           dispositivo=dispositivo, 
                           archivos=archivos, 
                           contacto=contacto,
                           comentarios=comentarios)
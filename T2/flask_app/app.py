from flask import Flask, request, render_template, redirect, url_for
import re

app = Flask(__name__)

# Funciones de validación
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
        # Validar datos de contacto
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
        dispositivos = request.form.getlist('device-name[]')
        for i, dispositivo in enumerate(dispositivos):
            dispositivo_data = {
                'device-name': request.form.getlist('device-name[]')[i],
                'device-type': request.form.getlist('device-type[]')[i],
                'device-years': request.form.getlist('device-years[]')[i],
                'device-condition': request.form.getlist('device-condition[]')[i]
            }
            errores.extend(validate_device(dispositivo_data, i))

        # Si hay errores, renderizar el formulario con los errores
        if errores:
            return render_template("donations/agregar-donacion.html", errores=errores)

        else:
            return render_template("donations/agregar-donacion.html", success=True)
        
    return render_template("donations/agregar-donacion.html")

@app.route("/ver-dispositivos", methods=["GET", "POST"])
def ver_dispositivos():
    return render_template("donations/ver-dispositivos.html")

@app.route("/informacion-dispositivo", methods=["GET", "POST"])
def informacion_dispositivo():
    return render_template("donations/informacion-dispositivo.html")

if __name__ == "__main__":
    app.run(debug=True)
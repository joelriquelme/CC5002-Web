from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("donations/index.html")

@app.route("/agregar-donacion", methods=["GET", "POST"])
def agregar_donacion():
    return render_template("donations/agregar-donacion.html")

@app.route("/ver-dispositivos", methods=["GET", "POST"])
def ver_dispositivos():
    return render_template("donations/ver-dispositivos.html")

@app.route("/informacion-dispositivo", methods=["GET", "POST"])
def informacion_dispositivo():
    return render_template("donations/informacion-dispositivo.html")
from flask import Flask, render_template, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import random


#############################
# APP FLASK CONFIGURATION
app = Flask(__name__)
app.secret_key = ".."
# DATABASE CONFIGURATION
uri = os.environ.get('MONGO_DB_URI', "mongodb://127.0.0.1")
client = MongoClient(uri)
db = client.kickstarter
#############################


@app.route("/")
def home_view():
    return render_template("home.html")


@app.route("/login")
def login_view():

    if not session.get('id'):
        session['id'] = random.randint(12345, 99999)

    return render_template("login.html", id=session.get('id'))


@app.route("/signup")
def signup_view():
    return render_template("signup.html")


@app.route("/browse")
def browse_view():
    proyectos = list(db.proyectos.find())
    return render_template("browse.html", proyectos=proyectos)


@app.route("/detalle/<id>")
def proyecto_view(id):
    proyectos = db.proyectos.find_one({'_id': ObjectId(id)})   # <---
    # cuando intentas buscar los '_id' necesitas convertir el id a un ObjectID con la funcion ObjectId(id) {'_id': ObjectId(id)}
    videos = db.videos.find_one({'channel_id': id})
    # el id del video no es igual al id del proyecto. se debe cambiar.
    return render_template("proyecto_detalle.html", proyectos=proyectos, videos=videos)


@app.route("/add/<id>")
def add_channel_to_guardados(id):
    proyecto = db.proyectos.find_one({'_id': ObjectId(id)})

    if not session.get('id'):
        return redirect('/')

    user = session.get('id')  # VARIABLE GLOBAL: id

    guardado = {}
    guardado['name'] = proyecto['name']
    guardado['img'] = proyecto['img']
    guardado['descrip'] = proyecto['descrip']
    guardado['autor'] = proyecto['autor']
    guardado['contributed'] = proyecto['contributed']
    guardado['financed'] = proyecto['financed']
    guardado['time'] = proyecto['time']
    guardado['category'] = proyecto['category']
    guardado['country'] = proyecto['country']

    # se guarda en la base de datos el id del usuario.
    guardado['user_id'] = user

    db.guardados.insert_one(guardado)

    return redirect('/guardado')


@app.route("/guardado")
def guardar_view():
    if not session.get('id'):
        return redirect('/')

    user = session.get('id')  # VARIABLE GLOBAL: id
    proyectos = list(db.guardados.find({'user_id': user}))
    return render_template("guardados.html", proyectos=proyectos)


@app.route("/patrocinar/<id>")
def patrocinar_view(id):
    proyectos = db.proyectos.find_one({'_id': ObjectId(id)})
    return render_template("patrocinar.html", proyectos=proyectos)


@app.route("/checkout/<id>/<aporte>")
def check_view(id, aporte):
    proyectos = db.proyectos.find_one({'_id': ObjectId(id)})
    return render_template("checkout.html", proyectos=proyectos, aporte=aporte)

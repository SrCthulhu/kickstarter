from flask import Flask, render_template, redirect
from mongokit import Connection, Document, ObjectId

app = Flask(__name__)

#############################


class Proyecto(Document):
    __database__ = 'kickstarter'
    __collection__ = 'proyectos'
    structure = {
        'img': str,
        'name': str,
        'descrip': str,
        'autor': str,
        'contributed': str,
        'financed': str,
        'time': str,
        'category': str,
        'country': str,
    }


class Guardado(Document):

    __database__ = 'kickstarter'
    __collection__ = 'guardados'
    structure = {
        'img': str,
        'name': str,
        'descrip': str,
        'autor': str,
        'contributed': str,
        'financed': str,
        'time': str,
        'category': str,
        'country': str,
    }


class Video(Document):
    __database__ = 'kickstarter'
    __collection__ = 'videos'
    structure = {
        'source': str,
        'channel_id': str,
    }


db = Connection(host="localhost", port=27017)
db.register([Proyecto, Guardado, Video])


@app.route("/")
def home_view():
    return render_template("home.html")


@app.route("/login")
def login_view():
    return render_template("login.html")


@app.route("/signup")
def signup_view():
    return render_template("signup.html")


@app.route("/browse")
def browse_view():
    proyectos = list(db.Proyecto.find())
    return render_template("browse.html", proyectos=proyectos)


@app.route("/detalle/<id>")
def proyecto_view(id):
    proyectos = db.Proyecto.find_one({'_id': ObjectId(id)})   # <---
    # cuando intentas buscar los '_id' necesitas convertir el id a un ObjectID con la funcion ObjectId(id) {'_id': ObjectId(id)}
    videos = db.Video.find_one({'channel_id': id})
    # el id del video no es igual al id del proyecto. se debe cambiar.
    return render_template("proyecto_detalle.html", proyectos=proyectos, videos=videos)


@app.route("/add/<id>")
def add_channel_to_guardados(id):

    proyectos = db.Proyecto.find_one({'_id': ObjectId(id)})

    newProyecto = db.Guardado()
    newProyecto['img'] = proyectos['img']
    newProyecto['name'] = proyectos['name']
    newProyecto['descrip'] = proyectos['descrip']
    newProyecto['autor'] = proyectos['autor']
    newProyecto['contributed'] = proyectos['contributed']
    newProyecto['financed'] = proyectos['financed']
    newProyecto['time'] = proyectos['time']
    newProyecto['category'] = proyectos['category']
    newProyecto['country'] = proyectos['country']
    newProyecto.save()

    return redirect('/guardado')


@app.route("/guardado")
def guardar_view():
    proyectos = list(db.Guardado.find())
    return render_template("guardados.html", proyectos=proyectos)


@app.route("/patrocinar/<id>")
def patrocinar_view(id):
    proyectos = db.Proyecto.find_one({'_id': ObjectId(id)})
    return render_template("patrocinar.html", proyectos=proyectos)


@app.route("/checkout/<id>/<aporte>")
def check_view(id, aporte):
    proyectos = db.Proyecto.find_one({'_id': ObjectId(id)})
    return render_template("checkout.html", proyectos=proyectos, aporte=aporte)

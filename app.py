from flask import Flask, render_template, request, redirect
from uuid import uuid4
from models.models import Users, Task, db
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)

# Configuro el motor de base de datos y la cadena de conexion importando las constantes
# significativas para la app.
import config
app.config.from_object(config)

# Asociando la Base de Datos con el App de Flask
db.init_app(app)

# Pimer inicio de la Aplicacion debo saber si la base de datos esta creada o no
with app.app_context():
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
        db.create_all()
        user = Users(id=str(uuid4()), username='admin', password='admin1234', email='admin@example.com')
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error al insertar usuario admin: {e}")
    else:
        users = Users.query.all()
        user_id = users[0].id

@app.route("/")
def index():
    tasks_db = Task.query.all()
    return render_template("index.html", tasks_db=tasks_db)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        #Agrego la Tarea a la base de datos
        id=str(uuid4())
        task_db = Task(id=id, title=title, description=description, user_id=user_id)
        db.session.add(task_db)
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error al Crear Tarea: {e}")
        return redirect("/")
    else:
        return render_template("create.html")


@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit(task_id):
    task_db = Task.query.filter_by(id=task_id).first()
    if task_db:
        if request.method == "POST":
            title = request.form["title"]
            description = request.form["description"]

            # ACA Actualizamos la base de datos
            if task_db:
                task_db.title = title
                task_db.description = description

                try:
                    db.session.commit()
                except Exception as e:
                    print(f"Error al Actualizar Tarea: {e}")
            # EN EL CASO DE QUE NO ENCONTREMOS LA TAREA DEBEREMOS INFORMAR ALGO !!!!!!
            return redirect("/")
        else:
            return render_template("edit.html", task=task_db)
    else:
        return redirect('/')

@app.route("/delete/<task_id>")
def delete(task_id):
    task_db = Task.query.get(task_id)
    if task_db:
        try:
            db.session.delete(task_db)
            db.session.commit()
            # return redirect('/') # SINO ESTUVISE MANEJANDO LOS DATOS EN MEMORIA DEBERIA DESMARCAR ESTA LINEA
        except Exception as e:
            print(f"Error al Eliminar Tarea: {e}")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

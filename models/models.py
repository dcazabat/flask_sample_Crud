from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Creo la variables que se va a encarga de conectarse a la base de datos
db = SQLAlchemy()

# Creamos los Modelos (Tablas de la BD)
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.String(200), primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text())
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(200), db.ForeignKey('users.id'), nullable=False)

    def __str__(self):
        return f'Titulo: {self.title}, Fecha de Creacion {self.date_create}'
    

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(200), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))
    # Planteo la relacion
    task = db.relationship('Task', backref='users', lazy=True)

    def __str__(self):
        return self.username
    
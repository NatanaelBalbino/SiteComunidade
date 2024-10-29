from main import database
from datetime import datetime


class Usuario(database.Model):
    id = database.Column(database.Integerm, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg', nullable=True)


class Post(database.Model):
    id = database.Column(database.Integerm, primary_key=True)
    titulo = database.Colunm(database.String, nullable=True)
    corpo = database.Colunm(database.text, nullable=True)
    data_criacao = database.Colunm(database.DateTime, default=datetime.utcnow, nullable=True)

from main import database
from datetime import datetime


class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg', nullable=True)
    cursos = database.Column(database.String, default='Não Informado', nullable=True)
    post = database.relationship('Post', backref='autor', lazy=True)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=True)
    corpo = database.Column(database.Text, nullable=True)
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow, nullable=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=True)

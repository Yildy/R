from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicacion_id = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime)
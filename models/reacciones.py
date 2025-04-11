from config import db

class Reaccion(db.Model):
    __tablename__ = 'reacciones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicacion_id = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime)
    estadoreaccion = db.Column(db.Boolean, default=True)
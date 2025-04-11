from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Publicacion(db.Model):
    __tablename__ = 'publicaciones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime)
    tipo = db.Column(db.Enum('queja', 'educativo', name='tipo_enum'), default='queja')
    imageurl = db.Column(db.String(255), nullable=False)
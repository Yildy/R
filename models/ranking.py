from config import db

class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    puntos = db.Column(db.Integer, default=0)
    fecha = db.Column(db.DateTime)
    medalla = db.Column(db.String(50), default='Ninguna')
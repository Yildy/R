from config import db

class CentroDeReciclaje(db.Model):
    __tablename__ = 'centro_de_reciclaje'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    tipo_residuo = db.Column(db.String(100), nullable=False)
    latitud = db.Column(db.Numeric(10, 8))
    longitud = db.Column(db.Numeric(11, 8))
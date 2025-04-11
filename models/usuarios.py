from datetime import datetime, timezone
from config import db
from models.datos_personales import DatosPersonales  # Importar el modelo relacionado

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    verificado = db.Column(db.Boolean, default=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relación uno a uno con DatosPersonales
    datos_personales = db.relationship('DatosPersonales', backref='usuario', uselist=False)
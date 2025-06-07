from config import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    verificado = db.Column(db.Boolean, default=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.now()) 
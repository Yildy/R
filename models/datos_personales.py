from config import db

class DatosPersonales(db.Model):
    __tablename__ = 'datos_personales'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)  # Clave foránea
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)

    # Relación con el modelo Usuario
    usuario = db.relationship('Usuario', backref='datos_personales', lazy=True)

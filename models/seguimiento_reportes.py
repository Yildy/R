from config import db

class SeguimientoReporte(db.Model):
    __tablename__ = 'seguimiento_reportes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    publicacion_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='activo')
    contenido = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.Enum('contenidoexplicito', 'contenido', name='tipo_reporte_enum'))
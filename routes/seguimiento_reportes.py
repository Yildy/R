from flask import Blueprint, request, jsonify
from models.seguimiento_reportes import SeguimientoReporte
from config import db

seguimiento_reportes_bp = Blueprint('seguimiento_reportes', __name__)

# Ruta para obtener todos los reportes
@seguimiento_reportes_bp.route('/seguimiento_reportes/obtener', methods=['GET'])
def obtener_reportes():
    reportes = SeguimientoReporte.query.all()
    return jsonify([{
        'id': reporte.id,
        'usuario_id': reporte.usuario_id,
        'publicacion_id': reporte.publicacion_id,
        'fecha': reporte.fecha,
        'estado': reporte.estado,
        'contenido': reporte.contenido,
        'tipo': reporte.tipo
    } for reporte in reportes]), 200

# Ruta para crear un nuevo reporte
@seguimiento_reportes_bp.route('/seguimiento_reportes/registro', methods=['POST'])
def crear_reporte():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    publicacion_id = data.get('publicacion_id')
    contenido = data.get('contenido')
    tipo = data.get('tipo', 'contenido')
    estado = data.get('estado', 'activo')
    fecha = data.get('fecha')

    if not usuario_id or not contenido:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    nuevo_reporte = SeguimientoReporte(
        usuario_id=usuario_id,
        publicacion_id=publicacion_id,
        contenido=contenido,
        tipo=tipo,
        estado=estado,
        fecha=fecha
    )
    db.session.add(nuevo_reporte)
    db.session.commit()

    return jsonify({'mensaje': 'Reporte creado exitosamente'}), 201

# Ruta para actualizar un reporte
@seguimiento_reportes_bp.route('/seguimiento_reportes/<int:reporte_id>', methods=['PUT'])
def actualizar_reporte(reporte_id):
    reporte = SeguimientoReporte.query.get(reporte_id)
    if not reporte:
        return jsonify({'error': 'Reporte no encontrado'}), 404

    data = request.get_json()
    reporte.contenido = data.get('contenido', reporte.contenido)
    reporte.tipo = data.get('tipo', reporte.tipo)
    reporte.estado = data.get('estado', reporte.estado)
    db.session.commit()

    return jsonify({'mensaje': 'Reporte actualizado exitosamente'}), 200

# Ruta para eliminar un reporte
@seguimiento_reportes_bp.route('/seguimiento_reportes/<int:reporte_id>', methods=['DELETE'])
def eliminar_reporte(reporte_id):
    reporte = SeguimientoReporte.query.get(reporte_id)
    if not reporte:
        return jsonify({'error': 'Reporte no encontrado'}), 404

    db.session.delete(reporte)
    db.session.commit()

    return jsonify({'mensaje': 'Reporte eliminado exitosamente'}), 200

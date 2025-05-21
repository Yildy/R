from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models.reacciones import Reaccion
from datetime import datetime

reacciones = Blueprint('reacciones', __name__)

@reacciones.route('/reacciones', methods=['POST'])
@jwt_required()
def crear_reaccion():
    user_id = get_jwt_identity()
    data = request.get_json()
    publicacion_id = data.get('publicacion_id')
    estadoreaccion = data.get('estadoreaccion', True)

    if not publicacion_id:
        return jsonify({'error': 'El ID de la publicación es obligatorio'}), 400

    existing_reaccion = Reaccion.query.filter_by(
        publicacion_id=publicacion_id,
        usuario_id=user_id
    ).first()

    if existing_reaccion:
        existing_reaccion.estadoreaccion = estadoreaccion
        existing_reaccion.fecha = datetime.utcnow()
        db.session.commit()
        return jsonify({'mensaje': 'Reacción actualizada correctamente', 'id': existing_reaccion.id, 'estado': existing_reaccion.estadoreaccion}), 200
    else:
        nueva_reaccion = Reaccion(
            publicacion_id=publicacion_id,
            usuario_id=user_id,
            fecha=datetime.utcnow(),
            estadoreaccion=estadoreaccion
        )
        db.session.add(nueva_reaccion)
        db.session.commit()
        return jsonify({'mensaje': 'Reacción creada correctamente', 'id': nueva_reaccion.id, 'estado': nueva_reaccion.estadoreaccion}), 201

@reacciones.route('/reacciones/<int:reaccion_id>', methods=['GET'])
def obtener_reaccion(reaccion_id):
    reaccion = Reaccion.query.get(reaccion_id)
    if not reaccion:
        return jsonify({'error': 'Reacción no encontrada'}), 404

    return jsonify({
        'id': reaccion.id,
        'publicacion_id': reaccion.publicacion_id,
        'usuario_id': reaccion.usuario_id,
        'fecha': str(reaccion.fecha),
        'estadoreaccion': reaccion.estadoreaccion
    }), 200

@reacciones.route('/reacciones/<int:reaccion_id>', methods=['PUT'])
@jwt_required()
def actualizar_reaccion(reaccion_id):
    user_id = get_jwt_identity()
    reaccion = Reaccion.query.get(reaccion_id)
    if not reaccion:
        return jsonify({'error': 'Reacción no encontrada'}), 404

    if reaccion.usuario_id != user_id:
        return jsonify({'error': 'No tienes puedes editar esta reacción'}), 403

    data = request.get_json()
    if 'estadoreaccion' in data:
        reaccion.estadoreaccion = data['estadoreaccion']
        reaccion.fecha = datetime.utcnow()
        db.session.commit()
        return jsonify({'mensaje': 'Reacción actualizada correctamente', 'id': reaccion.id, 'estado': reaccion.estadoreaccion}), 200
    else:
        return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400

@reacciones.route('/reacciones/<int:reaccion_id>', methods=['DELETE'])
@jwt_required()
def eliminar_reaccion(reaccion_id):
    user_id = get_jwt_identity()
    reaccion = Reaccion.query.get(reaccion_id)
    if not reaccion:
        return jsonify({'error': 'Reacción no encontrada'}), 404

    if reaccion.usuario_id != user_id:
        return jsonify({'error': 'No puedes eliminar esta reacción'}), 403

    db.session.delete(reaccion)
    db.session.commit()
    return jsonify({'mensaje': 'Reacción eliminada correctamente'}), 200

@reacciones.route('/publicaciones/<int:publicacion_id>/reacciones', methods=['GET'])
def obtener_reacciones_por_publicacion(publicacion_id):
    reacciones = Reaccion.query.filter_by(publicacion_id=publicacion_id).all()
    resultados = []
    for reaccion in reacciones:
        resultados.append({
            'id': reaccion.id,
            'usuario_id': reaccion.usuario_id,
            'fecha': str(reaccion.fecha),
            'estadoreaccion': reaccion.estadoreaccion
        })
    return jsonify(resultados), 200

@reacciones.route('/publicaciones/<int:publicacion_id>/reacciones/count', methods=['GET'])
def contar_reacciones_por_publicacion(publicacion_id):
    count = Reaccion.query.filter_by(publicacion_id=publicacion_id, estadoreaccion=True).count()
    return jsonify({'count': count}), 200
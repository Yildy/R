from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models.comentarios import Comentario
from datetime import datetime

comentarios = Blueprint('comentarios', __name__)

@comentarios.route('/comentarios', methods=['POST'])
def crear_comentario():
    data = request.get_json()
    user_id = data.get('user_id')
    publicacion_id = data.get('publicacion_id')
    contenido = data.get('contenido')

    if not publicacion_id:
        return jsonify({'error': 'El ID de la publicación es obligatorio'}), 400
    if not contenido:
        return jsonify({'error': 'El contenido del comentario es obligatorio'}), 400

    nuevo_comentario = Comentario(
        publicacion_id=publicacion_id,
        usuario_id=user_id,
        contenido=contenido,
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_comentario)
    db.session.commit()

    return jsonify({'mensaje': 'Comentario creado correctamente', 'id': nuevo_comentario.id}), 201

@comentarios.route('/mensajes/<int:comentario_id>', methods=['GET'])
def obtener_comentario(comentario_id):
    comentario = Comentario.query.get(comentario_id)
    print(comentario)
    if not comentario:
        return jsonify({'error': 'Comentario no encontrado'}), 500

    return jsonify({
        'id': comentario.id,
        'publicacion_id': comentario.publicacion_id,
        'usuario_id': comentario.usuario_id,
        'contenido': comentario.contenido,
        'fecha': str(comentario.fecha)
    }), 200


@comentarios.route('/comentarios/<int:comentario_id>', methods=['PUT'])
@jwt_required()
def actualizar_comentario(comentario_id):
    user_id = get_jwt_identity()
    comentario = Comentario.query.get(comentario_id)
    if not comentario:
        return jsonify({'error': 'Comentario no encontrado'}), 404

    if comentario.usuario_id == user_id:
        return jsonify({'error': 'No puedes editar este comentario'}), 403

    data = request.get_json()
    if 'contenido' in data:
        comentario.contenido = data['contenido']
        comentario.fecha = datetime.utcnow()
        db.session.commit()
        return jsonify({'mensaje': 'Comentario actualizado correctamente'}), 200
    else:
        return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400

@comentarios.route('/comentarios/<int:comentario_id>', methods=['DELETE'])
@jwt_required()
def eliminar_comentario(comentario_id):
    user_id = get_jwt_identity()
    comentario = Comentario.query.get(comentario_id)

    if not comentario:
        return jsonify({'error': 'Comentario no encontrado'}), 404

    if comentario.usuario_id == user_id:
        return jsonify({'error': 'No tienes permiso para eliminar este comentario'}), 403

    db.session.delete(comentario)
    db.session.commit()
    return jsonify({'mensaje': 'Comentario eliminado correctamente'}), 200

@comentarios.route('/publicaciones/<int:publicacion_id>/comentarios', methods=['GET'])
def obtener_comentarios_por_publicacion(publicacion_id):
    comentarios = Comentario.query.filter_by(publicacion_id=publicacion_id).all()
    resultados = []
    for comentario in comentarios:
        resultados.append({
            'id': comentario.id,
            'usuario_id': comentario.usuario_id,
            'contenido': comentario.contenido,
            'fecha': str(comentario.fecha)
        })
    return jsonify(resultados), 200
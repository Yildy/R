from flask import Blueprint, request, jsonify
from models.ranking import Ranking
from config import db

ranking_bp = Blueprint('ranking', __name__)

# Ruta para obtener todos los rankings
@ranking_bp.route('/ranking/obtener', methods=['GET'])
def obtener_rankings():
    rankings = Ranking.query.all()
    return jsonify([{
        'id': ranking.id,
        'usuario_id': ranking.usuario_id,
        'puntos': ranking.puntos,
        'fecha': ranking.fecha,
        'medalla': ranking.medalla
    } for ranking in rankings]), 200

# Ruta para crear un nuevo ranking
@ranking_bp.route('/ranking/registro', methods=['POST'])
def crear_ranking():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    puntos = data.get('puntos', 0)
    fecha = data.get('fecha')
    medalla = data.get('medalla', 'Ninguna')

    if not usuario_id:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    nuevo_ranking = Ranking(
        usuario_id=usuario_id,
        puntos=puntos,
        fecha=fecha,
        medalla=medalla
    )
    db.session.add(nuevo_ranking)
    db.session.commit()

    return jsonify({'mensaje': 'Ranking creado exitosamente'}), 201

# Ruta para actualizar un ranking
@ranking_bp.route('/ranking/<int:ranking_id>', methods=['PUT'])
def actualizar_ranking(ranking_id):
    ranking = Ranking.query.get(ranking_id)
    if not ranking:
        return jsonify({'error': 'Ranking no encontrado'}), 404

    data = request.get_json()
    ranking.usuario_id = data.get('usuario_id', ranking.usuario_id)
    ranking.puntos = data.get('puntos', ranking.puntos)
    ranking.fecha = data.get('fecha', ranking.fecha)
    ranking.medalla = data.get('medalla', ranking.medalla)
    db.session.commit()

    return jsonify({'mensaje': 'Ranking actualizado exitosamente'}), 200

# Ruta para eliminar un ranking
@ranking_bp.route('/ranking/<int:id>', methods=['DELETE'])
def eliminar_ranking(id):
    # Buscar el registro de ranking por ID
    ranking = Ranking.query.get(id)
    if not ranking:
        return jsonify({'error': 'Registro de ranking no encontrado'}), 404

    # Eliminar el registro de ranking
    db.session.delete(ranking)
    db.session.commit()
    return jsonify({'mensaje': 'Registro de ranking eliminado correctamente'}), 200
from flask import Blueprint, request, jsonify
from models.centro_de_reciclaje import CentroDeReciclaje
from config import db

centros_reciclaje_bp = Blueprint('centros_reciclaje', __name__)

# Ruta para obtener todos los centros de reciclaje
@centros_reciclaje_bp.route('/centros_reciclaje/obtener', methods=['GET'])
def mostrar_centros():
    centros = CentroDeReciclaje.query.all()
    return jsonify([{
        'id': centro.id,
        'nombre': centro.nombre,
        'usuario_id': centro.usuario_id,
        'direccion': centro.direccion,
        'tipo_residuo': centro.tipo_residuo,
        'latitud': centro.latitud,
        'longitud': centro.longitud
    } for centro in centros]), 200

# Ruta para crear un nuevo centro de reciclaje
@centros_reciclaje_bp.route('/centros_reciclaje/registro', methods=['POST'])
def crear_centro():
    data = request.get_json()
    nombre = data.get('nombre')
    usuario_id = data.get('usuario_id')
    direccion = data.get('direccion')
    tipo_residuo = data.get('tipo_residuo')
    latitud = data.get('latitud')
    longitud = data.get('longitud')

    if not nombre or not usuario_id or not direccion or not latitud or not longitud:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    nuevo_centro = CentroDeReciclaje(
        nombre=nombre,
        usuario_id=usuario_id,
        direccion=direccion,
        tipo_residuo=tipo_residuo,
        latitud=latitud,
        longitud=longitud
    )
    db.session.add(nuevo_centro)
    db.session.commit()

    return jsonify({'mensaje': 'Centro de reciclaje creado exitosamente'}), 201

# Ruta para actualizar un centro de reciclaje
@centros_reciclaje_bp.route('/centros_reciclaje/<int:centro_id>', methods=['PUT'])
def actualizar_centro(centro_id):
    centro = CentroDeReciclaje.query.get(centro_id)
    if not centro:
        return jsonify({'error': 'Centro de reciclaje no encontrado'}), 404

    data = request.get_json()
    centro.nombre = data.get('nombre', centro.nombre)
    centro.usuario_id = data.get('usuario_id', centro.usuario_id)
    centro.direccion = data.get('direccion', centro.direccion)
    centro.tipo_residuo = data.get('tipo_residuo', centro.tipo_residuo)
    centro.latitud = data.get('latitud', centro.latitud)
    centro.longitud = data.get('longitud', centro.longitud)
    db.session.commit()

    return jsonify({'mensaje': 'Centro de reciclaje actualizado exitosamente'}), 200

# Ruta para eliminar un centro de reciclaje
@centros_reciclaje_bp.route('/centros_reciclaje/<int:id>', methods=['DELETE'])
def eliminar_centro(centro_id):
    # Buscar el centro de reciclaje por ID
    centro = CentroDeReciclaje.query.get(centro_id)
    if not centro:
        return jsonify({'error': 'Centro de reciclaje no encontrado'}), 404

    # Eliminar el centro de reciclaje
    db.session.delete(centro)
    db.session.commit()
    return jsonify({'mensaje': 'Centro de reciclaje eliminado correctamente'}), 200

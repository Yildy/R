from flask import Blueprint, request, jsonify
from models.usuarios import Usuario
from models.datos_personales import DatosPersonales
from config import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

datos_personales_new_bp = Blueprint('datos_personales_new', __name__)

@datos_personales_new_bp.route('/datos_personales/new', methods=['POST'])
@jwt_required()
def crear_nuevos_datos_personales():
    user_id = get_jwt_identity()
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    telefono = data.get('telefono')
    fecha_nacimiento_str = data.get('fecha_nacimiento')

    if not nombre or not apellido:
        return jsonify({'error': 'Nombre y apellido son obligatorios'}), 400

    if DatosPersonales.query.filter_by(usuario_id=user_id).first():
        return jsonify({'error': 'Los datos personales ya existen para este usuario.'}), 409

    fecha_nacimiento = None
    if fecha_nacimiento_str:
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de fecha de nacimiento inválido (YYYY-MM-DD)'}), 400

    nuevos_datos = DatosPersonales(
        usuario_id=user_id,
        nombre=nombre,
        apellido=apellido,
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento
    )
    db.session.add(nuevos_datos)
    db.session.commit()

    return jsonify({'mensaje': 'Datos personales guardados correctamente'}), 201
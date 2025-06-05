from flask import Blueprint, request, jsonify
from models.usuarios import Usuario
from models.datos_personales import DatosPersonales
from config import db, bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

datos_personales_new_bp = Blueprint('datos_personales', __name__)

@datos_personales_new_bp.route('/datos_personales/registro', methods=['POST'])
def registrar_usuario_con_datos_personales():
    data = request.get_json()

    # Datos para el modelo Usuario
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    nombre_usuario = data.get('nombre_usuario')

    # Datos para el modelo DatosPersonales
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    telefono = data.get('telefono')
    fecha_nacimiento = data.get('fecha_nacimiento')

    # Validaciones
    if not correo or not contraseña or not nombre_usuario or not nombre or not apellido:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({'error': 'Correo ya registrado'}), 400

    # Crear el usuario
    hash_contraseña = bcrypt.generate_password_hash(contraseña).decode('utf-8')
    nuevo_usuario = Usuario(correo=correo, contraseña=hash_contraseña, nombre_usuario=nombre_usuario)
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Crear los datos personales
    datos_personales = DatosPersonales(
        usuario_id=nuevo_usuario.id,
        nombre=nombre,
        apellido=apellido,
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento
    )
    db.session.add(datos_personales)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado con datos personales correctamente'}), 201

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
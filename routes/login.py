from flask import Blueprint, request, jsonify
from models.usuarios import Usuario
from config import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

acceso = Blueprint('login', __name__)

@acceso.route('/usuario/acceso', methods=['POST'])
def login_usuario():
    data = request.get_json()
    correo = data.get('correo')
    contrasena = data.get('contraseña')

    usuario = Usuario.query.filter_by(correo=correo).first()
    if not usuario or not bcrypt.check_password_hash(usuario.contrasena, contrasena):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    access_token = create_access_token(identity=str(usuario.id))
    return jsonify({
        'mensaje': 'Login exitoso',
        'token': access_token,
        'usuario': {
            'id': usuario.id,
            'correo': usuario.correo,
            'nombre_usuario': usuario.nombre_usuario
        }
    }), 200

@acceso.route('/usuario/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    correo = data.get('correo')
    contrasena = data.get('contraseña')
    nombre_usuario = data.get('nombre_usuario')

    if not correo or not contrasena or not nombre_usuario:
        return jsonify({'error': 'Faltan campos'}), 400

    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({'error': 'Correo ya registrado'}), 400

    hash_contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    nuevo_usuario = Usuario(correo=correo, contrasena=hash_contrasena, nombre_usuario=nombre_usuario)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Registro exitoso'}), 201

@acceso.route('/perfil', methods=['GET'])
@jwt_required()
def perfil_usuario():
    # Extraer el user_id del token JWT
    user_id = int(get_jwt_identity())
    # Buscar al usuario en la base de datos
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Retornar la información del perfil del usuario
    return jsonify({
        'id': usuario.id,
        'correo': usuario.correo,
        'nombre_usuario': usuario.nombre_usuario,
        'verificado': usuario.verificado,
        'fecha_registro': usuario.fecha_registro
    }), 200

@acceso.route('/usuario/actualizar', methods=['PUT'])
@jwt_required()
def actualizar_usuario():
    user_id = int(get_jwt_identity())  # Obtener el ID del usuario desde el token JWT
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()
    if 'correo' in data:
        usuario.correo = data['correo']
    if 'nombre_usuario' in data:
        usuario.nombre_usuario = data['nombre_usuario']
    if 'contraseña' in data:
        usuario.contrasena = bcrypt.generate_password_hash(data['contrasena']).decode('utf-8')

    db.session.commit()
    return jsonify({'mensaje': 'Usuario actualizado correctamente'}), 200

@acceso.route('/usuario/eliminar', methods=['DELETE'])
@jwt_required()
def eliminar_usuario():
    user_id = int(get_jwt_identity())  # Obtener el ID del usuario desde el token JWT
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200

@acceso.route('/usuario/<int:usuario_id>', methods=['GET'])
def obtener_nombre_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({'nombre_usuario': usuario.nombre_usuario}), 200
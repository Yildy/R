from flask import Blueprint, request, jsonify
from models.usuarios import Usuario
from config import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

acceso = Blueprint('login', __name__)

@acceso.route('/usuario/acceso', methods=['POST'])
def login_usuario():
    data = request.get_json()
    correo = data.get('correo')
    contraseña = data.get('contraseña')

    usuario = Usuario.query.filter_by(correo=correo).first()
    if not usuario or not bcrypt.check_password_hash(usuario.contraseña, contraseña):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    access_token = create_access_token(identity=usuario.id)
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
    contraseña = data.get('contraseña')
    nombre_usuario = data.get('nombre_usuario')

    if not correo or not contraseña or not nombre_usuario:
        return jsonify({'error': 'Faltan campos'}), 400

    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({'error': 'Correo ya registrado'}), 400

    hash_contraseña = bcrypt.generate_password_hash(contraseña).decode('utf-8')
    nuevo_usuario = Usuario(correo=correo, contraseña=hash_contraseña, nombre_usuario=nombre_usuario)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Registro exitoso'}), 201


@acceso.route('/perfil', methods=['GET'])
@jwt_required()
def perfil_usuario():
    user_id = get_jwt_identity()
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({
        'id': usuario.id,
        'correo': usuario.correo,
        'nombre_usuario': usuario.nombre_usuario,
        'verificado': usuario.verificado,
        'fecha_registro': usuario.fecha_registro
    }), 200
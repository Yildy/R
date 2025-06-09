from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models.publicaciones import Publicacion
from datetime import datetime
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'  # Carpeta donde se guardarán las imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Tipos de archivos permitidos

publicaciones = Blueprint('publicaciones', __name__)
publicaciones.config = {'UPLOAD_FOLDER': UPLOAD_FOLDER}

# Función para verificar extensiones permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@publicaciones.route('/publicaciones', methods=['POST'])
@jwt_required()
def crear_publicacion():
    user_id = get_jwt_identity()
    data = request.form  # Usar request.form para datos de texto
    contenido = data.get('contenido')
    tipo = data.get('tipo', 'queja')
    file = request.files.get('image')  # Obtener el archivo de imagen

    if not contenido:
        return jsonify({'error': 'El contenido de la publicación es obligatorio'}), 400
    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'La imagen es obligatoria y debe ser un archivo válido'}), 400

    # Crear la carpeta de uploads si no existe
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Guardar la imagen en el servidor
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    if tipo not in ['queja', 'educativo']:
        return jsonify({'error': 'El tipo de publicación debe ser "queja" o "educativo"'}), 400

    nueva_publicacion = Publicacion(
        usuario_id=user_id,
        contenido=contenido,
        fecha=datetime.utcnow(),
        tipo=tipo,
        imageurl=filepath  # Guardar la ruta de la imagen en la base de datos
    )
    db.session.add(nueva_publicacion)
    db.session.commit()

    return jsonify({'mensaje': 'Publicación creada correctamente', 'id': nueva_publicacion.id}), 201

@publicaciones.route('/publicaciones', methods=['GET'])
def obtener_publicaciones():
    lista_publicaciones = Publicacion.query.all()
    resultados = []
    for publicacion in lista_publicaciones:
        resultados.append({
            'id': publicacion.id,
            'usuario_id': publicacion.usuario_id,
            'contenido': publicacion.contenido,
            'fecha': str(publicacion.fecha),
            'tipo': publicacion.tipo,
            'imageurl': publicacion.imageurl
        })
    return jsonify(resultados), 200

@publicaciones.route('/publicaciones/<int:publicacion_id>', methods=['GET'])
def obtener_publicacion(publicacion_id):
    publicacion = Publicacion.query.get(publicacion_id)
    if not publicacion:
        return jsonify({'error': 'Publicación no encontrada'}), 404

    return jsonify({
        'id': publicacion.id,
        'usuario_id': publicacion.usuario_id,
        'contenido': publicacion.contenido,
        'fecha': str(publicacion.fecha),
        'tipo': publicacion.tipo,
        'imageurl': publicacion.imageurl
    }), 200

@publicaciones.route('/publicaciones/<int:publicacion_id>', methods=['PUT'])
@jwt_required()
def actualizar_publicacion(publicacion_id):
    user_id = get_jwt_identity()
    publicacion = Publicacion.query.get(publicacion_id)
    if not publicacion:
        return jsonify({'error': 'Publicación no encontrada'}), 404

    if publicacion.usuario_id == user_id:
        return jsonify({'error': 'No tienes permiso para editar esta publicación'}), 403

    data = request.get_json()
    if 'contenido' in data:
        publicacion.contenido = data['contenido']
        publicacion.fecha = datetime.utcnow()
    if 'tipo' in data:
        tipo = data['tipo']
        if tipo in ['queja', 'educativo']:
            publicacion.tipo = tipo
        else:
            return jsonify({'error': 'El tipo de publicación debe ser "queja" o "educativo"'}), 400
    if 'imageurl' in data:
        publicacion.imageurl = data['imageurl']

    db.session.commit()
    return jsonify({'mensaje': 'Publicación actualizada correctamente', 'id': publicacion.id}), 200

@publicaciones.route('/publicaciones/<int:publicacion_id>', methods=['DELETE'])
@jwt_required()
def eliminar_publicacion(publicacion_id):
    user_id = get_jwt_identity()
    publicacion = Publicacion.query.get(publicacion_id)
    if not publicacion:
        return jsonify({'error': 'Publicación no encontrada'}), 404

    if publicacion.usuario_id == user_id:
        return jsonify({'error': 'No puedes eliminar esta publicación'}), 403

    db.session.delete(publicacion)
    db.session.commit()
    return jsonify({'mensaje': 'Publicación eliminada correctamente'}), 200
from flask import Flask
from config import init_app, db
from routes.login import acceso
from routes.centros_reciclaje import centros_reciclaje_bp
from routes.ranking import ranking_bp
from routes.seguimiento_reportes import seguimiento_reportes_bp  # Importar el blueprint de seguimiento_reportes
from routes.publicaciones import  publicaciones
from routes.comentarios import comentarios
from routes.reacciones import reacciones
from routes.datos_personales import datos_personales_new_bp

app = Flask(__name__)

init_app(app)

app.register_blueprint(acceso)
app.register_blueprint(centros_reciclaje_bp)
app.register_blueprint(ranking_bp)
app.register_blueprint(seguimiento_reportes_bp)  # Registrar el blueprint con prefijo /api
app.register_blueprint(publicaciones)
app.register_blueprint(comentarios)
app.register_blueprint(reacciones)
app.register_blueprint(datos_personales_new_bp)

with app.app_context():
    db.create_all()  # Esto asegura que todas las tablas se creen si es necesario

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask
from config import init_app, db
from routes.login import acceso
from routes.centros_reciclaje import centros_reciclaje_bp
from routes.ranking import ranking_bp  # Importar el blueprint de ranking

app = Flask(__name__)

init_app(app)

app.register_blueprint(acceso)
app.register_blueprint(centros_reciclaje_bp)
app.register_blueprint(ranking_bp)  # Registrar el blueprint con prefijo /api

with app.app_context():
    db.create_all()  # Esto asegura que todas las tablas se creen si es necesario

if __name__ == "__main__":
    app.run(debug=True)
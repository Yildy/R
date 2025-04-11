from flask import Flask
from config import init_app, db
from routes.login import acceso

app=Flask(__name__)

init_app(app)


app.register_blueprint(acceso)

with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)
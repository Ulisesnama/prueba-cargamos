"""Configuración de la aplicación"""

# Flask
from flask import Flask

# Aplicación
from config import Config
from database import db

# Api
from apis import api 


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

api.init_app(app)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
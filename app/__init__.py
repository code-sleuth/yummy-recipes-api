from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# initialize sql-alchemy
db = SQLAlchemy()


def set_app():
    from app.models import User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_APP'] = "main_app.py"
    app.config['SECRET'] = "i wont tell if you do not"
    app.config['APP_SETTINGS'] = "development"
    app.config['DATABASE_URL'] = "postgres://postgres:@localhost/flask-api"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:@localhost/flask-api"
    db.init_app(app)

    return app




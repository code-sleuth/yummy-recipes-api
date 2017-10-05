from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, json

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
    app.config['TESTING'] = True
    db.init_app(app)

    @app.route('/users/', methods=['POST', 'GET'])
    def users():
        if request.method == "POST":
            username = str(request.data.get('username', ''))
            fullname = str(request.data.get('fullname', ''))
            password = str(request.data.get('password', ''))
            if username and fullname and password:
                user = User(username, fullname, password)
                user.save()
                response = {
                    'id': user.id,
                    'username': user.username,
                    'fullname': user.fullname,
                    'password': user.password
                }
                response = json.dumps(response)
                return response, 201
        else:

            users = User.get_all_users()
            results = []

            for user in users:
                obj = {
                    'id': user.id,
                    'username': user.username,
                    'fullname': user.fullname,
                    'password': user.password
                }
                results.append(obj)

            response = jsonify(results)
            response.status.code = 200
            return response

    @app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def edit_by_id(id, **kwargs):
        user = User.query.filter_by(id=id).first()
        if not user:
            # abort
            abort(404)

        if request.method == 'DELETE':
            user.delete()
            return {
                "message": "users {} deleted".format(user.id)
            }, 200

        elif request.method == "PUT":
            username = str(request.data.get('username', ''))
            user.username = username
            user.save()
            response = jsonify({
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname,
                'password': user.password
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname,
                'password': user.password
            })
            response.status_code = 200
            return response

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app




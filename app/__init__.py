from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, json, make_response

# initialize sql-alchemy
db = SQLAlchemy()


def set_app():
    from app.models import User, Category, Recipe
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_APP'] = "main_app.py"
    app.config['SECRET'] = "i wont tell if you do not"
    app.config['APP_SETTINGS'] = "development"
    app.config['DATABASE_URL'] = "postgres://postgres:@localhost/flask_api"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:@localhost/flask_api"
    app.config['TESTING'] = True
    db.init_app(app)

    @app.route('/users', methods=['POST', 'GET'])
    def users():
        if request.method == "POST":
            username = str(request.data.get('username'))
            fullname = str(request.data.get('fullname'))
            password = str(request.data.get('password'))
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
                    'fullname': user.fullname
                }
                results.append(obj)

            response = json.dumps(results)
            return response, 200

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
            username = str(request.data.get('username'))
            user.username = username
            user.save()
            response = jsonify({
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname
            })
            response.status_code = 200
            return response

    # import the authentication blueprints and register them on the app
    from .auth import auth_blueprint
    from .category_blue_print import category_blue_print
    from .recipe_blue_print import recipe_blue_print
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(category_blue_print)
    app.register_blueprint(recipe_blue_print)

    return app




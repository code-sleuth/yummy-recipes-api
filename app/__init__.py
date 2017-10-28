from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, json, redirect, Flask, make_response
from flasgger import Swagger
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def set_app(config_name):
    from app.models import User, Category, Recipe
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../instance/config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SWAGGER'] = {
        'swagger': '2.0',
        'title': 'yummy-recipes-api',
        'description': "The innovative yummy recipes app is an application that allows\
        users to create, save and share meeting the needs of keeping track of awesome food recipes.\
        \nThis is a RESTful API built in python using the Flask Framework.",
        'basePath': '/',
        'version': '0.1.0',
        'contact': {
            'Developer': 'Ibrahim Mbaziira',
            'email': 'code.ibra@gmail.com',
            'Company': 'Andela'
        },
        'schemes': [
            'http',
            'https'
        ],
        'license': {
            'name': 'MIT'
        },
        'tags': [
            {
                'name': 'User',
                'description': 'The basic unit of authentication'
            },
            {
                'name': 'Category',
                'description': 'Categories help to group recipes that belong together'
            },
            {
                'name': 'Recipe',
                'description': 'A food recipe with certain details and ingredients'
            },
        ],
        'specs_route': '/swagger_docs/'
    }

    db.init_app(app)
    swagger = Swagger(app)

    @app.route('/users', methods=['POST', 'GET'])
    def users():
        if request.method == "POST":
            posted_data = request.get_json(force=True)
            username = str(posted_data['username'])
            fullname = str(posted_data['fullname'])
            password = str(posted_data['password'])
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
    def edit_by_id(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        if request.method == 'DELETE':
            user.delete()
            return make_response(jsonify({
                "message": "users {} deleted".format(user.id)
            })), 200

        elif request.method == "PUT":
            put_data = request.get_json(force=True)
            username = str(put_data['username'])
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
            response = make_response(jsonify({
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname
            })), 200
            return response

    # index
    @app.route('/')
    def index():
        return redirect('/swagger_docs/')

    # import the authentication blueprints and register them on the app
    from .auth import auth_blueprint
    from .category_blue_print import category_blue_print
    from .recipe_blue_print import recipe_blue_print
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(category_blue_print)
    app.register_blueprint(recipe_blue_print)

    return app




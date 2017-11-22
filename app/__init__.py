from flask_sqlalchemy import SQLAlchemy
from flask import redirect, Flask
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
        \nThis is a RESTful API built in python using the Flask Framework.\
        \n GitHub Repository: 'https://github.com/code-sleuth/yummy-recipes-api'",
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

    # index
    @app.route('/')
    def index():
        return redirect('/swagger_docs/')

    # import the authentication blueprints and register them on the app
    from .auth import auth_blueprint
    from .users_blue_print import users_blue_print
    from .category_blue_print import category_blue_print
    from .recipe_blue_print import recipe_blue_print
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blue_print)
    app.register_blueprint(category_blue_print)
    app.register_blueprint(recipe_blue_print)

    return app




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

    @app.route('/categories/', methods=['GET', 'POST'])
    def categories():
        # Get the access token from the header
        access_token = request.headers.get('Authorization')
        # print(request.headers)
        print(access_token)
        if access_token:
            # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            print("user id: ", user_id)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        cat = Category(name=name, created_by=user_id)
                        cat.save()
                        response = {
                            'id': cat.id,
                            'name': cat.name,
                            'date_created': cat.date_created,
                            'date_modified': cat.date_modified,
                            'created_by': user_id
                         }

                        response = json.dumps(response)
                        return response, 201

                else:
                    # GET all the categories created by this user
                    categories = Category.query.filter_by(created_by=user_id)
                    results = []

                    for cat in categories:
                        obj = {
                            'id': cat.id,
                            'name': cat.name,
                            'date_created': cat.date_created,
                            'date_modified': cat.date_modified,
                            'created_by': cat.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/categories/<int:id>', methods=['DELETE', 'PUT', 'GET'])
    def edit_category_by_id(id, **kwargs):
        category = Category.query.filter_by(id=id).first()
        print(category)
        if not category:
            abort(404)

        if request.method == 'DELETE':
            category.delete()
            return {
                "message": "Recipe Category {} Deleted".format(category.id)
            }, 200

        elif request.method == "PUT":
            name = str(request.data.get('name'))
            category.name = name
            category.save()
            response = jsonify({
                'id': category.id,
                'name': category.name,
                'date_created': category.date_created,
                'date_modified': category.date_modified,
                'created_by': category.created_by
            })
            response.status_code = 200
            return response

        else:
            # GET
            response = jsonify({
                'id': category.id,
                'name': category.name,
                'date_created': category.date_created,
                'date_modified': category.date_modified,
                'created_by': category.created_by
            })
            response.status_code = 200
            return response

    @app.route('/recipes', methods=['GET', 'POST'])
    def recipes():
        # Get access token
        access_token = request.headers.get('Authorization')
        if access_token:
            # decode token to get user id
            userid = User.decode_token(access_token)

            # if user id is not a string
            if not isinstance(userid, str):
                # user is authenticated, handle the request
                if request.method == 'POST':
                    category_id = int(request.data.get('category_id'))
                    created_by = int(request.data.get('created_by'))
                    name = str(request.data.get('name'))
                    details = str(request.data.get('details'))
                    ingredients = str(request.data.get('ingredients'))

                    if category_id and created_by and name and details and ingredients:
                        recipe = Recipe(category_id, name, details, ingredients, created_by)
                        print(created_by)
                        recipe.save()

                        response = {
                            'id': recipe.id,
                            'category_id': recipe.category_id,
                            'name': recipe.name,
                            'details': recipe.details,
                            'ingredients': recipe.ingredients,
                            'date_created': recipe.date_created,
                            'date_modified': recipe.date_modified,
                            'created_by': recipe.created_by
                        }

                        response = json.dumps(response)
                        return response, 201
                else:
                    # get all recipes created by this user
                    recipes = Recipe.query.filter_by(created_by=userid)
                    res = []
                    print("here")
                    print(recipes)
                    for recipe in recipes:
                        obj = {
                            'id': recipe.id,
                            'category_id': recipe.category_id,
                            'name': recipe.name,
                            'details': recipe.details,
                            'ingredients': recipe.ingredients,
                            'date_created': recipe.date_created,
                            'date_modified': recipe.date_modified,
                            'created_by': recipe.created_by
                        }
                        res.append(obj)

                    return make_response(jsonify(res)), 201
            else:
                # user authentication failed, so the payload is an error message
                message = userid
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/recipes/<int:id>', methods=['DELETE', 'PUT', 'GET'])
    def edit_recipes(id, **kwargs):
        recipe = Recipe.query.filter_by(id=id).first()

        if not recipe:
            abort(404)

        if request.method == "DELETE":
            recipe.delete()
            return {
                "message": "Recipe {} deleted".format(id)
            }, 200

        elif request.method == "PUT":
            # get values from put request
            category_id = int(request.data.get('category_id'))
            name = str(request.data.get('name'))
            details = str(request.data.get('details'))
            ingredients = str(request.data.get('ingredients'))

            # update database values
            recipe.category_id = category_id
            recipe.name = name
            recipe.details = details
            recipe.ingredients = ingredients

            # save and commit changes
            recipe.save()

            response = {
                'id': recipe.id,
                'category_id': recipe.category_id,
                'name': recipe.name,
                'details': recipe.details,
                'ingredients': recipe.ingredients,
                'date_created': recipe.date_created,
                'date_modified': recipe.date_modified,
                'created_by': recipe.created_by
            }

            response = json.dumps(response)
            return response, 200

        else:
            # GET
            response = {
                'id': recipe.id,
                'category_id': recipe.category_id,
                'name': recipe.name,
                'details': recipe.details,
                'ingredients': recipe.ingredients,
                'date_created': recipe.date_created,
                'date_modified': recipe.date_modified,
                'created_by': recipe.created_by
            }

            response = json.dumps(response)
            return response, 200

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app




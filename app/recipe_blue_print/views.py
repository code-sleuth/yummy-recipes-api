from . import recipe_blue_print

from flask import make_response, request, jsonify, json, abort
from app.auth.views import get_authenticated_user
from app.models import Recipe


def recipes_view():
    # Check whether user has appropriate access rights
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"}))

    if request.method == 'POST':
        post_data = request.get_json(force=True)
        category_id = int(post_data['category_id'])
        created_by = int(post_data['created_by'])
        name = str(post_data['name'])
        details = str(post_data['details'])
        ingredients = str(post_data['ingredients'])

        if category_id and created_by and name and details and ingredients:
            recipe = Recipe(category_id, name, details, ingredients, created_by)
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
            return make_response(jsonify({"message": "Failed to add Recipe"}))

    elif request.method == "GET":
        # get all recipes created by this user
        print(user.id)
        recipes = Recipe.query.filter_by(created_by=user.id)
        res = []
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

        return make_response(jsonify(res)), 200
    else:
        return make_response(jsonify({"message": "Bad request"})), 400


def recipes_view_edit(id):
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"}))

    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        abort(404)

    if request.method == "DELETE":
        recipe.delete()
        return make_response(jsonify({"message": "Recipe {} deleted".format(id)})), 200
    elif request.method == "PUT":
        # get values from put request
        update_data = request.get_json(force=True)
        category_id = int(update_data['category_id'])
        name = str(update_data['name'])
        details = str(update_data['details'])
        ingredients = str(update_data['ingredients'])

        # set database values to the new assigned ones
        recipe.category_id = category_id
        recipe.name = name
        recipe.details = details
        recipe.ingredients = ingredients

        # save and commit changes
        recipe.save()

        response = jsonify({
            'id': recipe.id,
            'category_id': recipe.category_id,
            'name': recipe.name,
            'details': recipe.details,
            'ingredients': recipe.ingredients,
            'date_created': recipe.date_created,
            'date_modified': recipe.date_modified,
            'created_by': recipe.created_by
        })
        return response, 200
    elif request.method == "GET":
        # GET
        response = jsonify({
            'id': recipe.id,
            'category_id': recipe.category_id,
            'name': recipe.name,
            'details': recipe.details,
            'ingredients': recipe.ingredients,
            'date_created': recipe.date_created,
            'date_modified': recipe.date_modified,
            'created_by': recipe.created_by
        })
        return response, 200
    else:
        return make_response(jsonify({"message": "Invalid request"})), 405


def search_by_name(name):
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"})), 403

    recipe_by_name = Recipe.query.filter(Recipe.name.like('%'+name+'%')).all()
    if not recipe_by_name:
        abort(404)

    if request.method == "GET":
        obj = []
        for recipe in recipe_by_name:
            rec = {
                'id': recipe.id,
                'category_id': recipe.category_id,
                'name': recipe.name,
                'details': recipe.details,
                'ingredients': recipe.ingredients,
                'date_created': recipe.date_created,
                'date_modified': recipe.date_modified,
                'created_by': recipe.created_by
            }
            obj.append(rec)
        if not obj:
            return make_response(jsonify({"message": "Empty result set"}))
        return make_response(jsonify(obj)), 200


def get_using_pagination(limit):
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"})), 403

    paginated = Recipe.query.paginate(per_page=limit, error_out=True)
    if not paginated:
        abort(404)

    if request.method == "GET":
        obj = []
        for recipe in paginated.items:
            rec = {
                'id': recipe.id,
                'category_id': recipe.category_id,
                'name': recipe.name,
                'details': recipe.details,
                'ingredients': recipe.ingredients,
                'date_created': recipe.date_created,
                'date_modified': recipe.date_modified,
                'created_by': recipe.created_by,
                'page_number': paginated.page
            }
            obj.append(rec)
        if not obj:
            return make_response(jsonify({"message": "Empty result set"}))
        return make_response(jsonify(obj)), 200


# Define the rule for recipes url ---> /recipes
recipe_blue_print.add_url_rule('/recipes', view_func=recipes_view, methods=['POST', 'GET'])
# Define the rule for recipes url ---> /recipes/<int:id>
recipe_blue_print.add_url_rule('/recipes/<int:id>', view_func=recipes_view_edit, methods=['DELETE', 'PUT', 'GET'])
# Define the rule for recipes url ---> /recipes/<string:name>
recipe_blue_print.add_url_rule('/recipes/<string:name>', view_func=search_by_name, methods=['GET'])
# Define the rule for recipes url ---> /recipes/pages/<int:limit>
recipe_blue_print.add_url_rule('/recipes/pages/<int:limit>', view_func=get_using_pagination, methods=['GET'])


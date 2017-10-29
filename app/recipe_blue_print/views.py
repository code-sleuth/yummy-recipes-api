from . import recipe_blue_print

from flask import make_response, request, jsonify, abort
from app.auth.views import get_authenticated_user
from app.models import Recipe
from flasgger import swag_from


@swag_from('swagger_docs/post_recipe.yaml', methods=['POST'])
@swag_from('swagger_docs/get_all_recipes_by_current_user.yaml', methods=['GET'])
def recipes_view():
    # Check whether user has appropriate access rights
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"})), 403

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
            return make_response(jsonify(response)), 201
        else:
            return make_response(jsonify({"message": "Failed to add Recipe"}))

    elif request.method == "GET":
        try:
            # get request params
            limit = request.args.get('limit') or 20
            page = request.args.get('page') or 1

            limit = int(limit)
            page = int(page)
            # get all recipes created by this user
            recipes = Recipe.query.filter_by(created_by=user.id).paginate(per_page=limit, page=page, error_out=False)
            res = []
            for recipe in recipes.items:
                obj = {
                    'id': recipe.id,
                    'category_id': recipe.category_id,
                    'name': recipe.name,
                    'details': recipe.details,
                    'ingredients': recipe.ingredients,
                    'date_created': recipe.date_created,
                    'date_modified': recipe.date_modified,
                    'created_by': recipe.created_by,
                    'per_page': recipes.per_page,
                    'page_number': recipes.page,
                    'total_items_returned': recipes.total
                }
                res.append(obj)
            if res:
                return make_response(jsonify(res)), 200
            else:
                return make_response(jsonify({
                    'message': 'No Items On This Page',
                    'per_page': recipes.per_page,
                    'page_number': recipes.page,
                    'total_items_returned': recipes.total
                })), 200
        except Exception:
            return make_response(jsonify({'message': 'limit and page cannot be string values'})), 400
    else:
        return make_response(jsonify({"message": "Bad request"})), 400


@swag_from('swagger_docs/delete_recipe_by_id.yaml', methods=['DELETE'])
@swag_from('swagger_docs/get_recipe_by_id.yaml', methods=['GET'])
@swag_from('swagger_docs/put_recipe_by_id.yaml', methods=['PUT'])
def recipes_view_edit(id):
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"})), 403

    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        return make_response(jsonify({'message': 'Recipe Not Found'})), 404

    if request.method == "DELETE":
        recipe.delete()
        return make_response(jsonify({"message": "Recipe with [ID: {}] deleted".format(id)})), 200
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
        return make_response(response), 200
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
        return make_response(response), 200
    else:
        return make_response(jsonify({"message": "Page not Found"})), 404


@swag_from('swagger_docs/search_current_user_recipes.yaml', methods=['GET'])
def search_by_name():
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"})), 403

    if request.method == "GET":
        try:
            # get params
            q = request.args.get('q') or " "
            limit = request.args.get('limit') or 20
            page = request.args.get('page') or 1

            q = str(q)
            limit = int(limit)
            page = int(page)

            recipe_by_name = Recipe.query.filter_by(created_by=user.id).filter(Recipe.name.like('%' + q + '%'))\
                .paginate(per_page=limit, page=page, error_out=False)
            if not recipe_by_name:
                abort(404)
            obj = []
            for recipe in recipe_by_name.items:
                rec = {
                    'id': recipe.id,
                    'category_id': recipe.category_id,
                    'name': recipe.name,
                    'details': recipe.details,
                    'ingredients': recipe.ingredients,
                    'date_created': recipe.date_created,
                    'date_modified': recipe.date_modified,
                    'created_by': recipe.created_by,
                    'per_page': recipe_by_name.per_page,
                    'page_number': recipe_by_name.page,
                    'total_items_returned': recipe_by_name.total
                }
                obj.append(rec)
            if not obj:
                return make_response(jsonify({
                    'message': 'No Content On This Page or Search Not Found',
                    'per_page': recipe_by_name.per_page,
                    'page_number': recipe_by_name.page,
                    'total_items_returned': recipe_by_name.total
                }))
            return make_response(jsonify(obj)), 200
        except Exception:
            return make_response(jsonify({'message': 'limit and page cannot be string values'})), 400

# Define the rule for recipes url ---> /recipes or /recipes?limit=<int:limit>&page=<int:page>
recipe_blue_print.add_url_rule('/recipes', view_func=recipes_view, methods=['POST', 'GET'])
# Define the rule for recipes url ---> /recipes/<int:id>
recipe_blue_print.add_url_rule('/recipes/<int:id>', view_func=recipes_view_edit, methods=['DELETE', 'PUT', 'GET'])
# Define the rule for recipes url ---> /recipes/search?q=<sting:q>&limit=<int:limit>&page=<int:page>'
recipe_blue_print.add_url_rule('/recipes/search', view_func=search_by_name, methods=['GET'])


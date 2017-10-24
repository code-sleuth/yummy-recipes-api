from . import category_blue_print

from flask import make_response, request, jsonify, json, abort
from app.auth.views import get_authenticated_user
from app.models import Category


def categories_view():
    # Check whether user has appropriate access rights
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"})), 403

    if request.method == "POST":
        post_data = request.get_json(force=True)
        name = str(post_data['name'])
        if name:
            cat = Category(name=name, created_by=user.id)
            cat.save()
            response = {
                'id': cat.id,
                'name': cat.name,
                'date_created': cat.date_created,
                'date_modified': cat.date_modified,
                'created_by': user.id
            }

            response = json.dumps(response)
            return response, 201
        else:
            error = jsonify({
                "message": "Name can not be a null string"
            })
            return error, 403

    elif request.method == "GET":
        # GET all the categories created by this user
        categories = Category.query.filter_by(created_by=user.id)
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


def categories_view_edit(id):
    # Check whether user has appropriate access rights
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({"message": "You have no access rights"})), 403

    category = Category.query.filter_by(id=id).first()
    if not category:
        abort(404)

    if request.method == 'DELETE':
        category.delete()
        return make_response(jsonify({
                   "message": "Recipe Category {} Deleted".format(category.id)
               })), 200

    elif request.method == "PUT":
        post_data = request.get_json(force=True)
        name = str(post_data['name'])
        if not name:
            return make_response(jsonify({"message": "name cannot be a null value"})), 403
        category.name = name
        if category.save():
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
            return make_response(jsonify({"message": "Failed to update category"}))

    elif request.method == "GET":
        response = jsonify({
            'id': category.id,
            'name': category.name,
            'date_created': category.date_created,
            'date_modified': category.date_modified,
            'created_by': category.created_by
        })
        return response, 200
    else:
        return make_response(jsonify({"message": "invalid request"}), 405)


# Define the rule for the categories url --->  /categories/
category_blue_print.add_url_rule('/categories', view_func=categories_view, methods=['POST', 'GET'])
# Define the rule for the categories url --->  /categories/<int:id>
category_blue_print.add_url_rule('/categories/<int:id>', view_func=categories_view_edit, methods=['DELETE', 'PUT', 'GET'])

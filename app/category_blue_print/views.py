from . import category_blue_print

from flask import make_response, request, jsonify, json, abort
from app.auth.views import get_authenticated_user
from app.models import Category
from flasgger import swag_from


@swag_from('swagger_docs/post_category.yaml', methods=['POST'])
@swag_from('swagger_docs/get_all_categories.yaml', methods=['GET'])
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
            return make_response(jsonify({
                'id': cat.id,
                'name': cat.name,
                'date_created': cat.date_created,
                'date_modified': cat.date_modified,
                'created_by': user.id
            })), 201

        else:
            error = jsonify({
                "message": "Name can not be a null string OR You are logged out"
            })
            return error, 401
    # get all categories
    elif request.method == "GET":
        try:
            limit = request.args.get('limit') or 20
            page = request.args.get('page') or 1

            limit = int(limit)
            page = int(page)

            # GET all the categories created by this user
            categories = Category.query.paginate(per_page=limit, page=page, error_out=False)
            results = []

            for cat in categories.items:
                obj = {
                    'id': cat.id,
                    'name': cat.name,
                    'date_created': cat.date_created,
                    'date_modified': cat.date_modified,
                    'created_by': cat.created_by,
                    'per_page': categories.per_page,
                    'page_number': categories.page,
                    'total_items_returned': categories.total
                }
                results.append(obj)

            if results:
                return make_response(jsonify(results)), 200
            else:
                return make_response(jsonify({
                    'message': 'No Content On This Page',
                    'per_page': categories.per_page,
                    'page_number': categories.page,
                    'total_items_returned': categories.total
                })), 200
        except Exception:
            return make_response(jsonify({'message': 'limit and page cannot be string values'})), 400


@swag_from('swagger_docs/put_category_by_id.yaml', methods=['PUT'])
@swag_from('swagger_docs/delete_category_by_id.yaml', methods=['DELETE'])
@swag_from('swagger_docs/get_category_by_id.yaml', methods=['GET'])
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


@swag_from('swagger_docs/search_categories.yaml', methods=['GET'])
def search_category():
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({'message': 'you have no access rights'})), 403

    if request.method == 'GET':
        name = request.args.get('q') or " "
        limit = request.args.get('limit') or 20
        page = request.args.get('page') or 1
        try:
            name = str(name)
            limit = int(limit)
            page = int(page)

            categories = Category.query.filter(Category.name.like('%' + name + '%')) \
                .paginate(per_page=limit, page=page, error_out=False)
            if not categories:
                abort(404)

            obj = []
            for category in categories.items:
                cat_obj = {
                    'id': category.id,
                    'name': category.name,
                    'date_created': category.date_created,
                    'date_modified': category.date_modified,
                    'created_by': category.created_by,
                    'per_page': categories.per_page,
                    'page_number': categories.page,
                    'total_items_returned': categories.total
                }
                obj.append(cat_obj)
            if obj:
                return make_response(jsonify(obj)), 200
            else:
                return make_response(jsonify({
                    'message': 'No Content On This Page or Search Not Found',
                    'limit_per_page': categories.per_page,
                    'page_number': categories.page,
                    'total_items_returned': categories.total
                })), 200
        except Exception:
            return make_response(jsonify({'message': 'limit and page cannot be string values'})), 400

# Define the rule for the categories url --->  /categories or /categories?limit=<int:limit>&page=<int:page>
category_blue_print.add_url_rule('/categories', view_func=categories_view, methods=['POST', 'GET'])
# Define the rule for the categories url --->  /categories/<int:id>
category_blue_print.add_url_rule('/categories/<int:id>', view_func=categories_view_edit, methods=['DELETE', 'PUT', 'GET'])
# Define the rule for the categories url ---> /categories/<string:wild_card>
category_blue_print.add_url_rule('/categories/search', view_func=search_category, methods=['GET'])

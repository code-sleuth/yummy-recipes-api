from . import users_blue_print

from flask import make_response, jsonify, request, abort
from app.auth.views import get_authenticated_user
from app.models import User
from flasgger import swag_from
from werkzeug.security import generate_password_hash


@swag_from('swagger_docs/get_all_users.yaml', methods=['GET'])
def users():
    if request.method == 'GET':
        user = get_authenticated_user(request)
        if not user:
            return make_response(jsonify({'message': 'you have no access rights'})), 403
        try:
            # get request params
            limit = request.args.get('limit') or 20
            page = request.args.get('page') or 1

            limit = int(limit)
            page = int(page)
            users = User.query.paginate(
                per_page=limit, page=page, error_out=False)

            results = []
            for user in users.items:
                obj = {
                    'id': user.id,
                    'username': user.username,
                    'fullname': user.fullname,
                    'per_page': users.per_page,
                    'page_number': users.page,
                    'total_items_returned': users.total
                }
                results.append(obj)
            if results:
                return make_response(jsonify(results)), 200
            else:
                return make_response(jsonify({
                    'message': 'No Items On This Page',
                    'per_page': users.per_page,
                    'page_number': users.page,
                    'total_items_returned': users.total
                })), 200
        except Exception:
            return make_response(jsonify({'message': 'limit and page cannot be string values'})), 400


@swag_from('swagger_docs/put_user_by_id.yaml', methods=['PUT'])
@swag_from('swagger_docs/delete_user_by_id.yaml', methods=['DELETE'])
@swag_from('swagger_docs/get_user_by_id.yaml', methods=['GET'])
def edit_by_id(id):
    user = get_authenticated_user(request)
    if not user:
        return make_response(jsonify({'message': 'you have no access rights'})), 403

    user_data = User.query.filter_by(id=id).first()
    if not user_data:
        abort(404)

    if request.method == 'DELETE':
        user_data.delete()
        return make_response(jsonify({
            "message": "users with [ID: {}] deleted successfully".format(user.id)
        })), 200

    elif request.method == "PUT":
        put_data = request.get_json(force=True)
        if 'old_password' in put_data and 'fullname' in put_data:
            old_password = str(put_data['old_password'])
            new_password = str(put_data['new_password'])
            new_fullname = str(put_data['fullname'])
            if user_data.validate_password(old_password):
                user_data.fullname = new_fullname
                user_data.password = generate_password_hash(new_password)
                user_data.save()
                return make_response(jsonify({'id': user_data.id,
                                              'username': user_data.username,
                                              'fullname': user_data.fullname})), 200
            else:
                return make_response(jsonify({'message': 'Invalid Old Password'})), 401
        elif 'old_password' in put_data and 'new_password' in put_data and 'fullname' not in put_data:
            old_password = str(put_data['old_password'])
            new_password = str(put_data['new_password'])
            if user_data.validate_password(old_password):
                user_data.password = generate_password_hash(new_password)
                user_data.save()
                return make_response(jsonify({'id': user_data.id,
                                              'username': user_data.username,
                                              'fullname': user_data.fullname})), 200
            else:
                return make_response(jsonify({'message': 'Invalid Old Password'})), 401
        else:
            # update just the fullname
            new_fullname = str(put_data['fullname'])
            user_data.fullname = new_fullname
            user_data.save()
            return make_response(jsonify({'id': user_data.id,
                                          'username': user_data.username,
                                          'fullname': user_data.fullname})), 200
    else:
        # GET
        return make_response(jsonify({
            'id': user_data.id,
            'username': user_data.username,
            'fullname': user_data.fullname,
            'password': user_data.password
        })), 200


def get_current_user():
    if request.method == 'GET':
        user = get_authenticated_user(request)
        if not user:
            return make_response(jsonify({'message': 'you have no access rights'})), 403
        else:
            user_info = User.query.filter_by(id=user.id).first()
            if not user_info:
                abort(404)
            else:
                return make_response(jsonify({
                    'id': user_info.id,
                    'username': user_info.username,
                    'fullname': user_info.fullname,
                    'email': user_info.email,
                    'password': user_info.password
                })), 200


users_blue_print.add_url_rule('/users', view_func=users, methods=['GET'])
users_blue_print.add_url_rule(
    '/users/<int:id>', view_func=edit_by_id, methods=['DELETE', 'PUT', 'GET'])
users_blue_print.add_url_rule(
    '/users/info', view_func=get_current_user, methods=['GET'])

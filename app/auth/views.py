from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User, BlackListToken
from flasgger import swag_from


def get_authenticated_user(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        access_token = auth_header
    except (IndexError, ValueError):
        return 'Authorization header is in wrong format.'
    if not access_token:
        return None
    else:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            # user is authenticated so get the user
            user = User.query.get(user_id)
            return user
        elif user_id == 'You are already logged out':
            return user_id
        else:
            return None


#  class to register new user
class RegistrationView(MethodView):
    """document api"""

    @swag_from('swagger_docs/register_user.yaml', methods=['POST'])
    def post(self):
        # Handle POST request for this view. Url ---> /auth/register"""
        # Query to see if the user already exists
        post_data = request.get_json(force=True)
        # check if posted username is already in the database
        user = User.query.filter_by(username=post_data['username']).first()
        if not user:
            # There is no user so we'll try to register new user
            try:
                # Register new user
                username = post_data['username']
                fullname = post_data['fullname']
                password = post_data['password']
                user = User(username=username, fullname=fullname, password=password)
                user.save()

                response = {
                    'message': 'User registered successfully.'
                }
                # return user registered successfully message
                return make_response(jsonify(response)), 201
            except Exception as ex:
                # Return error message
                response = {
                    'message': str(ex)
                }
                return make_response(jsonify(response)), 401
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User exists. Login'
            }

            return make_response(jsonify(response)), 202


# class to handle user login and token generation
class LoginView(MethodView):
    @swag_from('swagger_docs/login.yaml', methods=['POST'])
    def post(self):
        # Handle POST request for this view. Url ---> /auth/login
        try:
            post_data = request.get_json(force=True)
            # Get the user object using their username (unique to every user)
            user = User.query.filter_by(username=post_data['username']).first()
            # Try to authenticate the found user using their password
            if user and user.validate_password(post_data['password']):
                # Generate the access token. This will be used as the authorization header
                user_access_token = user.user_generate_token(user.id)
                if user_access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': user_access_token.decode('utf-8')
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid username or password'
                }
                return make_response(jsonify(response)), 401
        except Exception as ex:
            # Create a response containing an string error message
            response = {
                'message': str(ex)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500


class LogoutView(MethodView):
    @swag_from('swagger_docs/logout.yaml', methods=['POST'])
    def post(self):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            res = User.decode_token(auth_token)
            if not isinstance(res, str):
                blacklist_token = BlackListToken(token=auth_token)
                try:
                    blacklist_token.save()
                    response_object = {
                        'status': 'success',
                        'message': 'successfully logged out'
                    }
                    return make_response(jsonify(response_object)), 200
                except Exception as e:
                    response_object = {
                        'status': 'failed from thrown exception',
                        'message': str(e)
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail from instance',
                    'message': 'You are already logged out'
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail from token',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 403


# Define the API resources
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])

# Define the rule for the login url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])

# Define the rule for the logout url --->  /auth/logout
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/logout', view_func=logout_view, methods=['POST'])


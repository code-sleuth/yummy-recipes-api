from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


#  class to register new user
class RegistrationView(MethodView):
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
                'message': 'User exits. Login'
            }

            return make_response(jsonify(response)), 202


# class to handle user login and token generation
class LoginView(MethodView):
    def post(self):
        # Handle POST request for this view. Url ---> /auth/login
        try:
            post_data = request.get_json(force=True)
            print(post_data)
            # Get the user object using their username (unique to every user)
            user = User.query.filter_by(username=post_data['username']).first()
            # Try to authenticate the found user using their password
            if user and user.validate_password(post_data['password']):
                # Generate the access token. This will be used as the authorization header
                user_access_token = user.user_generate_token(user.id)
                if user_access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': user_access_token.decode()
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

# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])

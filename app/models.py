import jwt
import os
from flask import current_app
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
import unicodedata


class User(db.Model):
    """
    class User that represents the user database model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    fullname = db.Column(db.String(50))
    password = db.Column(db.String(500))
    email = db.Column(db.String(256), unique=True)

    recipes = db.relationship(
        'Recipe', backref="users", lazy='dynamic', cascade="all, delete-orphan")
    categories = db.relationship(
        'Category', backref="users", lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, username='', fullname='', password='', email=''):
        self.username = username
        self.fullname = fullname
        self.password = generate_password_hash(password)
        self.email = email

    @staticmethod
    def get_all_users():
        """
        Static function to return all users in the database
        """
        return User.query.all()

    def save(self):
        """save function that commits user instance to be saved to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete user from database
        """
        db.session.delete(self)
        db.session.commit()

    def validate_password(self, password):
        """Function to validate input password
        """
        return check_password_hash(self.password, password)

    def validate_user_email(self, email):
        """ Function to validate provided email address
        """
        try:
            v = validate_email(email)  # validate and get info
            email = v["email"]  # replace with normalized form
            return True
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
            return False

    @staticmethod
    def is_number(username):
        """function to check if provided string is an integer
        """
        try:
            float(username)
            return True
        except ValueError:
            pass

        try:
            unicodedata.numeric(username)
            return True
        except (TypeError, ValueError):
            return False

    def user_generate_token(self, userid):
        """Generate token for user
        """
        try:
            # set up a payload with an expiration date
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': userid
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as ex:
            return str(ex)

    @staticmethod
    def decode_token(token):
        """Function to decode the token
        """
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            is_blacklisted_token = BlackListToken.check_blacklist(
                auth_token=token)
            if is_blacklisted_token:
                return 'Token Blacklisted. Please log in'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            # if the token is expired, return an error string
            return "The token is expired. Login to renew token"
        except jwt.InvalidTokenError:
            # if the token is invalid, return an error string
            return "Invalid token. Login or Register"

    def __repr__(self):
        return "<User: {}>".format(self.username)


class Category(db.Model):
    """class Category that represents the category database model
    """
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    rec = db.relationship('Recipe', backref="categories",
                          lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, name="", created_by=""):
        self.name = name
        self.created_by = created_by

    def new_category(self, name):
        """function to update category name
        """
        self.name = name

    def save(self):
        """function to save category instance
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_categories():
        """static method to return all categories
        """
        return Category.query.all()

    def delete(self):
        """function to delete current category instance
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Category: {}>".format(self.name)


class Recipe(db.Model):
    """class Recipe that represents the recipe database model
    """
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    name = db.Column(db.String(40))
    details = db.Column(db.String(500))
    ingredients = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, category_id='', name='', details='', ingredients='', created_by=''):
        self.category_id = category_id
        self.created_by = created_by
        self.name = name
        self.details = details
        self.ingredients = ingredients

    @staticmethod
    def get_all_recipes():
        """Function to return all the recipes in the database
        """
        return Recipe.query.all()

    def save(self):
        """save function that commits category instance to be saved to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete function to r3move recipe from database
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Recipe: {}>".format(self.name)


class BlackListToken(db.Model):
    """Class to blacklist expired tokens
    """
    __tablename__ = 'blacklist_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(
        db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        self.token = token

    def save(self):
        """function to save expired token
        """
        db.session.add(self)
        db.session.commit()

    def check_blacklist(auth_token):
        """function to check if token is blacklisted
        """
        # check whether token has been blacklisted
        res = BlackListToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

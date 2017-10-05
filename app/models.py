import jwt
from app import db, set_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


# class User to create user database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    fullname = db.Column(db.String(50))
    password = db.column(db.String(500))

    recipes = db.relationship('Recipe', backref="users", lazy='dynamic')
    categories = db.relationship('Category', backref="users", lazy='dynamic')

    def __init__(self, username, fullname, password):
        self.username = username
        self.fullname = fullname
        self.password = generate_password_hash(password)

    @staticmethod
    def get_all_users():
        return User.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    # generate token for user
    def user_generate_token(self, userid):
        try:
            # set up a payload with an expiration date
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=3),
                'iat': datetime.utcnow(),
                'sub': userid
            }

            jwt_string = jwt.encode(
                payload,
                set_app().config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as ex:
            return str(ex)

    # decode the token
    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, app.config.get('SECRET'))
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
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    rec = db.relationship('Recipe', backref="categories", lazy='dynamic')

    def __init__(self):
        pass

    def new_category(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    name = db.Column(db.String(40))
    details = db.Column(db.String(500))
    ingredients = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, category_id='', user_id='', name='', details='', ingredients=''):
        self.category_id = category_id
        self.user_id = user_id
        self.name = name
        self.details = details
        self.ingredients = ingredients

    def new_recipe(self, category_id, user_id, name, details, ingredients):
        self.category_id = category_id
        self.user_id = user_id
        self.name = name
        self.details = details
        self.ingredients = ingredients

    @staticmethod
    def get_all_recipes():
        return Recipe.query.all()

    def save(self):
        db.session.save(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

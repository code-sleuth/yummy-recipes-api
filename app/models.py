from app import db


# class User to create user database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    fullname = db.Column(db.String(50))
    password = db.column(db.String(50))

    recipes = db.relationship('Recipe', backref="users")

    def __init__(self):
        pass

    def new_user(self, username, fullname, password):
        self.username = username
        self.fullname = fullname
        self.password = password

    @staticmethod
    def get_all_users():
        return User.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self._name)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    recipes = db.relationship('Recipe', backref="categories")

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(40))
    details = db.Column(db.String(500))
    ingredients = db.Column(db.String(200))

    def __init__(self):
        pass

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

import unittest
import json
from app import set_app, db


# Test cases for the authentication blueprint
class AuthTestCase(unittest.TestCase):
    # Set up test variables
    def setUp(self):
        self.app = set_app(config_name='testing')
        # initialize the test client
        self.client = self.app.test_client

        with self.app.app_context():
            # This is the user test json data with a predefined username and password
            self.user_details = {
                'username': 'xcode',
                'fullname': 'john dow',
                'password': 'pass',
                'email': 'code.ibra@gmail.com'
            }

            self.user_login = {
                'username': 'xcode',
                'password': 'pass'
            }

            self.category_details = {
                'name': 'Rice Category'
            }

            self.category_update_data = {
                'name': 'Rice More Category'
            }

            self.recipe_details = {
                'created_by': 1,
                'category_id': 1,
                'name': "recipe one",
                'details': 'lots of spice',
                'ingredients': 'everything'
            }
            self.update_recipe = {
                'category_id': 1,
                'name': "recipe one and another one",
                'details': 'lots of spicy meats',
                'ingredients': 'everything and all'
            }
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

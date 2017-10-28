import unittest
import json
from app import set_app, db


# test  user class
class UserTest(unittest.TestCase):
    def setUp(self):
        # initialize app.
        # define test variables
        self.app = set_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {'username': 'xcode', 'fullname': 'ibrahim mbaziira', 'password': 'pass'}

        # bind app to current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_new_user(self, username='ibm', fullname='jon dow', password='123'):
        user_info = {
            'username': username,
            'fullname': fullname,
            'password': password
        }
        return self.client().post('/auth/register', data=json.dumps(user_info))

    def user_login(self, username='ibm', password='123'):
        user_info = {
            'username': username,
            'password': password
        }
        return self.client().post('/auth/login', data=json.dumps(user_info))

    def test_user_creation(self):
        # Test that the API can create a user (POST request)
        # register a test user, then log them in
        self.register_new_user()
        result = self.user_login()
        self.assertEqual(result.status_code, 200)
        # ensure the request has an authorization header set with the access token in it
        res = self.client().post('/users', data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        self.assertIn('xcode', str(res.data))

    def test_create_users_table(self):
        self.register_new_user()
        result = self.user_login()
        res = self.client().post('/users', data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        self.assertIn('xcode', str(res.data))

    def test_api_get_all_users(self):
        # GET request test
        self.register_new_user()
        result = self.user_login()
        self.assertEqual(result.status_code, 200)
        res = self.client().post('/users', data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/users', data=json.dumps(self.user))
        self.assertEqual(res.status_code, 200)
        self.assertIn('xcode', str(res.data))

    def test_api_get_user_by_id(self):
        # get user by id
        self.register_new_user()
        result = self.user_login()
        self.assertEqual(result.status_code, 200)
        res = self.client().post('/users', data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        result = self.client().get('/users/2')
        self.assertEqual(result.status_code, 200)
        self.assertIn('xcode', str(result.data))

    def test_user_can_be_edited(self):
        # PUT request
        self.register_new_user()
        result = self.user_login()
        self.assertEqual(result.status_code, 200)
        res = self.client().post('/users', data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().put('/users/1', data=json.dumps({"username": "new"}))
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/users/1')
        self.assertIn('new', str(result.data))

    def test_user_can_be_deleted(self):
        # DELETE request
        self.register_new_user()
        result = self.user_login()
        self.assertEqual(result.status_code, 200)
        res = self.client().post('/users', data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        dell = self.client().delete('/users/2')
        self.assertEqual(dell.status_code, 200)
        result = self.client().get('/users/2')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        # teardown all initialized variables
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

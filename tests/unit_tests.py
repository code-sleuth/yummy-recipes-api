import unittest
import json
from app import set_app, db


# test  user class
class UserTest(unittest.TestCase):
    def setUp(self):
        # initialize app.
        # define test variables
        self.app = set_app()
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

    def user_login(self, username='ibm', fullname='jon dow', password='123'):
        user_info = {
            'username': username,
            'fullname': fullname,
            'password': password
        }
        return self.client().post('/auth/login', data=json.dumps(user_info))

    def test_user_creation(self):
        # Test that the API can create a user (POST request)
        # register a test user, then log them in
        self.register_new_user()
        result = self.user_login()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        # ensure the request has an authorization header set with the access token in it
        res = self.client().post('/users/', headers=dict(Authorization="Owner " + access_token), data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('xcode', str(res.data))

    def test_create_users_table(self):
        self.register_new_user()
        result = self.user_login()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/users/', headers=dict(Authorization="Owner " + access_token),  data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('xcode', str(res.data))

    def test_api_get_all_users(self):
        # GET request test
        self.register_new_user()
        result = self.user_login()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/users/', headers=dict(Authorization="Owner " + access_token), data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/users/', headers=dict(Authorization="Owner " + access_token), data=self.user)
        self.assertEqual(res.status_code, 200)
        self.assertIn('xcode', str(res.data))

    def test_api_get_user_by_id(self):
        # get user by id
        self.register_new_user()
        result = self.user_login()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/users/', headers=dict(Authorization="Owner " + access_token), data=self.user)
        self.assertEqual(res.status_code, 201)
        res_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/users/2')
        self.assertEqual(result.status_code, 200)
        self.assertIn('xcode', str(result.data))

    def test_user_can_be_edited(self):
        # PUT request
        self.register_new_user()
        result = self.user_login()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/users/', headers=dict(Authorization="Owner " + access_token), data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().put('/users/2', headers=dict(Authorization="Owner " + access_token), data={"username": "xcode"})
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/users/1')
        self.assertIn('ibm', str(result.data))

    def test_user_can_be_deleted(self):
        # DELETE request
        self.register_new_user()
        result = self.user_login()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/users/', headers=dict(Authorization="Owner " + access_token),
                                 data=self.user)
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

if __name__ == "__main__":
    unittest.main()




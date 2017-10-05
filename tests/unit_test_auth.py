import unittest
import json
from app import set_app, db


# Test cases for the authentication blueprint
class AuthTestCase(unittest.TestCase):
    # Set up test variables
    def setUp(self):
        self.app = set_app()
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        self.user_details = {
            'username': 'xcode',
            'fullname': 'john dow',
            'password': 'pass'
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        # Test that user registers successfully.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details))
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "User registered successfully.")
        self.assertEqual(res.status_code, 201)

    def test_existing_user(self):
        # Test that no duplicate users allowed.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details))
        print(res)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/auth/register', data=json.dumps(self.user_details))
        self.assertEqual(second_res.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User exits. Login")

    def test_user_login(self):
        # Test that a registered user can login.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details))
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/login', data=json.dumps(self.user_details))
        print(login_res)
        # get the results in json format
        result = json.loads(login_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], "You logged in successfully.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_unknown_user_login(self):
        # Test non-registered users cannot login.
        # dictionary to represent an unregistered user
        user_not_in_db = {
            'username': 'you',
            'fullname': 'you are',
            'password': 'nope'
        }
        # send a POST request to /auth/login with the invalid data above
        res = self.client().post('/auth/login', data=json.dumps(user_not_in_db))
        # get the result in json
        result = json.loads(res.data.decode())
        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid username or password")

import json
from unit_base_test import AuthTestCase


# Test cases for the authentication blueprint
class AuthTests(AuthTestCase):
    def test_registration(self):
        # Test that user registers successfully.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details),
                                 content_type='application/json')
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertTrue(result['message'] == "User registered successfully.")
        self.assertTrue(res.content_type == 'application/json')
        self.assertEqual(res.status_code, 201)

    def test_existing_user(self):
        # Test that no duplicate users allowed.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 201)
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details),
                                 content_type='application/json')
        self.assertEqual(reg.status_code, 202)
        # get the results returned in json format
        result = json.loads(reg.data.decode())
        self.assertEqual(result['message'], "User exists. Login")

    def test_user_login(self):
        # Test that a registered user can login.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details))
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/login', data=json.dumps(self.user_login),
                                       content_type='application/json')
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
            'password': 'nope'
        }
        # send a POST request to /auth/login with the invalid data above
        res = self.client().post('/auth/login', data=json.dumps(user_not_in_db),
                                 content_type='application/json')
        # get the result in json
        result = json.loads(res.data.decode())
        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid username or password")

    def test_valid_logout(self):
        # test for logout before token expires
        # register user
        res = self.client().post('/auth/register', data=json.dumps(self.user_details),
                                 content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'User registered successfully.')
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login),
                                 content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # logout and blacklist token
        log_out = self.client().post(
            '/auth/logout', headers=dict(Authorization=log_in['access_token']))
        log_out_data = json.loads(log_out.data.decode())
        self.assertEqual(log_out_data['status'], 'success')
        self.assertEqual(log_out_data['message'], 'successfully logged out')
        self.assertEqual(log_out.status_code, 200)

    def test_api_get_all_users(self):
        # GET request test
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details),
                                 content_type='application/json')
        reg_data = json.loads(reg.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')
        self.assertEqual(reg.content_type, 'application/json')
        self.assertEqual(reg.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login),
                                 content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # get all users
        get_users = self.client().get(
            '/users', headers=dict(Authorization=log_in['access_token']))
        self.assertEqual(get_users.status_code, 200)
        self.assertIn('xcode', str(get_users.data))

    def test_get_user_by_id(self):
        # GET request test
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details),
                                 content_type='application/json')
        reg_data = json.loads(reg.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')
        self.assertEqual(reg.content_type, 'application/json')
        self.assertEqual(reg.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login),
                                 content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # get all users
        get_users = self.client().get(
            '/users/1', headers=dict(Authorization=log_in['access_token']))
        self.assertEqual(get_users.status_code, 200)
        self.assertIn('xcode', str(get_users.data))

    def test_user_can_be_edited(self):
        # PUT request
        # GET request test
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details),
                                 content_type='application/json')
        reg_data = json.loads(reg.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')
        self.assertEqual(reg.content_type, 'application/json')
        self.assertEqual(reg.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login),
                                 content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # get all users
        update_user = self.client().put('/users/1', headers=dict(Authorization=log_in['access_token']),
                                        data=json.dumps({"fullname": "new_fullname"}))
        self.assertEqual(update_user.status_code, 200)
        self.assertIn('new_fullname', str(update_user.data))

    def test_user_can_be_deleted(self):
        # DELETE request
        # GET request test
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details),
                                 content_type='application/json')
        reg_data = json.loads(reg.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')
        self.assertEqual(reg.content_type, 'application/json')
        self.assertEqual(reg.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login),
                                 content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # delete user by id
        delete_user = self.client().delete(
            '/users/1', headers=dict(Authorization=log_in['access_token']))
        self.assertEqual(delete_user.status_code, 200)
        self.assertIn('deleted', str(delete_user.data))

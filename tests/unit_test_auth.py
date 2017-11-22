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
                'password': 'pass'
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

    def test_registration(self):
        # Test that user registers successfully.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details), content_type='application/json')
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertTrue(result['message'] == "User registered successfully.")
        self.assertTrue(res.content_type == 'application/json')
        self.assertEqual(res.status_code, 201)

    def test_existing_user(self):
        # Test that no duplicate users allowed.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details), content_type='application/json')
        self.assertEqual(reg.status_code, 202)
        # get the results returned in json format
        result = json.loads(reg.data.decode())
        self.assertEqual(result['message'], "User exists. Login")

    def test_user_login(self):
        # Test that a registered user can login.
        res = self.client().post('/auth/register', data=json.dumps(self.user_details))
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/login', data=json.dumps(self.user_login), content_type='application/json')
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
        res = self.client().post('/auth/login', data=json.dumps(user_not_in_db), content_type='application/json')
        # get the result in json
        result = json.loads(res.data.decode())
        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid username or password")

    def test_valid_logout(self):
        # test for logout before token expires
        # register user
        res = self.client().post('/auth/register', data=json.dumps(self.user_details), content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'User registered successfully.')
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login), content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # logout and blacklist token
        log_out = self.client().post('/auth/logout', headers=dict(Authorization=log_in['access_token']))
        log_out_data = json.loads(log_out.data.decode())
        self.assertEqual(log_out_data['status'], 'success')
        self.assertEqual(log_out_data['message'], 'successfully logged out')
        self.assertEqual(log_out.status_code, 200)

    def test_api_get_all_users(self):
        # GET request test
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details), content_type='application/json')
        reg_data = json.loads(reg.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')
        self.assertEqual(reg.content_type, 'application/json')
        self.assertEqual(reg.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login), content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # get all users
        get_users = self.client().get('/users', headers=dict(Authorization=log_in['access_token']))
        self.assertEqual(get_users.status_code, 200)
        self.assertIn('xcode', str(get_users.data))

    def test_get_user_by_id(self):
        # GET request test
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details), content_type='application/json')
        reg_data = json.loads(reg.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')
        self.assertEqual(reg.content_type, 'application/json')
        self.assertEqual(reg.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login), content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # get all users
        get_users = self.client().get('/users/1', headers=dict(Authorization=log_in['access_token']))
        self.assertEqual(get_users.status_code, 200)
        self.assertIn('xcode', str(get_users.data))

    def test_user_can_be_edited(self):
        # PUT request
        # GET request test
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details), content_type='application/json')
        reg_data = json.loads(reg.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')
        self.assertEqual(reg.content_type, 'application/json')
        self.assertEqual(reg.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login), content_type='application/json')
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
        reg = self.client().post('/auth/register', data=json.dumps(self.user_details), content_type='application/json')
        reg_data = json.loads(reg.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')
        self.assertEqual(reg.content_type, 'application/json')
        self.assertEqual(reg.status_code, 201)
        # login
        log = self.client().post('/auth/login', data=json.dumps(self.user_login), content_type='application/json')
        log_in = json.loads(log.data.decode())
        self.assertEqual(log.status_code, 200)
        self.assertEqual(log_in['message'], 'You logged in successfully.')
        self.assertTrue(log_in['access_token'])
        self.assertEqual(log.content_type, 'application/json')
        # delete user by id
        delete_user = self.client().delete('/users/1', headers=dict(Authorization=log_in['access_token']))
        self.assertEqual(delete_user.status_code, 200)
        self.assertIn('deleted', str(delete_user.data))

    """
    TEST CATEGORY END POINTS
    """

    def test_add_get_update_delete_category(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))
        self.assertEqual(reg_user.status_code, 201)
        reg_data = json.loads(reg_user.data.decode('utf-8'))
        self.assertEqual(reg_data['message'], 'User registered successfully.')

        # login with new user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        self.assertEqual(login.status_code, 200)
        logged_in = json.loads(login.data.decode('utf-8'))
        self.assertEqual(logged_in['message'], 'You logged in successfully.')
        self.assertTrue(logged_in['access_token'])

        # create new category
        post_data = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                       data=json.dumps(self.category_details))
        self.assertEqual(post_data.status_code, 201)

        # get all categories and paginate
        get_category = self.client().get('/categories', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(get_category.status_code, 200)
        get_category_data = json.loads(get_category.data.decode('utf-8'))
        # check for defaults for pagination
        self.assertEqual(get_category_data[0]['per_page'], 20)
        self.assertEqual(get_category_data[0]['page_number'], 1)
        self.assertEqual(get_category_data[0]['total_items_returned'], 1)

        # search category and paginate
        search_category = self.client().get('/categories/search?q=Rice&limit=2&page=1',
                                            headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(search_category.status_code, 200)
        search_category_data = json.loads(search_category.data.decode('utf-8'))
        self.assertEqual(search_category_data[0]['per_page'], 2)
        self.assertEqual(search_category_data[0]['page_number'], 1)
        self.assertEqual(search_category_data[0]['total_items_returned'], 1)

        # update category
        update = self.client().put('/categories/1', headers=dict(Authorization=logged_in['access_token']),
                                   data=json.dumps(self.category_update_data))
        self.assertEqual(update.status_code, 200)

        # delete category
        delete = self.client().delete('/categories/1', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(delete.status_code, 200)

    def test_fail_add_category(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))
        self.assertEqual(reg_user.status_code, 201)
        reg_data = json.loads(reg_user.data.decode())
        self.assertEqual(reg_data['message'], 'User registered successfully.')

        # login with new user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        self.assertEqual(login.status_code, 200)
        logged_in = json.loads(login.data.decode())
        self.assertEqual(logged_in['message'], 'You logged in successfully.')
        self.assertTrue(logged_in['access_token'])

        # fail to create new category
        fail_data = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                       data=json.dumps({'name': ''}))
        self.assertEqual(fail_data.status_code, 401)

        fail_info = json.loads(fail_data.data.decode())
        self.assertEqual(fail_info['message'], 'Name can not be a null string OR You are logged out')

        # fail to update non existent category
        fail_update = self.client().put('/categories/1', headers=dict(Authorization=logged_in['access_token']),
                                   data=json.dumps({'name': ''}))
        self.assertEqual(fail_update.status_code, 404)

        # fail to delete non existent category
        fail_delete = self.client().delete('/categories/1', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(fail_delete.status_code, 404)

        # create new category
        post_data = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                       data=json.dumps(self.category_details))
        self.assertEqual(post_data.status_code, 201)

        # fail to update existing category
        fail_update = self.client().put('/categories/1', headers=dict(Authorization=logged_in['access_token']),
                                   data=json.dumps({'name': ''}))
        self.assertEqual(fail_update.status_code, 403)

        fail_update_info = json.loads(fail_update.data.decode())
        self.assertEqual(fail_update_info['message'], "name cannot be a null value")

        # fail to delete category
        fail_delete = self.client().delete('/categories/', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(fail_delete.status_code, 404)

        """
        TEST RECIPE END POINTS
        """
    def test_add_get_delete_update_recipe(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))
        self.assertEqual(reg_user.status_code, 201)
        reg_data = json.loads(reg_user.data.decode())
        self.assertEqual(reg_data['message'], "User registered successfully.")

        # login with registered user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        self.assertEqual(login.status_code, 200)
        logged_in = json.loads(login.data.decode())
        self.assertEqual(logged_in['message'], 'You logged in successfully.')
        self.assertTrue(logged_in['access_token'])

        # create category
        category = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                      data=json.dumps(self.category_details))
        self.assertEqual(category.status_code, 201)

        # create recipe
        recipe = self.client().post('/recipes', headers=dict(Authorization=logged_in['access_token']),
                                    data=json.dumps(self.recipe_details))
        self.assertEqual(recipe.status_code, 201)

        # get recipe and paginate
        get_recipe = self.client().get('/recipes', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(get_recipe.status_code, 200)
        get_recipe_data = json.loads(get_recipe.data.decode('utf-8'))
        self.assertEqual(get_recipe_data[0]['per_page'], 20)
        self.assertEqual(get_recipe_data[0]['page_number'], 1)
        self.assertEqual(get_recipe_data[0]['total_items_returned'], 1)

        # search for recipe
        search_recipe = self.client().get('recipes/search?q=r&limit=3&page=1',
                                        headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(search_recipe.status_code, 200)
        search_recipe_data = json.loads(search_recipe.data.decode('utf-8'))
        self.assertEqual(search_recipe_data[0]['per_page'], 3)
        self.assertEqual(search_recipe_data[0]['page_number'], 1)
        self.assertEqual(search_recipe_data[0]['total_items_returned'], 1)

        # update recipe
        update_recipe = self.client().put('/recipes/1', headers=dict(Authorization=logged_in['access_token']),
                                          data=json.dumps(self.update_recipe))
        self.assertEqual(update_recipe.status_code, 200)
        update_recipe_data = json.loads(update_recipe.data.decode())
        self.assertEqual(update_recipe_data['name'], 'recipe one and another one')

        # delete recipe
        delete_recipe = self.client().delete('/recipes/1', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(delete_recipe.status_code, 200)
        # try to get deleted recipe
        get_deleted_recipe = self.client().get('/recipes/1', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(get_deleted_recipe.status_code, 404)

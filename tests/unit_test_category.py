import json
from unit_base_test import AuthTestCase

"""
TEST CATEGORY END POINTS
"""


class CategoryTest(AuthTestCase):
    def test_add_category(self):
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

    def test_get_all_categories(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with new user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode('utf-8'))

        # create new category
        post_data = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                       data=json.dumps(self.category_details))
        self.assertEqual(post_data.status_code, 201)

        # get all categories and paginate
        get_category = self.client().get(
            '/categories', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(get_category.status_code, 200)
        get_category_data = json.loads(get_category.data.decode('utf-8'))
        # check for defaults for pagination
        self.assertEqual(get_category_data[0]['per_page'], 5)
        self.assertEqual(get_category_data[0]['page_number'], 1)
        self.assertEqual(get_category_data[0]['total_items_returned'], 1)

    def test_serach_category(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with new user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode('utf-8'))

        # create new category
        post_data = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                       data=json.dumps(self.category_details))

        # search category and paginate
        search_category = self.client().get('/categories/search?q=Rice&limit=2&page=1',
                                            headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(search_category.status_code, 200)
        search_category_data = json.loads(search_category.data.decode('utf-8'))
        self.assertEqual(search_category_data[0]['per_page'], 2)
        self.assertEqual(search_category_data[0]['page_number'], 1)
        self.assertEqual(search_category_data[0]['total_items_returned'], 1)

    def test_update_category(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with new user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode('utf-8'))

        # create new category
        post_data = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                       data=json.dumps(self.category_details))

        # update category
        update = self.client().put('/categories/1', headers=dict(Authorization=logged_in['access_token']),
                                   data=json.dumps(self.category_update_data))
        self.assertEqual(update.status_code, 200)

    def test_delete_category(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with new user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode('utf-8'))

        # create new category
        post_data = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                       data=json.dumps(self.category_details))

        # delete category
        delete = self.client().delete(
            '/categories/1', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(delete.status_code, 200)

    def test_fail_add_category(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with new user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode())

        # fail to create new category
        fail_data = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                       data=json.dumps({'name': ''}))
        self.assertEqual(fail_data.status_code, 401)

        fail_info = json.loads(fail_data.data.decode())
        self.assertEqual(
            fail_info['message'], 'Name can not be a null string OR You are logged out')

        # fail to update non existent category
        fail_update = self.client().put('/categories/1', headers=dict(Authorization=logged_in['access_token']),
                                        data=json.dumps({'name': ''}))
        self.assertEqual(fail_update.status_code, 404)

        # fail to delete non existent category
        fail_delete = self.client().delete(
            '/categories/1', headers=dict(Authorization=logged_in['access_token']))
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
        self.assertEqual(
            fail_update_info['message'], "name cannot be a null value")

        # fail to delete category
        fail_delete = self.client().delete(
            '/categories/', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(fail_delete.status_code, 404)

import json
from unit_base_test import AuthTestCase

"""
TEST RECIPE END POINTS
"""


class RecipeTest(AuthTestCase):
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

    def test_get_recipe(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with registered user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode())

        # create category
        category = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                      data=json.dumps(self.category_details))
        self.assertEqual(category.status_code, 201)

        # create recipe
        recipe = self.client().post('/recipes', headers=dict(Authorization=logged_in['access_token']),
                                    data=json.dumps(self.recipe_details))
        self.assertEqual(recipe.status_code, 201)

        # get recipe and paginate
        get_recipe = self.client().get(
            '/recipes', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(get_recipe.status_code, 200)
        get_recipe_data = json.loads(get_recipe.data.decode('utf-8'))
        self.assertEqual(get_recipe_data[0]['per_page'], 20)
        self.assertEqual(get_recipe_data[0]['page_number'], 1)
        self.assertEqual(get_recipe_data[0]['total_items_returned'], 1)

    def test_search_recipe(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with registered user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode())

        # create category
        category = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                      data=json.dumps(self.category_details))

        # create recipe
        recipe = self.client().post('/recipes', headers=dict(Authorization=logged_in['access_token']),
                                    data=json.dumps(self.recipe_details))

        # search for recipe
        search_recipe = self.client().get('recipes/search?q=r&limit=3&page=1',
                                          headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(search_recipe.status_code, 200)
        search_recipe_data = json.loads(search_recipe.data.decode('utf-8'))
        self.assertEqual(search_recipe_data[0]['per_page'], 3)
        self.assertEqual(search_recipe_data[0]['page_number'], 1)
        self.assertEqual(search_recipe_data[0]['total_items_returned'], 1)

    def test_update_recipe(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with registered user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode())

        # create category
        category = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                      data=json.dumps(self.category_details))

        # create recipe
        recipe = self.client().post('/recipes', headers=dict(Authorization=logged_in['access_token']),
                                    data=json.dumps(self.recipe_details))

        # update recipe
        update_recipe = self.client().put('/recipes/1', headers=dict(Authorization=logged_in['access_token']),
                                          data=json.dumps(self.update_recipe))
        self.assertEqual(update_recipe.status_code, 200)
        update_recipe_data = json.loads(update_recipe.data.decode())
        self.assertEqual(
            update_recipe_data['name'], 'recipe one and another one')

    def test_delete_recipe(self):
        # register user
        reg_user = self.client().post('/auth/register', data=json.dumps(self.user_details))

        # login with registered user
        login = self.client().post('/auth/login', data=json.dumps(self.user_login))
        logged_in = json.loads(login.data.decode())

        # create category
        category = self.client().post('/categories', headers=dict(Authorization=logged_in['access_token']),
                                      data=json.dumps(self.category_details))

        # create recipe
        recipe = self.client().post('/recipes', headers=dict(Authorization=logged_in['access_token']),
                                    data=json.dumps(self.recipe_details))

        # delete recipe
        delete_recipe = self.client().delete(
            '/recipes/1', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(delete_recipe.status_code, 200)
        # try to get deleted recipe
        get_deleted_recipe = self.client().get(
            '/recipes/1', headers=dict(Authorization=logged_in['access_token']))
        self.assertEqual(get_deleted_recipe.status_code, 404)

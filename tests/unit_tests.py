import unittest, json
from app import set_app, db


# test  user class
class UserTest(unittest.TestCase):
    def setUp(self):
        self.app = set_app()
        self.user = {'id': 1, 'username': 'xcode', 'fullname': 'ibrahim mbaziira'}

        with self.app.app_context():
            db.create_all()

    def test_create_users_table(self):
        res = self.post('/users/', data=self.user)
        self.assertEqual(reps.status_code, 201)
        self.assertIn('xcode', str(res.data))

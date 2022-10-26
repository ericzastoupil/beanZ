#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='userguy')
        u.set_password('r34lLyg00dP@$$w0rd')
        self.assertFalse(u.check_password('password123'))
        self.assertTrue(u.check_password('r34lLyg00dP@$$w0rd'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
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
        u1 = User(username='user1')
        u1.set_password('r34lLyg00dP@$$w0rd')
        self.assertFalse(u1.check_password('password123'))
        self.assertTrue(u1.check_password('r34lLyg00dP@$$w0rd'))

    
    '''
    def test_created_on(self):
        creation = datetime.utcnow()
        print("\n[+] Creation: ", creation)
        u2 = User(username='user2')
        print("\n[+] u2.created_on: ", u2.created_on.cast(Date))
        self.assertTrue(creation < u2.created_on.cast(Date))
        self.assertTrue(datetime.utcnow() > datetime(u2.created_on))

    def test_updated_on(self):
        u3 = User(username='user3')
        u3.set_password('password')

        before = u3.updated_on
        u3.set_password('newpassword')
        after = u3.updated_on

        self.assertTrue(before > after)
    '''
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
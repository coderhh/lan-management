import unittest

import datetime

from app.main import db
from app.main.model.account import Account
from app.test.base import BaseTestCase


class TestAccountModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = Account(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = Account.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = Account(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = Account.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(Account.decode_auth_token(auth_token.decode("utf-8") ) == 1)


if __name__ == '__main__':
    unittest.main()


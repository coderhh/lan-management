#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   account.py
@Time    :   2022/08/09 22:18:48
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import datetime
import secrets
from typing import Union

import jwt
from app.main.model.blacklist import BlacklistToken
from app.main.model.refresh_token import RefreshToken

from .. import db, flask_bcrypt
from ..config import key


class Account(db.Model):
    """ Account Model for storing account related details """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(20), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=True)
    password_hash = db.Column(db.String(100))
    refresh_tokens = db.relationship('RefreshToken', cascade="all, delete")

    @property
    def password(self):
        """_summary_

        Raises:
            AttributeError: _description_
        """
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        """_summary_

        Args:
            password (_type_): _description_
        """
        self.password_hash = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """_summary_

        Args:
            password (str): _description_

        Returns:
            bool: _description_
        """
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(account_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp':
                datetime.datetime.now() +
                datetime.timedelta(days=1, seconds=5),
                'iat':
                datetime.datetime.now(),
                'sub':
                account_id
            }
            return jwt.encode(payload, key, algorithm='HS256')
        except jwt.ExpiredSignatureError:
            return jwt.ExpiredSignatureError

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            if auth_token.startswith('Bear'):
                auth_token = auth_token.split(' ')[1]
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def encode_refresh_token(ip_add: str):
        """_summary_

        Args:
            ip (str): _description_

        Returns:
            _type_: _description_
        """
        refresh_token = RefreshToken(token=secrets.token_hex(40),
                                     expires=datetime.datetime.now() +
                                     datetime.timedelta(days=7),
                                     created_at=datetime.datetime.now(),
                                     created_by_ip=ip_add)
        return refresh_token

    @staticmethod
    def remove_old_refresh_token(account: object):
        """_summary_

        Args:
            account (object): _description_

        Returns:
            _type_: _description_
        """
        try:
            token_iterator = filter(
                lambda refresh_token: refresh_token.is_active is True and
                refresh_token.is_expired is False, account.refresh_tokens)
            refresh_tokens = list(token_iterator)
            account.refresh_tokens = refresh_tokens
        except AttributeError:
            return AttributeError

    @staticmethod
    def asdict(class_instance):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {
            'public_id': class_instance.public_id,
            'email': class_instance.email,
            'first_name': class_instance.first_name,
            'last_name': class_instance.last_name,
            'role': class_instance.role
        }

    def __repr__(self):
        return f"<Account '{self.email}'>."

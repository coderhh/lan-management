from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from app.main.model.refresh_token import RefreshToken
from ..config import key
import jwt
from typing import Union
import secrets

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
    refresh_tokens = db.relationship('RefreshToken', backref='account', lazy=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(account_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': account_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
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
    def encode_refresh_token(ip: str):
        refresh_token = RefreshToken(
            token = secrets.token_hex(40),
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=7),
            created_at = datetime.datetime.utcnow(),
            created_by_ip = ip
        )
        return refresh_token
    @staticmethod
    def remove_old_refresh_token(self):
        return ""


    def __repr__(self):
        return "<Account '{}'>".format(self.email)

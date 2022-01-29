from enum import unique
from .. import db
import datetime


class RefreshToken(db.Model):
    """[summary]
     Token Model for storing refresh tokens
    Args:
        db ([type]): [description]
    """
    __tablename__ = 'refresh_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    #is_expired = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by_ip = db.Column(db.String(50), nullable=False)
    replaced_by_token = db.Column(db.String(500), unique=True)
    revoked = db.Column(db.DateTime)
    revoked_by_ip = db.Column(db.String(50))
    #is_active = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    @property
    def is_expired(self):
        return self.expires <= datetime.datetime.utcnow()

    @property
    def is_active(self):
        return (not self.is_expired) and (self.revoked == None)


    def __repr__(self):
        return "<Refresh Token '{}'>".format(self.token)

#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   refresh_token.py
@Time    :   2022/08/10 10:11:09
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import datetime

from .. import db


class RefreshToken(db.Model):
    """[summary]
     Token Model for storing refresh tokens
    Args:
        db ([type]): [description]
    """
    __tablename__ = 'refresh_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by_ip = db.Column(db.String(50), nullable=False)
    replaced_by_token = db.Column(db.String(500), unique=True)
    revoked = db.Column(db.DateTime)
    revoked_by_ip = db.Column(db.String(50))
    account_id = db.Column(db.Integer,
                           db.ForeignKey('account.id'),
                           nullable=True)

    @property
    def is_expired(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.expires <= datetime.datetime.now()

    @property
    def is_active(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return (not self.is_expired) and (self.revoked is None)

    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return f"<Refresh Token '{self.token}'>"

#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   blacklist.py
@Time    :   2022/08/10 09:57:23
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import datetime

from .. import db


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return f'<id: token: {self.token}'

    @staticmethod
    def check_blacklist(auth_token: str) -> bool:
        """_summary_

        Args:
            auth_token (str): _description_

        Returns:
            bool: _description_
        """
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        return bool(res)

#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   blacklist_service.py
@Time    :   2022/08/10 11:09:50
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import datetime
from typing import Dict, Tuple

from app.main import db
from app.main.model.blacklist import BlacklistToken
from app.main.model.refresh_token import RefreshToken
from app.main.util.dto import AuthDto

api = AuthDto.api


def black_list_token(token: str, r_token: str) -> Tuple[Dict[str, str], int]:
    """_summary_

    Args:
        token (str): _description_
        r_token (str): _description_
        ip (str): _description_

    Returns:
        Tuple[Dict[str, str], int]: _description_
    """
    blacklist_token = BlacklistToken(token=token)
    try:
        refresh_token = RefreshToken.query.filter_by(token=r_token).first()

        if refresh_token:
            # revoke refresh token
            #refresh_token.revoked = datetime.datetime.now()
            #refresh_token.revoked_by_ip = ip
            db.session.delete(refresh_token)
            db.session.commit()
            api.logger.info('BLACKED REFRESHTOKEN %s', refresh_token)
        # insert the jwt token
        db.session.add(blacklist_token)
        db.session.commit()
        # remove old jwt token
        old_jwt_tokens = BlacklistToken.query.filter(
            BlacklistToken.blacklisted_on <
            (datetime.datetime.now() - datetime.timedelta(minutes=3))).all()
        for token in old_jwt_tokens:
            api.logger.info('BLACKED TOKEN: %s', token.token)
            db.session.delete(token)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200
    except RuntimeError as e_msg:
        response_object = {'status': 'fail', 'message': e_msg}
        return response_object, 200


def get_all_blacked_token() -> Tuple[Dict[str, str], int]:
    """_summary_

    Returns:
        Tuple[Dict[str, str], int]: _description_
    """
    tokens = BlacklistToken.query.filter().all()
    response_object = {
        'status': 'success',
        'tokens': str(tokens),
        'count': str(len(tokens))
    }
    return response_object, 200

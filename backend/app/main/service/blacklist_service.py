from doctest import FAIL_FAST
from app.main import db
from app.main.model.blacklist import BlacklistToken
from typing import Dict, Tuple
import datetime
from app.main.model.refresh_token import RefreshToken
from app.main.util.dto import AuthDto

api = AuthDto.api

def black_list_token(token: str, r_token: str, ip: str) -> Tuple[Dict[str, str], int]:
    blacklist_token = BlacklistToken(token=token)
    try:
        refresh_token = RefreshToken.query.filter_by(token = r_token).first()
        if refresh_token:
            # revole refresh token
            refresh_token.revoked = datetime.datetime.now()
            refresh_token.revoked_by_ip = ip
        # insert the jwt token
        db.session.add(blacklist_token)
        db.session.commit()
         # remove old jwt token
        old_jwt_tokens = BlacklistToken.query.filter(BlacklistToken.blacklisted_on < (datetime.datetime.now() - datetime.timedelta(minutes=3))).all()
        for token in old_jwt_tokens:
            api.logger.info('BLACKED TOKEN: {}'.format(token.token))
            db.session.delete(token)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 200

def get_all_blacked_token() -> Tuple[Dict[str, str], int]:
    tokens = BlacklistToken.query.filter().all()
    response_object = {
            'status': 'success',
            'tokens': str(tokens),
            'count': str(len(tokens))
        }
    return response_object, 200

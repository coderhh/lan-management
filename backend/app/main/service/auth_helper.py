import datetime
from os import access
import string
from app.main.model.account import Account
from app.main.util.dto import AuthDto
from app.main.model.refresh_token import RefreshToken
from app.main.util.dto import AccountDto
from .blacklist_service import black_list_token, get_all_blacked_token
from typing import Dict, Tuple
from app.main import db

api = AuthDto.api


class Auth:

    @staticmethod
    def login_account(data: Dict[str, str],
                      ip: string) -> Tuple[Dict[str, str], int]:
        try:
            api.logger.info(
                'User {} is trying to login from IP ADDRESS: {}'.format(
                    data.get('email'), ip))
            # fetch the user data
            account = Account.query.filter_by(email=data.get('email')).first()
            if account and account.check_password(data.get('password')):
                # generate Jwt token and refresh token
                auth_token = Account.encode_auth_token(account.id)
                refresh_token = Account.encode_refresh_token(ip)
                account.refresh_tokens.append(refresh_token)
                # remove old refresh token from account
                #Account.remove_old_refresh_token(account)
                db.session.commit()
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'jwtToken': auth_token.decode(),
                        'refreshToken': refresh_token.token
                    }
                    response_object.update(Account.asdict(account))
                    api.logger.info(response_object)
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401
        except Exception as e:
            api.logger.error(e)
            response_object = {'status': 'fail', 'message': 'Try again'}
            return response_object, 500

    @staticmethod
    def logout_account(data: str, refresh_token: str,
                       ip: str) -> Tuple[Dict[str, str], int]:
        if data:
            if " " in data:
                auth_token = data.split(" ")[1]
            else:
                auth_token = data
        else:
            auth_token = ''
        if auth_token:
            resp = Account.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return black_list_token(token=auth_token,
                                        r_token=refresh_token,
                                        ip=ip)
            else:
                response_object = {'status': 'fail', 'message': resp}
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_account(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = Account.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                account = Account.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'account_id': account.id,
                        'email': account.email,
                        'role': account.role,
                        'created_on': str(account.created_on)
                    }
                }
                return response_object, 200
            response_object = {'status': 'fail', 'message': resp}
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401

    @staticmethod
    def refresh_token(token: str, ip: str) -> Tuple[Dict[str, str], int]:
        try:
            account = Account.query.join(RefreshToken).filter(
                RefreshToken.token == token).first()
            if not account:
                api.logger.warning(
                    'invalid refresh token, can not find current account')
                response_object = {
                    'status':
                    'fail',
                    'message':
                    'invalid refresh token, can not find current account'
                }
                return response_object, 401
            new_refresh_token = Account.encode_refresh_token(ip)
            token_iterator = filter(
                lambda refresh_token: refresh_token.token == token,
                account.refresh_tokens)
            refresh_token = list(token_iterator)[0]
            refresh_token.revoked = datetime.datetime.now()
            refresh_token.revoked_by_ip = ip
            refresh_token.replaced_by_token = new_refresh_token.token
            account.refresh_tokens.append(new_refresh_token)
            db.session.commit()
            #Account.remove_old_refresh_token(account)
            #db.session.commit()
            jwt_auth_token = Account.encode_auth_token(account.id)
            api.logger.info('NEW JWT TOKEN: {}'.format(jwt_auth_token))
            response_object = {
                'status': 'success',
                'message': 'Successfully refreshed token.',
                'jwtToken': jwt_auth_token.decode(),
                'refreshToken': new_refresh_token.token
            }
            response_object.update(Account.asdict(account))
            return response_object, 200
        except Exception as e:
            api.logger.error(e)
            response_object = {'status': 'fail', 'message': 'try again'}
            return response_object, 500

    @staticmethod
    def get_all_blacked_token() -> Tuple[Dict[str, str], int]:
        return get_all_blacked_token()

    @staticmethod
    def ip_address(request) -> string:
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        return ip

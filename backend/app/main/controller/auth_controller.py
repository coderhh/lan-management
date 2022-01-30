from ipaddress import ip_address
import re
from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from typing import Dict, Tuple

api = AuthDto.api
account_auth = AuthDto.account_auth


@api.route('/login')
class AccountLogin(Resource):
    """
        Account Login Resource
    """
    @api.doc('account login')
    @api.expect(account_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        # get the post data
        post_data = request.json
        ip = Auth.ip_address(request)
        api.logger.info('User is trying to login from IP ADDRESS: {}'.format(ip))
        return Auth.login_account(data=post_data, ip=ip)



@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout an account')
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        auth_header = request.headers.get('Authorization')
        refresh_token = request.headers.get('RefreshToken')
        ip = Auth.ip_address(request)
        api.logger.info('User is trying to log out from IP ADDRESS: {} with JWT TOKEN: {} and REFRESH TOKEN: {}'.format(ip, auth_header, refresh_token))
        return Auth.logout_account(data = auth_header, refresh_token = refresh_token, ip=ip)

@api.route('/refresh-token')
class RefreshToken(Resource):
    """
    Refresh Token Resource
    """
    @api.doc(security='refresh_token')
    def post(self) -> Tuple[Dict[str, str], int]:
        refresh_token = request.headers.get('RefreshToken')
        ip = Auth.ip_address(request)
        api.logger.info('User is trying to refresh token from IP ADDRESS: {} with {}'.format(ip, refresh_token))
        return Auth.refresh_token(refresh_token, ip)
    # @api.doc('get all blacked token')
    # def get(self) -> Tuple[Dict[str, str], int]:
    #     return Auth.get_all_blacked_token()
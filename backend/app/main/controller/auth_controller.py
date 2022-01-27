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
        return Auth.login_account(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a account')
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_account(data=auth_header)

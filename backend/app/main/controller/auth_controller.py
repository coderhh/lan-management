#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   auth_controller.py
@Time    :   2022/08/09 22:00:29
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

from typing import Dict, Tuple

from app.main.service.auth_helper import Auth
from flask import make_response, request
from flask_restx import Resource

from ..util.dto import AuthDto

api = AuthDto.api
account_auth = AuthDto.account_auth


@api.route('/login')
class AccountLogin(Resource):
    """_summary_

    Args:
        Resource (_type_): _description_

    Returns:
        _type_: _description_
    """

    @api.doc('account login')
    @api.expect(account_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        """_summary_

        Returns:
            Tuple[Dict[str, str], int]: _description_
        """
        post_data = request.json
        ip_ = Auth.ip_address(request)
        result = Auth.login_account(data=post_data, ip=ip_)
        res = make_response(result)
        refresh_token = result[0]['refreshToken']
        res.set_cookie("refreshToken",
                       value=refresh_token,
                       samesite='None',
                       secure=True,
                       httponly=True)
        return res


@api.route('/logout')
class LogoutAPI(Resource):
    """_summary_

    Args:
        Resource (_type_): _description_

    Returns:
        _type_: _description_
    """

    @api.doc('logout an account')
    def post(self) -> Tuple[Dict[str, str], int]:
        """_summary_

        Returns:
            Tuple[Dict[str, str], int]: _description_
        """

        auth_header = request.headers.get('Authorization')
        refresh_token = request.cookies.get('refreshToken')
        ip_ = Auth.ip_address(request)
        api.logger.info(
            'User is trying to log out from IP ADDRESS: %s with JWT TOKEN:'
            '%s and REFRESH TOKEN: %s', ip_, auth_header, refresh_token)
        return Auth.logout_account(data=auth_header,
                                   refresh_token=refresh_token,
                                   ip=ip_)


@api.route('/refresh-token')
class RefreshToken(Resource):
    """Refresh Token

    Args:
        Resource (_type_): _description_

    Returns:
        _type_: _description_
    """

    @api.doc(security='refresh_token')
    def post(self) -> Tuple[Dict[str, str], int]:
        """_summary_

        Returns:
            Tuple[Dict[str, str], int]: _description_
        """
        auth_header = request.headers.get('Authorization')
        refresh_token = request.cookies.get('refreshToken')
        ip_ = Auth.ip_address(request)
        api.logger.info(
            'User is trying to refresh token from IP ADDRESS: %s with'
            'refreshToken: %s and jwtToken: %s', ip_, refresh_token,
            auth_header)
        return make_response(Auth.refresh_token(refresh_token, ip_))

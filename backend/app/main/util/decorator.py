#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   decorator.py
@Time    :   2022/08/11 23:19:50
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import logging
from functools import wraps
from typing import Callable

from app.main.service.auth_helper import Auth
from flask import request

logger = logging.getLogger(__name__)


def token_required(func) -> Callable:
    """_summary_

    Args:
        f (_type_): _description_

    Returns:
        Callable: _description_
    """

    @wraps(func)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_account(request)
        token = data.get('data')

        if not token:
            return data, status

        return func(*args, **kwargs)

    return decorated


def admin_token_required(func: Callable) -> Callable:
    """_summary_

    Args:
        f (Callable): _description_

    Returns:
        Callable: _description_
    """

    @wraps(func)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_account(request)
        token = data.get('data')

        if not token:
            return data, status

        role = token.get('role')

        if role.upper() != 'ADMIN':
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return func(*args, **kwargs)

    return decorated

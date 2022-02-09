from functools import wraps
import logging
from flask import request
from app.main.service.auth_helper import Auth
from typing import Callable

logger= logging.getLogger(__name__)
def token_required(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_account(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_account(request)
        token = data.get('data')

        if not token:
            return data, status

        role = token.get('role')

        if role != 'admin':
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated

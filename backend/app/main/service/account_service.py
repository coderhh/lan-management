#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   account_service.py
@Time    :   2022/08/10 10:19:03
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import datetime
import uuid
from typing import Dict, Tuple

from app.main import db
from app.main.model.account import Account

from ..util.dto import AccountDto

api = AccountDto.api


def save_new_account(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """_summary_

    Args:
        data (Dict[str, str]): _description_

    Returns:
        Tuple[Dict[str, str], int]: _description_
    """
    account = Account.query.filter_by(email=data['email']).first()
    if not account:
        new_account = Account(public_id=str(uuid.uuid4()),
                              email=data['email'],
                              first_name=data['first_name'],
                              last_name=data['last_name'],
                              role=data['role'],
                              password=data['password'],
                              created_on=datetime.datetime.now())
        db.session.add(data)
        db.session.commit()
        return generate_token(new_account)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Account already exists. Please Log in.',
        }
        return response_object, 409


def update_an_account(data: Dict[str, str],
                      public_id) -> Tuple[Dict[str, str], int]:
    """_summary_

    Args:
        data (Dict[str, str]): _description_
        public_id (_type_): _description_

    Returns:
        Tuple[Dict[str, str], int]: _description_
    """
    account = Account.query.filter_by(public_id=public_id).first()
    if account:
        account.email = data['email']
        account.first_name = data['first_name']
        account.last_name = data['last_name']
        account.role = data['role']
        account.password = data['password']
        account.updated_on = datetime.datetime.now()

        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully updated.',
            'account': str(account)
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Account not exists.',
        }
        return response_object, 404


def get_all_accounts():
    """_summary_

    Returns:
        _type_: _description_
    """
    return Account.query.all()


def get_a_account_by_id(public_id):
    """_summary_

    Args:
        public_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    return Account.query.filter_by(public_id=public_id).first()


def delete_a_account(public_id):
    """_summary_

    Args:
        public_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    account = Account.query.filter_by(public_id=public_id).first()
    if account:
        try:
            db.session.delete(account)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully deleted.',
            }
            return response_object, 200
        except RuntimeError:
            response_object = {
                'status': 'fails',
                'message': 'can not delete.',
            }
            return response_object, 500
    else:
        response_object = {
            'status': 'fail',
            'message': 'Account not exists.',
        }
        return response_object, 404


def generate_token(account: Account) -> Tuple[Dict[str, str], int]:
    """_summary_

    Args:
        account (Account): _description_

    Returns:
        Tuple[Dict[str, str], int]: _description_
    """
    try:
        # generate the auth token
        auth_token = Account.encode_auth_token(account.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except RuntimeError:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

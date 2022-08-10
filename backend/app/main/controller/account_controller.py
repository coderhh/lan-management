#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   account_controller.py
@Time    :   2022/08/09 21:56:30
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

from typing import Dict, Tuple

from app.main.util.decorator import admin_token_required
from flask import request
from flask_restx import Resource

from ..service.account_service import (delete_a_account, get_a_account_by_id,
                                       get_all_accounts, save_new_account,
                                       update_an_account)
from ..util.dto import AccountDto

api = AccountDto.api
_account = AccountDto.account


@api.route('/')
class AccountList(Resource):
    """_summary_

    Args:
        Resource (_type_): _description_

    Returns:
        _type_: _description_
    """

    @api.doc('list_of_registered_account')
    @admin_token_required
    @api.marshal_list_with(_account)
    def get(self):
        """List all registered accounts"""
        return get_all_accounts()

    @api.expect(_account, validate=True)
    @api.response(201, 'Account successfully created.')
    @api.doc('create a new account')
    #@admin_token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Account """
        data = request.json

        return save_new_account(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
class Account(Resource):
    """_summary_

    Args:
        Resource (_type_): _description_

    Returns:
        _type_: _description_
    """

    @api.response(404, 'Account not found.')
    @api.doc('get an account')
    @api.marshal_with(_account)
    def get(self, public_id):
        """get an account given its identifier"""
        account = get_a_account_by_id(public_id)
        if not account:
            api.abort(404)
        else:
            return account

    @api.doc('delete an account')
    @admin_token_required
    def delete(self, public_id):
        """delete an account give its identifier"""
        return delete_a_account(public_id)

    @api.expect(_account, validate=True)
    @api.response(200, 'Account successfully updated.')
    @api.doc('update an account')
    @admin_token_required
    def put(self, public_id) -> Tuple[Dict[str, str], int]:
        """Update an Account """
        data = request.json
        return update_an_account(data=data, public_id=public_id)

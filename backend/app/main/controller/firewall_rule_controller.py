#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   firewall_rule_controller.py
@Time    :   2022/08/09 21:57:40
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

from typing import Dict, Tuple

from app.main.util.decorator import admin_token_required, token_required
from flask import request
from flask_restx import Resource

from ..service.firewall_rule_service import (create_new_rule, delete_a_rule,
                                             delete_all_rules,
                                             get_a_rule_by_rule_num,
                                             get_all_rules)
from ..util.dto import FirewallRuleDto

api = FirewallRuleDto.api
_firewall_rule = FirewallRuleDto.firewall_rule


@api.route('/')
class FirewallRuleList(Resource):
    """_summary_

    Args:
        Resource (_type_): _description_

    Returns:
        _type_: _description_
    """

    @api.doc('list_of_firewall_rules')
    @token_required
    @api.marshal_list_with(_firewall_rule)
    def get(self):
        """List all firewall rules"""
        return get_all_rules()

    @api.expect(_firewall_rule, validate=True)
    @api.response(201, 'Firewall rule successfully created.')
    @api.doc('create a new firewall rule')
    @token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a firewall rule """
        data = request.json
        return create_new_rule(data=data)

    @api.doc('delete all rules')
    @admin_token_required
    def delete(self):
        """delete all rules from local databaser"""
        return delete_all_rules()


@api.route('/<rule_num>')
@api.param('rule_num', 'The Rule identifier')
class FirewallRule(Resource):
    """_summary_

    Args:
        Resource (_type_): _description_

    Returns:
        _type_: _description_
    """

    @api.response(404, 'Rule not found.')
    @api.doc('get a rule')
    @api.marshal_with(_firewall_rule)
    @token_required
    def get(self, rule_num):
        """get a rule given its identifier"""
        api.logger.info(rule_num)
        rule = get_a_rule_by_rule_num(rule_num)
        if not rule:
            api.abort(404)
        else:
            return rule

    @api.doc('delete a rule')
    @token_required
    def delete(self, rule_num):
        """delete a rule give its identifier"""
        return delete_a_rule(rule_num)

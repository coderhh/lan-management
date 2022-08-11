#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   dto.py
@Time    :   2022/08/11 23:21:11
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

from flask_restx import Namespace, fields


class AccountDto:
    """_summary_
    """
    api = Namespace('Account', description='account related operations')
    account = api.model(
        'Account', {
            'email':
            fields.String(required=True, description='account email address'),
            'first_name':
            fields.String(required=True, description='account firstname'),
            'last_name':
            fields.String(required=True, description='account lastname'),
            'role':
            fields.String(required=True, description='account role'),
            'password':
            fields.String(required=True, description='account password'),
            'public_id':
            fields.String(description='account identifier')
        })


class AuthDto:
    """_summary_
    """
    api = Namespace('Auth', description='authentication related operations')
    account_auth = api.model(
        'Auth_Details', {
            'email':
            fields.String(required=True, description='The email address'),
            'password':
            fields.String(required=True, description='The user password '),
        })


class VlanBindingDto:
    """_summary_
    """
    api = Namespace('VlanBinding',
                    description='vlan binding related operations')
    vlan_binding = api.model(
        'VlanBinding', {
            'id':
            fields.String(description='binding id'),
            'ip_address':
            fields.String(required=True, description='ip address'),
            'mac_address':
            fields.String(required=True, description='mac address'),
            'network_mask':
            fields.String(required=True, description='network mask'),
            'vlan_id':
            fields.String(required=False, description='vlan id'),
            'created_on':
            fields.String(description='created time'),
        })


class FirewallRuleDto:
    """_summary_
    """
    api = Namespace('FirewallRule',
                    description='firewall rule related operations')
    firewall_rule = api.model(
        'FirewallRule', {
            'ip_address': fields.String(required=True,
                                        description='ip address'),
            'rule_num': fields.String(description='rule number'),
            'vlan_id':
            fields.String(description='vlan id which rule belongs to'),
            'created_on': fields.String(description='created time'),
        })

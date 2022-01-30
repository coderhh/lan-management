from flask_restx import Namespace, fields

class AccountDto:
    api = Namespace('Account',description='account related operations')
    account = api.model('Account', {
        'email': fields.String(required=True, description='account email address'),
        'first_name': fields.String(required=True, description='account firstname'),
        'last_name': fields.String(required=True, description='account lastname'),
        'role': fields.String(required=True, description='account role'),
        'password': fields.String(required=True, description='account password'),
        'public_id': fields.String(description='account Identifier')
    })


class VlanBindDto:
    api = Namespace('VlanBind',description='vlan bind related operations')
    account = api.model('VlanBind', {
        # 'email': fields.String(required=True, description='account email address'),
        # 'first_name': fields.String(required=True, description='account firstname'),
        # 'last_name': fields.String(required=True, description='account lastname'),
        # 'role': fields.String(required=True, description='account role'),
        # 'password': fields.String(required=True, description='account password'),
        # 'public_id': fields.String(description='account Identifier')
    })

class FirewallRuleDto:
    api = Namespace('FirewallRule',description='firewall rule related operations')
    firewall_rule = api.model('FirewallRule', {
        'ip_address': fields.String(required=True, description='ip address'),
        'rule_num': fields.String(description='rule number'),
        'vlan_id': fields.String(description='vlan id which rule belongs to'),
        'created_on': fields.String(description='created time'),
    })

class AuthDto:
    api = Namespace('Auth', description='authentication related operations')
    account_auth = api.model('Auth_Details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

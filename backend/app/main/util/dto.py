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

class AuthDto:
    api = Namespace('Auth', description='authentication related operations')
    account_auth = api.model('Auth_Details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

from flask_restx import Api
from flask import Blueprint

from .main.controller.account_controller import api as account_ns
from .main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='LAN MANAGEMENT API WITH JWT',
    version='1.0',
    description='backend api for lan mangement system',
    authorizations=authorizations,
    security='apikey'
)

##api.add_namespace(user_ns, path='/user')
api.add_namespace(account_ns, path='/account')
api.add_namespace(auth_ns)

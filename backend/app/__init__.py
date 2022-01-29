from flask_restx import Api
from flask import Blueprint
import logging

from .main.controller.account_controller import api as account_ns
from .main.controller.auth_controller import api as auth_ns


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='lan_api_v1.log',
                    filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
     'refresh_token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'RefreshToken'
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

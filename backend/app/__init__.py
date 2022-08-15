#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2022/08/09 11:51:52
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import logging
from importlib.resources import path

from flask import Blueprint
from flask_restx import Api

from .main.controller.account_controller import api as account_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.firewall_rule_controller import api as firewall_rule_ns
from .main.controller.vlan_bind_controller import api as vlan_bind_ns

logging.basicConfig(
    level=logging.INFO,
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

api = Api(blueprint,
          title='LAN MANAGEMENT API WITH JWT',
          version='1.0',
          description='backend api for lan mangement system',
          authorizations=authorizations,
          security=['apikey', 'refresh_token'])

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(account_ns, path='/account')
api.add_namespace(firewall_rule_ns, path='/firewallrule')
api.add_namespace(vlan_bind_ns, path='/vlanbinding')

#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2022/08/09 21:52:50
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name: str) -> Flask:
    """_summary_

    Args:
        config_name (str): _description_

    Returns:
        Flask: _description_
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    CORS(app, supports_credentials=True, resources={r'/*': {'origins': '*'}})
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app

#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2022/08/09 21:53:08
@Author  :   yehanghan
@Version :   1.0
@Contact :   yehanghan@gmail.com
'''

import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """_summary_
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False


class DevelopmentConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'lan_backend_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'lan_backend_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """_summary_

    Args:
        Config (_type_): _description_
    """
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(dev=DevelopmentConfig,
                      test=TestingConfig,
                      prod=ProductionConfig)


class LANConfig:
    """_summary_
    """
    L3SWICH_HOST = "172.16.10.253"
    L3SWICH_USER = "admin"
    L3SWICH_PASSWORD = "admin"
    FIREWALL_HOST = "172.16.10.254"
    FIREWALL_USER = "admin"
    FIREWALL_PASSWORD = "admin"


key = Config.SECRET_KEY

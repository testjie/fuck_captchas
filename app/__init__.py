# -*- coding:utf-8 -*-
__author__ = 'snake'

from flask import Flask, Blueprint
from config import config

bp = Blueprint("bp", __name__)


def create_app(config_name="DevelopmentConfig"):
    app = Flask(__name__)
    app.config["permanent_session_lifetime"] = False
    app.config.from_object(config[config_name])
    # 注册蓝本
    app.register_blueprint(bp)

    return app
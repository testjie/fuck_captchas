# -*- coding:utf-8 -*-
__author__ = 'snake'

import os
import sys


class BaseConfig:
    HOST = "0.0.0.0"
    JSON_AS_ASCII = False           # json 中文支持
    BABEL_DEFAULT_LOCALE = 'zh'
    SECRET_KEY = os.urandom(24)     # SESSION配置


# 开发环境
class DevelopmentConfig(BaseConfig):
    DEBUG = True


# 线上发布环境
class ProductionConfig(BaseConfig):
    DEBUG = False


config = {
    "DevelopmentConfig": DevelopmentConfig,
    "ProductionConfig": ProductionConfig
    }

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'captcha',
    'charset': 'utf8mb4'
}


UPLOADS_PATH = sys.path[1] + "/app/uploads/"
CNN_WAP_PATH = "C:/Users/SNake/PycharmProjects/fuck_captchas/app/cnn/wap/"
# -*- coding:utf-8 -*-
__author__ = 'snake'
import tensorflow as tf

from app import bp
from flask import request
from app.utils.scmcc_wap import cnn
from app.utils.common import _upload_files


@bp.route("/scmccWapCaptchaCrack", methods=["post"])
def fuck_wap_captcha():
    file = request.files['file']
    file_name = file.filename
    if _upload_files(file, file_name):
        pass

    return "123"




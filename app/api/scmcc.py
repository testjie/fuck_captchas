# -*- coding:utf-8 -*-
__author__ = 'snake'

from app import bp
from flask import jsonify
from flask import request
from config import UPLOADS_PATH
from app.utils.common import upload_files
from app.utils.scmcc_wap import fuck_captcha


@bp.route("/scmccWapCaptchaCrack", methods=["post"])
def fuck_wap_captcha():
    file = request.files['file']
    file_name = file.filename

    if upload_files(file) is False:
        return ""

    captcha_text = fuck_captcha(image_path=UPLOADS_PATH + file_name)

    res = {
        "code": 200,
        "msg": "success!",
        "data": captcha_text
    }
    return jsonify(res)

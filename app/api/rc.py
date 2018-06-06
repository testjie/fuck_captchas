# -*- coding:utf-8 -*-
__author__ = 'snake'

import os
from app import bp
from flask import request
from app.utils.common import _upload_files
from app.utils.common import _get_json_data


@bp.route("/rcCaptachCrack", methods=["POST"])
def rc_captach_crack():
    """
    人工验证码打码
    :return:
    """
    file = request.files['file']
    file_name = file.filename
    if _upload_files(file, file_name):
        from app.utils.rk import RClient
        rc = RClient('snake110', 'a12345678', '1', 'b40ffbee5c1cf4e38028c197eb2fc751')
        im = open(os.path.join("static/captchas/", file_name), 'rb').read()
        return _get_json_data(data=rc.rk_create(im, 1040), msg="success", code=200, url="")

    return _get_json_data(msg="failed", code=-100, data="", url="")
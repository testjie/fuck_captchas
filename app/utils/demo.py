# -*- coding:utf-8 -*-
__author__ = 'snake'

import requests


def _fuck_captache(file_path):
    """
    返回验证码
    :param file_path:
    :return: 0为错误，其他为正确
    """
    try:
        file = open(file_path, 'rb').read()
        filename = file_path.split("/")[-1]
        files = {'file': (filename, file)}
        r = requests.post('http://localhost:87/scmccWapCaptchaCrack', files=files)
        if r.status_code == 200:
            return r.text

        return ""
    except Exception as e:
        return ""


if __name__ == "__main__":
    path = "./4942.jpg"
    print(_fuck_captache(path))
# -*- coding:utf-8 -*-
__author__ = 'snake'

import os
import json
from config import UPLOADS_PATH
from flask import request
from datetime import datetime
from app.utils.db import query, excute


def scan_sql_injector(keywords):
    """
    sql注入检测工具
    :param keywords:
    :return: True: 通过；False：不通过
    """
    rules = ["=", "and", "or", "%", "*", "admin", "administrator", "root", "select", "drop", ">",
             "<", "!", "@", "#", "$", "^", "&", "(", ")", "~", "_", "=", "+", "-", "[", "]", ":",
             ";", "'", "\"", "?", "/", "！", "￥", "……", "【", "】", "、", "|", "\\", "AND", "OR",
             "？", "）", "（", "：", "～", "”", "“", "；", "‘", "’", "、", "。", "，", "《", "》", "·"]

    for kw in rules:
        if kw in keywords:
            return False
    return True


def get_real_ip():
    """
    # 获取真实ip，第一种情况为nginx转发，第二种情况为直接访问
    :return:
    """
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr


def is_overload_commmit(ip, form_id, times=1):
    """
    判断当前ip访问当前的form是否超过提交次数 默认为3分钟一次
    :param ip:
    :param form_id:
    :param times:
    :return:
        返回值：
        1:存在记录并且通过
        2:不存在记录
        -1:form_id不存在
        -2:存在多个ip记录，情况异常
        -3:3分钟内多次提交
    """
    # 1.查询form_id是否存在
    sql = "select * from tbl_form_id where form_id ='%s'" % form_id
    if query(sql) is None:
        return "-1"

    sql = "select * from tbl_ip_limit where form_id='%s' and ip='%s'" % (form_id, ip)
    result = query(sql)
    # 如果存在该ip的记录，则进行下一步

    if result:
        if len(result) > 1:
            return "-2"
        success_submit_times = result[0].get("success_submit_times")
        # 计算当前时间和上次时间的时间差
        now_time = datetime.now()
        t_str = result[0].get("last_submit_time")
        last_submit_time = datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')

        time_diff = (now_time - last_submit_time).total_seconds()
        if success_submit_times == times or time_diff < 181:
            return "-3"
        else:
            return "1"
    # 如果没有，直接进行操作
    else:
        return "2"


def add_user_access_histroy(user_ip, interface):
    """
    添加用户访问历史记录
    :param user_ip:
    :param interface:
    :return:
    """
    sql = "INSERT INTO tbl_user_access_history VALUES(NULL, '%s', '%s', '%s')" % (
        user_ip, interface, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    excute(sql)


# 获得json记录
def _get_json_data(data, code, msg, url):
    """
    获得json
    :param data:
    :param code:
    :param msg:
    :param url:
    :return:
    """
    json_data = {
        "data": data,
        "code": code,
        "msg": msg,
        "url": url,
    }
    try:
        return json.dumps(json_data)
    except:
        return []


# todo 文件保存失败
def upload_files(file):
    """
    上传图片公共方法
    :param file: 上传的file文件
    :return: True:成功;False失败
    """
    try:
        upload_path = os.path.join(UPLOADS_PATH, file.filename)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        file.save(upload_path)
        return True
    except Exception as e:
        return False



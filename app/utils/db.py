# -*- coding:utf-8 -*-
__author__ = 'snake'
from datetime import datetime
import config, copy, pymysql


def decode_result_date(datas):
    """
    将数据库查询的数据进行时间格式化
    :param datas: (())， 从数据库查询的数据
    :return: [[]] 返回list列表
    """
    results = []
    for data in datas:
        tmp_list = []
        for item in data:
            if isinstance(item, datetime):
                tmp_list.append(item.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                tmp_list.append(item)
        results.append(tmp_list)

    return results


def query(sql=""):
    """
        根据sql查询结果
        args: sql
        return: results 返回结果[{'articleId': 2, 'status': 1, 'createDate': '2018-03-30 11:22:50', 'userId': -1, 'id': 4, 'updateDate': None}]
    """
    results = []
    db = pymysql.connect(**config.db_config)
    cur = db.cursor()
    try:
        cur.execute(sql)  # 执行sql语句
        # 获得列名
        descs = []
        for desc in cur.description:
            descs.append(desc[0])

        # 构造键值对{"列名":数据}
        results = []
        for res in decode_result_date(cur.fetchall()):
            row = {}
            for i in range(len(descs)):
                row[descs[i]] = res[i]
            results.append(row)
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()  # 关闭连接
        return results


def excute(sql=""):
    """
        根据sql插入或更新数据
        args: sql
        return: is_success，1:成功 0失败
    """
    is_success = True
    db = pymysql.connect(**config.db_config)
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        is_success = False
    finally:
        cur.close()
        db.close()
        return is_success


def excutemany(sqls=[]):
    """
        执行多条插入或更新语句，级联提交时可使用此方法
        args: [sql1, sql2,...]
        return: is_success，1:成功 0失败
    """
    is_success = True
    db = pymysql.connect(**config.db_config)
    cur = db.cursor()
    try:
        for sql in sqls:
            cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        is_success = False
    finally:
        cur.close()
        db.close()
        return is_success


if __name__ == "__main__":
    data = query("select * from tbl_user where username='1' and password='1'")
    print(data)

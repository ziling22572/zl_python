#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql


class MysqlUtils:
    conn = pymysql.connect(host="localhost", user="root", password="root", database="ziling_api", charset="utf8")
    # 连接database
    cursor = conn.cursor()
    # 定义要执行的SQL语句
    sql = "SELECT GROUP_CONCAT( a.number ) FROM	welfarelotterypnginfo a WHERE	a.pngnumber IN ('20180820032902106488','20180820032902108769',		'20180820032902122325',		'20180820032902124365',		'20180820032902125143',		'20180820032902126490',	'20180820032902501531',	'')"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取结果
    results = cursor.fetchall()
    print(results.__getitem__(0))
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()

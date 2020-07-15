# encoding: utf-8
'''
@Author:peter young
@file: db2.py
@time: 2020/7/15 21:37
'''

import sqlite3


def get_conn():
    return sqlite3.connect('test.sqlite3')


def query_data(sql):
    conn = get_conn()
    #用DictCursor返回的是字典的形式，而不是数组
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def insert_or_update_date(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print("successful")
    finally:
        conn.close()


def create_table(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print("successful")
    finally:
        conn.close()


if __name__ == "__main__":
    # sql ='''CREATE TABLE test
	# 	(ID INT PRIMARY KEY NOT NULL,
	# 	NAME         TEXT  NOT NULL,
	# 	AGE          INT   NOT NULL);'''
    # create_table(sql)

    # sql = " insert into test (ID,name,age) values(1,'daming',20)"
    # sql = " insert into test (ID,name,age) values(2,'xiaoming',25)"
    # insert_or_update_date(sql)

    sql = "select * from test"
    datas = query_data(sql)
    import pprint

    pprint.pprint(datas)

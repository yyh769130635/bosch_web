# -*- coding: utf-8 -*-
# @Time : 7/21/2020 11:19 AM
# @Author : Peter yang

import psutil
import datetime
import sqlite3
import os

# ------------Variables---------------#

database_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + r"\db.sqlite3"

# ------------/Variables--------------#

# 链接数据库
def get_conn():
    global database_path
    return sqlite3.connect(database_path)


# 创建表
def create_table(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print("successful")
    finally:
        conn.close()


def query_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def insert_or_update_date(sql, data):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print("successful")
    finally:
        conn.close()


if __name__ == "__main__":

    with open(r"C:\Users\YGP2SZH\Desktop\result-2\time_record.txt", "r") as f:
        line = f.readline()
        while line:
            temp = line.split(";")
            folder_name = temp[0].split("\\")[-1]
            temp.insert(0, folder_name)
            data = tuple(temp,)
            sql = "insert into ShowSpace_radar05 (folder_name,folder_dir,folder_size,scan_date,time_duration) values(?,?,?,?,?);"
            insert_or_update_date(sql, data)
            line = f.readline()

    ####################################################################################################

    # folder = [r'//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/01_GEN4',
    #           r'//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/05_Radar_ER']
    # for i in range(len(folder)):
    #     usage = psutil.disk_usage(folder[i])
    #     t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     sql = "insert into ShowSpace_isilon (folder_NAME,folder_DIR,total_space,used_space,free_space,PERCENTAGE,SCAN_date) values(?,?,?,?,?,?,?);"
    #     total = str(usage.total // 1024 // 1024 // 1024) + "GB"
    #     used = str(usage.used // 1024 // 1024 // 1024) + "GB"
    #     free = str(usage.free // 1024 // 1024 // 1024) + "GB"
    #     percentage = str(usage.percent) + "%"
    #     data = ("isilon{}".format(i + 1), folder[i], total, used, free, percentage, t)
    #     print(data)
    #     insert_or_update_date(sql, data)

    ####################################################################################################
    # sql = '''
    # create table isilon (
    # NAME          varchar (50),
    # DIR           text,
    # TOTAL         integer default 0,
    # USED          integer default 0,
    # FREE          integer default 0,
    # PERCENTAGE    real,
    # SCAN_TIME     text );'''
    # create_table(sql)

    # print(os.getcwd())
    # # 上一级目录的路径
    # path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print(path)
    # print(database_path)

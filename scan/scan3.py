# -*- coding: utf-8 -*-
# @Time : 7/24/2020 5:23 PM
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
    pass
    # print(os.getcwd())
    # path = r"C:\Users\YGP2SZH\Desktop\result-2\radar_05_details"
    # for root, sub_dirs, Files in os.walk(path):
    #     for file_name in Files:
    #         with open(path+"\\"+file_name, "r") as f:
    #             line = f.readline()
    #             while line:
    #                 temp = line.strip("\n").split(";")
    #                 print(temp)
    #                 folder_name = temp[0].split("\\")[-1]
    #                 temp.insert(0, folder_name)
    #                 data = tuple(temp,)
    #                 print(data)
    #                 sql = "insert into ShowSpace_radar05_details (folder_name,folder_dir,type,number,size,scan_date) values(?,?,?,?,?,?);"
    #                 insert_or_update_date(sql, data)
    #                 line = f.readline()
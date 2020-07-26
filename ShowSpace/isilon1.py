# -*- coding: utf-8 -*-
# @Time : 7/23/2020 2:32 PM
# @Author : Peter yang

from django.shortcuts import render
from django.http import HttpResponse

from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, PictorialBar, Funnel, Pie, Gauge
from pyecharts.globals import SymbolType
from pyecharts.options import ComponentTitleOpts

###############
import psutil
import os
import time
import datetime
import sqlite3

# -----------------<variables>--------------------

database_path = r".\db.sqlite3"


# -----------------<variables>--------------------


def query_data_one(sql, data=()):
    conn = sqlite3.connect(database_path)
    try:
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        return cursor.fetchone()
    except:
        conn.rollback()
    finally:
        conn.close()


def isilon_info(i):
    '''
    :param i: isilon {n}
    :return: isilon {n} 's info
    '''
    data = ("isilon{}".format(i),)
    sql = "select total_space,used_space,free_space,percentage,scan_date from ShowSpace_isilon where folder_name=? order by scan_date  desc"
    temp = query_data_one(sql, data)
    info = {}
    info["total"] = round(int(temp[0][:-2]) // 1024, 2)
    info["used"] = round(int(temp[1][:-2]) // 1024, 2)
    info["free"] = round(int(temp[2][:-2]) // 1024, 2)
    info["percentage"] = temp[3]
    info["scan_date"] = temp[4]
    return info


def read_context(totalSpace):
    '''
    :param totalSpace: isilon1's total space
    :return: {}
    '''
    ## 读txt，之后再配合数据库
    res = {}
    path = r".\scan\IsilonSzh.txt"
    with open(path, "r") as f:
        line = f.readline()
        while line:
            temp = line.split(" ")
            used = temp[2].split(",")[0]
            used = round(int(used) / 1024, 2)
            res[temp[0]] = [used, round((used / totalSpace) * 100, 2), "2020-07-15 11:08"]
            line = f.readline()
    return res


def main(request):
    isilon1 = isilon_info(1)
    context = read_context(isilon1["total"])

    return render(request, 'ShowSpace/isilon1.html', {"context": context})

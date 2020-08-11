# -*- coding: utf-8 -*-
# @Time : 7/20/2020 1:41 PM
# @Author : Peter yang

from django.shortcuts import render
from django.http import HttpResponse

from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, PictorialBar, Funnel, Pie, Line
from pyecharts.faker import Faker
from pyecharts.globals import SymbolType
from pyecharts.options import ComponentTitleOpts

###############
import psutil
import os
import time
import datetime
import sqlite3
import pprint

# -----------------<variables>--------------------

database_path = r".\db.sqlite3"


# database_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + r"\db.sqlite3"


# -----------------<variables>--------------------

def query_data(sql, data=()):
    conn = sqlite3.connect(database_path)
    try:
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    except:
        conn.rollback()
    finally:
        conn.close()


def query_data_many(sql, data=()):
    conn = sqlite3.connect(database_path)
    try:
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        return cursor.fetchmany()
    except:
        conn.rollback()
    finally:
        conn.close()


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
    data = ("isilon{}".format(i),)
    sql = "select total_space,used_space,free_space,percentage,scan_date from ShowSpace_isilon where folder_name=? order by scan_date  desc"
    temp = query_data_one(sql, data)
    info = {}
    info["total"] = round(int(temp[0][:-2]) // 1024, 2)  # ->TB
    info["used"] = round(int(temp[1][:-2]) // 1024, 2)  # ->TB
    info["free"] = round(int(temp[2][:-2]) // 1024, 2)
    info["percentage"] = temp[3]
    info["scan_date"] = temp[4]
    return info


def radar05_info(totalSpace):
    # totalSpace = isilon_info(2)["total"]
    ans = {}
    sql = "select DISTINCT folder_name from ShowSpace_radar05 "
    names = query_data(sql)
    for name in names:
        sql = "select folder_size,scan_date from ShowSpace_radar05 where folder_name=? order by scan_date  desc"
        temp = query_data_one(sql, name)
        # 扫描单位是B
        usedSpace = round(int(temp[0]) // 1024 // 1024 // 1024 / 1024, 2)
        ans[name[0]] = [usedSpace, round((usedSpace / totalSpace) * 100, 2), temp[1]]
    # print(ans)
    return ans


def radar_05_folder_info(folder_name):
    # folder_name = "08_report_summary"
    sql = "select folder_size,scan_date from ShowSpace_radar05 where folder_name=? order by scan_date"
    ans = query_data(sql, (folder_name,))
    print(ans)
    return ans


def main(request):
    global folder_Info_path

    # 数据库中读入isilon2的信息
    Radar_05_Disk_Usage = isilon_info(2)

    result = radar05_info(Radar_05_Disk_Usage["total"])

    values2 = sorted(result.items(), key=lambda result: result[0])  # 按照名字排序
    values1 = []
    for k, v in result.items():
        values1.append([k, v[0]])
    # values1.append(["others",])
    values11 = sorted(values1, key=lambda x: x[0])  # 按照名字排序的

    # inner_data_pair = [i for i in sorted(values1, key=lambda x: -x[1])][:3]  # 按照大小排序
    # c = (
    #     Pie(init_opts=opts.InitOpts(width="1200px", height="400px"))
    #         .add("", values11, center=["50%", "50%"], is_clockwise=False, radius=["50%", "80%"])
    #         .set_global_opts(
    #         legend_opts=opts.LegendOpts(type_="scroll", pos_right="80%", pos_top="15%", orient="vertical"), )
    #         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", color="#000000", font_size=13))
    #         .set_colors(
    #         ["#000000", "#6495ED", "#90EE90", "#00FFFF", "#FFCC00", "#FF0000", "#FFDEAD", "#008B8B", "#7FFFD4",
    #          "#CCCC99","#FF0000", "#00FFFF", "#6495ED"])
    #         .add(series_name="", data_pair=inner_data_pair, radius=[0, "30%"],
    #              label_opts=opts.LabelOpts(position="inner", color="#000000", font_size=8), center=["50%", "50%"], )
    # )

    c = (
        Pie(init_opts=opts.InitOpts(width="1200px", height="400px"))
            .add("", values11, center=["50%", "50%"], is_clockwise=False, radius=["40%", "80%"], )
            .set_global_opts(
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="80%", pos_top="15%", orient="vertical"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", color="#000000", font_size=13))
            .set_colors(
            ["#000000", "#6495ED", "#90EE90", "#00FFFF", "#FFCC00", "#FF0000", "#FFDEAD", "#008B8B", "#7FFFD4",
             "#CCCC99", "#FF0000", "#00FFFF", "#6495ED"])
    )

    return render(request, 'ShowSpace/radar05.html', {'result': values2, 'data': c.render_embed()})


# 不用了
def readfile(path, totalSpace):
    # path = r'.\result\time_record.txt'
    values = {}
    with open(path, "r+") as f:
        line = f.readline()
        while line:
            temp = line.strip().split(";")
            folder_name = temp[0].split("\\")[-1]
            # 扫描的时候记录单位是B
            usedSpace = round(int(temp[1]) // 1024 // 1024 // 1024 / 1024, 2)
            values[folder_name] = [round(usedSpace, 2),
                                   round((usedSpace / totalSpace) * 100, 2), temp[2]]
            line = f.readline()
    return values


def get_radar05_details(name):
    # name = "00_Cluster"
    ans = []
    value = []
    #sql = '''select DISTINCT type from ShowSpace_radar05_details '''
    # pprint.pprint(query_data(sql))
    #types = query_data(sql)
    #file_Format = ("AVI", "ZIP", "MF4", "RIF", "7Z","others")
    types = ["MF4","RIF","AVI","ZIP","7Z","others"]
    for type in types:
        #if type[0] not in file_Format:
            #continue
        sql = '''select folder_name,type,number,size,scan_date from ShowSpace_radar05_details
                    where folder_name=?  and type =? order by scan_date DESC'''
        i = query_data_one(sql, (name, type,))

        size = round(int(i[3]) // 1024 // 1024 // 1024 / 1024, 2)
        ans.append([i[1], i[2], size, i[4]])
        value.append([i[1], int(i[3])])
    # pprint.pprint(ans)
    return ans, value


def get_details(request, name):
    ###先读txt,之后配合数据库
    # print(hello)
    # data = []
    # values1 = []
    # file_name_dir = "\\" + name + ".txt"
    # with open(r".\scan\result\radar_05_details" + file_name_dir, "r") as f:
    #     line = f.readline()
    #     while line:
    #         temp = line.strip().split(";")
    #         size = round(int(temp[3]) // 1024 // 1024 // 1024 / 1024, 2)
    #         # name = temp[0].split("\\")
    #         data.append([temp[1], temp[2], size, temp[4]])
    #         values1.append([temp[1], int(temp[3])])
    #         line = f.readline()

    data1, values1 = get_radar05_details(name)

    # data1 = data[-6:]
    # values11 = values1[-6:]

    c = (Pie(init_opts=opts.InitOpts(width="600px", height="320px"))
        .add("", values1, center=["50%", "50%"], is_clockwise=False, radius=["30%", "60%"])
        .set_global_opts(
        legend_opts=opts.LegendOpts(type_="scroll", pos_right="85%", orient="vertical"),
    )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", color="#000000", font_size=13))
        .set_colors(
        ["#FF4500", "#FFA500", "#FFFF00", "#90EE90", "#48D1CC", "#87CEEB", "#9370DB"])
    )

    # c = (
    #     Bar(init_opts=opts.InitOpts(width="600px", height="250px"))
    #         .add_xaxis([values11[i][0] for i in range(len(values11))])
    #         .add_yaxis("文件类型大小", [values11[i][1]//10000000000 for i in range(len(values11))], stack="stack1")
    #         .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    #         .set_global_opts(title_opts=opts.TitleOpts(title="文件类型及其大小"),
    #                        yaxis_opts= opts.AxisOpts(type_="log",is_scale=True) )
    #         .set_colors(
    #         ["#6495ED"])
    # )

    ans = radar_05_folder_info(name)
    date = [ans[i][1] for i in range(len(ans))]
    size = [round(ans[i][0] // 1024 // 1024 // 1024 / 1024, 2) for i in range(len(ans))]
    d = (Line(init_opts=opts.InitOpts(width="1200px", height="300px"))
        .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        xaxis_opts=opts.AxisOpts(type_="category", name="date"),
        yaxis_opts=opts.AxisOpts(type_="value",
                                 axistick_opts=opts.AxisTickOpts(is_show=True),
                                 splitline_opts=opts.SplitLineOpts(is_show=True),
                                 name="Size TB",
                                 max_=int(max(size)) + 100,
                                 min_=int(min(size)) - 100,
                                 ))
        .add_xaxis(xaxis_data=date)
        .add_yaxis(
        series_name="Folder " + name,
        y_axis=size,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(type_="max", name="max", symbol_size=70, symbol="pin")]
            ),
    )
    )

    return render(request, "ShowSpace/details.html", {"data": data1, "data2": c.render_embed(),
                                                      "folder_name": name, "temp": d.render_embed()})


if __name__ == "__main__":
    # ##先读txt,之后配合数据库
    # data = []
    # with open(r"C:\Users\YGP2SZH\Desktop\myProject\scan\result\radar_05_details\00_Cluster.txt", "r") as f:
    #     line = f.readline()
    #     while line:
    #         temp = line.split(";")
    #         # print(temp)
    #         data.append([temp[1], temp[2], temp[3], temp[4]])
    #         line = f.readline()
    # print(data)

    sql = '''select DISTINCT type from ShowSpace_radar05_details '''
    # pprint.pprint(query_data(sql))
    types = query_data(sql)
    for i in types:
        # print(i[0])
        sql = '''select folder_name,type,number,size,scan_date from ShowSpace_radar05_details
            where folder_name=?  and type =? order by scan_date DESC'''
        print(query_data(sql, ("00_Cluster", i[0],)))

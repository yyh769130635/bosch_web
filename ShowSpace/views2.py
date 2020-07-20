# -*- coding: utf-8 -*-
# @Time : 7/20/2020 1:41 PM
# @Author : Peter yang

from django.shortcuts import render
from django.http import HttpResponse

from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, PictorialBar, Funnel, Pie
from pyecharts.globals import SymbolType
from pyecharts.options import ComponentTitleOpts

###############
import psutil
import os
import time
import datetime
# -----------------<variables>--------------------
folder_Info_path = r'.\scan\result\time_record.txt'
radar_05_details_path = r".\scan\result\isilon2.txt"
# -----------------<variables>--------------------

def main(request):
    global folder_Info_path
    global radar_05_details_path

    with open(radar_05_details_path) as f:
        Radar_05_Disk_Usage = f.readline().split(";")

    result = readfile(folder_Info_path, int(Radar_05_Disk_Usage[0]))

    values2 = sorted(result.items(), key=lambda result: result[0])  # 按照名字排序
    values1 = []
    for k, v in result.items():
        values1.append([k, v[0]])
    values11 = sorted(values1, key=lambda x: x[0])  # 按照名字排序的
    inner_data_pair = [i for i in sorted(values1, key=lambda x: -x[1])][:3]  # 按照大小排序

    c = (Pie().add("", values11, center=["50%", "50%"], is_clockwise=False, radius=["45%", "70%"])
        .set_global_opts(
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="85%", orient="vertical"),
    )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", color="#000000", font_size=10))
        .set_colors(
        ["#000000", "#6495ED", "#90EE90", "#00FFFF", "#FFCC00", "#FF0000", "#FFDEAD", "#008B8B", "#7FFFD4", "#CCCC99",
         "#FF0000", "#00FFFF", "#6495ED"])
        .add(
        series_name="",
        data_pair=inner_data_pair,
        radius=[0, "30%"],
        label_opts=opts.LabelOpts(position="inner"),
        center=["50%", "50%"],
    )
    )

    return render(request, 'ShowSpace/index.html', {'result': values2, 'data': c.render_embed()})


def readfile(path, totalSpace):
    # path = r'.\result\time_record.txt'
    values = {}
    with open(path, "r+") as f:
        line = f.readline()
        while line:
            temp = line.strip().split(";")
            temp2 = temp[0].split("\\")[-1]
            # 扫描的时候记录单位是GB
            usedSpace = int(temp[1][:-2])
            values[temp2] = [round(usedSpace / 1024, 2),
                             round((usedSpace / (totalSpace // 1024 // 1024 // 1024)) * 100, 2), temp[2]]
            line = f.readline()
    return values


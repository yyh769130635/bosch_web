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

def hello(request):
    return render(request, "ShowSpace/hello.html")


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
    path = r"C:\Users\YGP2SZH\Desktop\myProject\scan\IsilonSzh.txt"
    with open(path, "r") as f:
        line = f.readline()
        while line:
            temp = line.split(" ")
            used = temp[2].split(",")[0]
            used = round(int(used) / 1024, 2)
            res[temp[0]] = [used, round((used / totalSpace) * 100, 2), "2020-07-15 11:08"]
            line = f.readline()

    # print(res)
    return res
    
    
def real_time():
    path1 = r"//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/01_GEN4"
    path2 = r"//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/05_Radar_ER"
    isilon1 = {}
    isilon2 = {}
    temp1 = psutil.disk_usage(path1)
    isilon1["total"] = round(temp1.total // 1024 // 1024 // 1024 / 1024, 2)
    isilon1["used"] = round(temp1.used // 1024 // 1024 // 1024 / 1024, 2)
    isilon1["free"] = round(temp1.free // 1024 // 1024 // 1024 / 1024, 2)
    isilon1["scan_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
<<<<<<< HEAD
    isilon1["percentage"] = str(temp1.percent)+"%"
=======
    isilon1["percentage"] = temp1.percent
>>>>>>> parent of f783f78... 8.9

    temp2 = psutil.disk_usage(path2)
    isilon2["total"] = round(temp2.total // 1024 // 1024 // 1024 / 1024, 2)
    isilon2["used"] = round(temp2.used // 1024 // 1024 // 1024 / 1024, 2)
    isilon2["free"] = round(temp2.free // 1024 // 1024 // 1024 / 1024, 2)
    isilon2["scan_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
<<<<<<< HEAD
    isilon2["percentage"] = str(temp2.percent)+"%"
=======
    isilon2["percentage"] = temp2.percent
>>>>>>> parent of f783f78... 8.9

    return isilon1, isilon2
    

def main(request):
    isilon1, isilon2 = real_time()
<<<<<<< HEAD
    #isilon1 = isilon_info(1)
    #isilon2 = isilon_info(2)
=======

    # isilon1 = isilon_info(1)
    # is    ilon2 = isilon_info(2)
>>>>>>> parent of f783f78... 8.9

    rate1 = round((isilon1["used"] / isilon1["total"]) * 100, 2)
    d1 = (
        Gauge(init_opts=opts.InitOpts(width="400px", height="320px"))
            .add("", [("Usage Percentage", rate1)],
                 split_number=5,
                 axisline_opts=opts.AxisLineOpts(
                     linestyle_opts=opts.LineStyleOpts(
                         color=[(0.3, "#67e0e3"), (0.7, "#37a2da"), (1, "#fd666d")], width=30
                     )
                 ),
                 # title_label_opts=opts.LabelOpts(font_size=25, color="#FF0000", font_family="Microsoft YaHei"),
                 title_label_opts=opts.LabelOpts(is_show=False),
                 detail_label_opts=opts.LabelOpts(font_size=14, color="#FF0000", font_family="Microsoft YaHei",
                                                  formatter="Used Percentage: \n{value}%"),
                 )
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    rate2 = round((isilon2["used"] / isilon2["total"]) * 100, 2)
    d2 = (
        Gauge(init_opts=opts.InitOpts(width="400px", height="320px"))
            .add("", [("Usage Percentage", rate2)],
                 split_number=5,
                 axisline_opts=opts.AxisLineOpts(
                     linestyle_opts=opts.LineStyleOpts(
                         color=[(0.3, "#67e0e3"), (0.7, "#37a2da"), (1, "#fd666d")], width=30
                     )
                 ),
                 # title_label_opts=opts.LabelOpts(font_size=25, color="#FF0000", font_family="Microsoft YaHei"),
                 title_label_opts=opts.LabelOpts(is_show=False),
                 detail_label_opts=opts.LabelOpts(font_size=14, color="#FF0000", font_family="Microsoft YaHei",
                                                  formatter="Used Percentage: \n{value}%"),
                 )
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    # 饼图
    # c = (
    #     Pie(init_opts=opts.InitOpts(width="800px", height="250px"))
    #         .add("", pie_values, radius=["50%", "80%"],
    #              label_opts=opts.LabelOpts(
    #                  position="outside",
    #                  formatter=" {b|{b}: }\n {c| {c}TB} , {per|{d}%} ",
    #                  background_color="#FFFFFF", border_color="#000000",
    #                  border_width=1, border_radius=4,
    #                  rich={
    #                      "b": {"fontSize": 20, "lineHeight": 33, 'color': '#000080', 'align': 'center'},
    #                      "per": {"fontSize": 15, "lineHeight": 20, 'color': '#FF0000'},
    #                      "c": {'color': '#000000', "fontSize": 15, 'lineHeight': 20, 'align': 'center'}
    #                  },
    #              ),
    #              ).set_colors(['#A9A9A9', '#00BFFF']).set_global_opts(
    #         legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
    #     ))

    return render(request, 'ShowSpace/FreeSpace.html', {'data2': d2.render_embed(), 'data1': d1.render_embed(),
                                                        'isilon1': isilon1, 'isilon2': isilon2})


if __name__ == "__main__":
    read_context()

#     print(datetime.datetime.now().strftime('%F %T'))

# import os
# # 上一级目录的路径
# path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# path = path + r"\result"

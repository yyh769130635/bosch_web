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

# 扫描文件的结果
g_scannedResultPath = './result'
# 在G盘
# g_Disk_path_1 = r'\\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\01_GEN4'
# g_Disk_path_2 = '//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/05_Radar_ER'
g_Disk_path_1 = r"D:\\"
g_Disk_path_2 = r"C:\\"


# 换算成TB
def intoTB(data) -> str:
    return str(round(int(data) / 1024 / 1024 / 1024 / 1024, 2)) + ' TB'  # Byte --> TeraByte and leave 2 decimal places


def intoTB2(data) -> float:
    return round(int(data) / 1024 / 1024 / 1024 / 1024, 2)


# 输入输出是整个szh文件夹的情况
def readResult(scannedResultPath, totalSpace) -> dict:
    '''
    :param scannedResultPath: 扫描结果文件夹的路径
    :param totalSpace: DiskUsage_2.total 盘的总大小
    查看05_Radar_ER文件夹使用情况,返回文件夹的空间大小、占用率、扫描时间
    :return:
    {'\\\\abtvdfs2.de.bosch.com\\ismdfs\\loc\\szh\\000000':
    ['0.0 TB','0.21%','2020-06-16 15:59:51'], .........}
    '''

    result = {}
    for eachResult in os.listdir(scannedResultPath):
        try:
            with open(os.path.join(scannedResultPath, eachResult), mode='r') as f:
                scanned = f.read().split('\n')
            # scanned = open(os.path.join(scannedResultPath, eachResult)).read().split('\n')
            pass
        except:
            scanned = []
            pass

        # print(eachResult)
        eachPath = '\\\\' + eachResult.replace('-', '\\').strip('.txt')
        # print(scanned)
        for each in scanned:
            if each != '':
                usedSpace = each.split(';')[1]
                if eachPath not in result:
                    # result = {path : [space, percent, time]}
                    result[eachPath] = [int(usedSpace),
                                        str(round((int(usedSpace) / totalSpace) * 100, 2)) + '%',
                                        TimeStampToTime(
                                            os.path.getmtime(os.path.join(scannedResultPath, eachResult))), ]
                else:
                    result[eachPath][0] += int(usedSpace)  # Sum All
                    result[eachPath][1] = str(round((result[eachPath][0] / totalSpace) * 100, 2)) + '%'

    for i in result:
        result[i][0] = intoTB(result[i][0])

    return result


# 输入输出是radar那个文件夹的情况
def read_05_Radar(scannedResultPath, totalSpace):
    '''
    :param scannedResultPath: 扫描结果文件夹的路径
    :param totalSpace: DiskUsage_2.total 盘的总大小
    :return:
    '''
    Radar_05_result = {}
    diskUsage = 0
    for eachResult in os.listdir(scannedResultPath):
        try:
            with open(os.path.join(scannedResultPath, eachResult), mode='r') as f:
                scanned = f.read().split('\n')
            # scanned = open(os.path.join(scannedResultPath, eachResult)).read().split('\n')
            pass
        except:
            scanned = []
            pass
        # get specific details of 05_Radar
        if '05_Radar_ER' in eachResult:
            for each in scanned:
                if each != '':
                    path = each.split(';')[0]
                    usedSpace = each.split(';')[1]
                    scannedTime = each.split(';')[2]

                    if 'UNC' in path:
                        path = '\\\\' + path.lstrip('\\\\?\\UNC')
                    else:
                        path = path.lstrip('\\\\?\\')

                    Radar_05_result[path] = [usedSpace,
                                             str(round((int(usedSpace) / totalSpace) * 100, 2)) + '%',
                                             scannedTime, ]  # {path : [space, percent]}
                    diskUsage += int(usedSpace)
    for i in Radar_05_result:
        Radar_05_result[i][0] = intoTB(Radar_05_result[i][0])

    return Radar_05_result, diskUsage


# 输入输出是radar那个文件夹的情况
def read_05_Radar2(scannedResultPath, totalSpace):
    '''
    :param scannedResultPath: 扫描结果文件夹的路径
    :param totalSpace: DiskUsage_2.total 盘的总大小,用于统计文件夹占用比
    :return: {__:[__,__,__]}
    '''

    Radar_05_result = {}
    for eachResult in os.listdir(scannedResultPath):
        try:
            with open(os.path.join(scannedResultPath, eachResult), mode='r') as f:
                scanned = f.read().split('\n')
            # scanned = open(os.path.join(scannedResultPath, eachResult), mode='r').read().split('\n')
            pass
        except:
            scanned = []
            pass
        # get specific details of 05_Radar
        if '05_Radar_ER' in eachResult:
            for each in scanned:
                if each != '':
                    path = each.split(';')[0]
                    usedSpace = each.split(';')[1]
                    scannedTime = each.split(';')[2]

                    if 'UNC' in path:
                        path = '\\\\' + path.lstrip('\\\\?\\UNC')  ##lstrip() 方法用于截掉字符串左边的空格或指定字符
                    else:
                        path = path.lstrip('\\\\?\\')
                    # mainDir = r"\\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_E"
                    title = path.split("\\")[-1]
                    Radar_05_result[title] = [usedSpace,
                                              round((int(usedSpace) / totalSpace) * 100, 2),
                                              scannedTime, int(usedSpace)]  # {path : [space, percent]}

    for i in Radar_05_result:
        Radar_05_result[i][0] = intoTB(Radar_05_result[i][0])

    return Radar_05_result


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def getLastUpdateTime(scannedResultPath):
    return TimeStampToTime(os.path.getctime(scannedResultPath))


# 这个是主函数,对主页模板渲染
def index(request):
    '''
    :param request:
    :return: dict传给html渲染
    '''
    scannedResultPath = g_scannedResultPath

    context = {}

    # r'\\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\01_GEN4'
    DiskUsage_1 = psutil.disk_usage(g_Disk_path_1)
    context['Total_1'] = intoTB(DiskUsage_1.total)
    context['Used_1'] = intoTB(DiskUsage_1.used)
    context['Free_1'] = intoTB(DiskUsage_1.free)
    context['Percentage_1'] = round(100 - DiskUsage_1.percent, 2)  # unused

    # g_Disk_path_2 = '//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/05_Radar_ER'
    DiskUsage_2 = psutil.disk_usage(g_Disk_path_2)
    context['Total_2'] = intoTB(DiskUsage_2.total)
    context['Used_2'] = intoTB(DiskUsage_2.used)
    context['Free_2'] = intoTB(DiskUsage_2.free)
    context['Percentage_2'] = round(100 - DiskUsage_2.percent, 2)  # unused

    # combine_05_Radar(scannedResultPath) #Write into File
    context['Drives'] = readResult(scannedResultPath, DiskUsage_2.total)  # ->Dict{list1,list2}
    context['Radar_05'], diskUsage = read_05_Radar(scannedResultPath, DiskUsage_2.total)  # ->Dict{list1,list2},int

    context['LastUpdate'] = getLastUpdateTime(scannedResultPath)
    context['curTime'] = datetime.datetime.now().strftime('%F %T')
    values2 = []
    values2.append(["Free Space", DiskUsage_2.total - diskUsage])
    values2.append(["Used Space", diskUsage])
    c = (
        Pie(init_opts=opts.InitOpts(width="800px", height="250px"))
            .add("", values2, radius=["50%", "80%"],
                 label_opts=opts.LabelOpts(
                     position="outside",
                     formatter="{b|  {b}: } {per|{d}%}  ",
                     background_color="#FFFFFF", border_color="#000000",
                     border_width=1, border_radius=4,
                     rich={
                         "b": {"fontSize": 15, "lineHeight": 33, 'color': '#000080'},
                         "per": {"fontSize": 15, "lineHeight": 33, 'color': '#FF0000'},
                     },
                 ),
                 ).set_colors(['#A9A9A9', '#00BFFF']).set_global_opts(
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        ))

    return render(request, 'ShowSpace/FreeSpace.html', {'context': context, 'data': c.render_embed()})


def index2(request):
    scannedResultPath = g_scannedResultPath
    DiskUsage_2 = psutil.disk_usage(g_Disk_path_2)
    result = read_05_Radar2(scannedResultPath, DiskUsage_2.total)
    used = 0
    values1 = []
    # print(result)
    others = 0
    # for k, v in result.items():
    #     if v[3] < 9000000000000:
    #         others += v[3]
    #     else:
    #         values1.append([k, v[3]])
    #         used += v[1]
    # values1.append(['others', others])
    for k, v in result.items():
        values1.append([k, v[3]])
        used += v[1]
    values11 = sorted(values1, key=lambda x: x[0]) #按照名字排序的
    values2 = sorted(result.items(), key=lambda result: result[0]) #按照名字排序
    inner_data_pair = [i for i in sorted(values1, key=lambda x: -x[1])][:3] #按照大小排序
    print(inner_data_pair)
    c = (Pie().add("", values11, center=["50%", "50%"], is_clockwise=False,radius=["50%","70%"])
        .set_global_opts(
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="85%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", color="#000000", font_size=15))
        .set_colors(
        ["#000000", "#6495ED", "#90EE90", "#00FFFF", "#FFCC00", "#FFDEAD", "#FF0000", "#008B8B", "#7FFFD4", "#CCCC99","#FF0000","#00FFFF","#6495ED"])
        .add(
        series_name="",
        data_pair=inner_data_pair,
        radius=[0, "30%"],
        label_opts=opts.LabelOpts(position="inner"),
        center=["50%", "50%"],
    )
    )

    return render(request, 'ShowSpace/index.html', {'result': values2, 'data': c.render_embed()})
# if __name__ == "__main__":
#     g_scannedResultPath = './result'
#     import os
#
#     # 上一级目录的路径
#     path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#     path = path + r"\result"
#     result = read_05_Radar2(path, 1000000000000000)
# print(result)
# import pprint
# pprint.pprint(result)

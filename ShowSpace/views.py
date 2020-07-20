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
g_Disk_path_1 = r'\\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\01_GEN4'
g_Disk_path_2 = r'//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/05_Radar_ER'


# 换算成TB
def intoTB(data) -> str:
    return str(round(int(data) / 1024 / 1024 / 1024 / 1024, 2)) + ' TB'  # Byte --> TeraByte and leave 2 decimal places


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


def read_Disk_Usage(path):
    usage = {}
    with open(path) as f:
        usage_info = f.readline().split(";")

    usage['Total'] = intoTB(usage_info[0])
    usage['Used'] = intoTB(usage_info[1])
    usage['Free'] = intoTB(usage_info[2])
    usage['Percentage'] = round(100 - float(usage_info[3]), 2)  # unused
    usage['time'] = usage_info[4]
    return usage


def main(request):
    '''
    :param request:
    :return: dict传给html渲染
    '''
    scannedResultPath = g_scannedResultPath
    context = {}

    path1 = r".\scan\result\isilon1.txt"
    isilon1 = read_Disk_Usage(path1)

    path2 = r".\scan\result\isilon2.txt"
    isilon2 = read_Disk_Usage(path2)

    context['Drives'] = readResult(scannedResultPath, 8621420999789056)
    context['Radar_05'], diskUsage = read_05_Radar(scannedResultPath, 8621420999789056)

    context['curTime'] = datetime.datetime.now().strftime('%F %T')

    values2 = []
    values2.append(["Free Space", round(4947245995217920 // 1024 // 1024 // 1024 / 1024, 2)])
    values2.append(["Used Space", round(3674175004571136 // 1024 // 1024 // 1024 / 1024, 2)])
    c = (
        Pie(init_opts=opts.InitOpts(width="800px", height="250px"))
            .add("", values2, radius=["50%", "80%"],
                 label_opts=opts.LabelOpts(
                     position="outside",
                     formatter=" {b|{b}: }\n {c| {c}TB} ({per|{d}%}) ",
                     background_color="#FFFFFF", border_color="#000000",
                     border_width=1, border_radius=4,
                     rich={
                         "b": {"fontSize": 20, "lineHeight": 33, 'color': '#000080','align': 'center'},
                         "per": {"fontSize": 15, "lineHeight": 20, 'color': '#FF0000'},
                         "c": {'color': '#000000', "fontSize": 15, 'lineHeight': 20, 'align': 'center'}
                     },
                 ),
                 ).set_colors(['#A9A9A9', '#00BFFF']).set_global_opts(
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        ))

    return render(request, 'ShowSpace/FreeSpace.html', {'context': context, 'data': c.render_embed(),
                                                        'isilon1': isilon1, 'isilon2': isilon2})


if __name__ == "__main__":
    # path = r'//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/05_Radar_ER'
    # DiskUsage_2 = psutil.disk_usage(g_Disk_path_1)
    # print(DiskUsage_2)

    print(datetime.datetime.now().strftime('%F %T'))

    # import os
    # # 上一级目录的路径
    # path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # path = path + r"\result"

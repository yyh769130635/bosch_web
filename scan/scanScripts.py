# -*- coding: utf-8 -*-
# @Time : 7/15/2020 9:33 AM
# @Author : Peter yang

import os, time, sys, pprint
from os.path import join, getsize
import multiprocessing
import datetime
import sqlite3
import psutil
import schedule
import shutil

# ------------Variables---------------#
extendMaxLengthSymbol = r'\\?\UNC'
flag = 1  # 1表示真实环境，0为test
file_Format = ("avi", "zip", "mf4", "RIF", "htm")

# file_Format = ('py', 'html', 'bat', 'css', 'ipynb')

database_path = r".\db.sqlite3"


# database_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + r"\db.sqlite3"


# ------------/Variables--------------#
# 链接数据库
def get_conn():
    global database_path
    return sqlite3.connect(database_path)


def insert_or_update_date(sql, data):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        print("successful")
    finally:
        conn.close()


def scan_files(directory):
    start = time.time()
    cnt = [0, 0, 0, 0, 0]
    size = [0, 0, 0, 0, 0]
    others_size = 0
    others_cnt = 0
    fold_size = 0
    fold_cnt = 0
    global file_Format

    # 扫描文件夹下具体信息
    for root, sub_dirs, Files in os.walk(directory):
        for special_file in Files:
            # if postfix:
            # print(special_file)
            # temp = special_file.split('.')
            # if special_file.endswith(postfix):
            # print(temp[-1])
            # print(temp[-1] in file_Format)
            temp = special_file.split('.')[-1]
            if temp in file_Format:
                index = file_Format.index(temp)
                cnt[index] += 1
                size[index] += getsize(os.path.join(root, special_file))
                # files_list.append(os.path.join(root, special_file))
            else:
                others_cnt += 1
                others_size += getsize(os.path.join(root, special_file))
            fold_size += getsize(os.path.join(root, special_file))
            fold_cnt += 1

    result_name = directory.split("\\")[-1]
    end = time.time()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = (result_name, directory, fold_size, date, str((end - start) // 60),)

    sql = '''insert into ShowSpace_radar05 (folder_name,folder_dir,folder_size,scan_date,time_duration) 
                values(?,?,?,?,?);'''
    insert_or_update_date(sql, data)
    print("insert radar_05 total info successfully !")

    for i in range(len(file_Format)):
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = (result_name, directory, file_Format[i], cnt[i], size[i], t,)
        sql = '''insert into ShowSpace_radar05_details 
        (folder_name,folder_dir,type,number,size,scan_date) values(?,?,?,?,?,?);'''
        insert_or_update_date(sql, data)

    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = (result_name, directory, "others", others_cnt, others_size, t,)
    sql = '''insert into ShowSpace_radar05_details 
            (folder_name,folder_dir,type,number,size,scan_date) values(?,?,?,?,?,?);'''
    insert_or_update_date(sql, data)
    print("insert radar_05 details info successfully !")


def isilon():
    paths = [r"//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/01_GEN4",
             r"//abtvdfs2.de.bosch.com/ismdfs/loc/szh/DA/Radar/05_Radar_ER"]
    for i in range(len(paths)):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        isilon = psutil.disk_usage(paths[i])
        sql = '''insert into ShowSpace_isilon 
                (folder_name,folder_dir,total_space,used_space,free_space,percentage,scan_date) values(?,?,?,?,?,?,?);'''
        total_space = str(isilon.total // 1024 // 1024 // 1024) + "GB"
        used_space = str(isilon.used // 1024 // 1024 // 1024) + "GB"
        free_space = str(isilon.free // 1024 // 1024 // 1024) + "GB"
        percentage = str(isilon.percent) + "%"
        data = ("isilon{}".format(i + 1), paths[i], total_space, used_space, free_space, percentage, date)
        insert_or_update_date(sql, data)
    print("insert isilon1 and isilon2 info successfully !")


def main(files):
    ##扫描isilon1.2的整体信息
    isilon()

    ##扫描05雷达的具体信息
    for path in files:
        p = multiprocessing.Process(target=scan_files, args=(path,))
        p.start()

    # 目前所有的运行的进程
    for p in multiprocessing.active_children():
        print('subProcess: ' + p.name + ' id: ' + str(p.pid))


def foo():
    print('CPU core numbers:' + str(multiprocessing.cpu_count()))  # 查看当前机器CPU核心数量
    print("Father process start!：%d" % os.getpid())

    if flag:
        print("It's real !")
        files = [r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\00_Cluster",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\01_GAC",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\02_VW",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\03_BJEV_N61",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\04_BJEV_N60_2",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\05_Xpeng",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\06_FAW_C105",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\07_Geely",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\08_report_summary",
                 r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\09_FAW_D357"]
        main(files)
    else:
        print("It's test !")
        files = [r"C:\Users\YGP2SZH\Desktop\bosch\bosch-web",
                 r"C:\Users\YGP2SZH\Desktop\download\myProject"]
        main(files)


def ListDir(dir_data):
    '''
    :param dir_data: 指定获取内容的目录
    每次返回目录下的一个文件或文件夹(生成器练习)
    '''
    list_dir = os.listdir(dir_data)
    while True:
        try:
            list_obj = list_dir.pop()
            yield dir_data, list_obj
        except IndexError:
            return


def getFilePath():
    path = r"\\bosch.com\dfsrb\DfsDE\DIV\CS\DE_CS$\Prj\IT\Admin\1_IsilonQuotaReport"
    folders = []
    for root, obj in ListDir(path):
        dir_obj = '%s\%s' % (root, obj)
        if os.path.isfile(dir_obj):  # 文件处理
            continue
        else:  # 目录处理
            time = os.path.getmtime(dir_obj)
            folders.append([dir_obj, time])
    obj_dir = sorted(folders, key=lambda x: -x[1])[0][0]

    ans = []
    for root, obj in ListDir(obj_dir):
        if "Szh" in obj:
            temp = obj.split("_")
            t = temp[2]
            time = "20" + t[0:2] + "-" + t[2:4] + "-" + t[4:6] + " " + t[6:8] + ":" + t[8:10]
            sourcePath = '%s\%s' % (root, obj)
            ans.append([sourcePath, obj, time])
        else:
            continue
    return ans


def copyAndSave():
    ans = getFilePath()
    targets = []
    for i in ans:
        print(i)
        sourcePath = i[0]
        targetPath = '.\\scan\\'
        # fileName = "QuotaReport_" + i[1].split("_")[1] + ".txt"
        fileName = i[1]
        #targetPath2 = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\static\\" + fileName
        targetPath2 = ".\\static\\" + fileName
        targets.append([targetPath + fileName, i[2]])
        shutil.copy(sourcePath, targetPath + fileName)
        shutil.copy(sourcePath, targetPath2)
    print("copy successfully")

    # print(targetPaths)
    # 保存成特点格式的文件供读取
    for row in targets:
        file = '.\\scan\\' + row[0].split("_")[1] + ".txt"
        res = []
        with open(row[0], "r") as f:
            line = f.readline()
            while line:
                if "-->" in line:
                    temp = line.split(" ")
                    if int(temp[4].split(",")[0]) > 0:
                        res.append([temp[2], int(temp[4].split(",")[0])])
                line = f.readline()

        with open(file, "w+") as f:
            for i in res:
                f.write(i[0] + ";" + str(i[1]) + ";" + row[1] + "\n")

    print("save successfully")


def temp():
    # print("--"*10)
    print("temp")
    # print("--"*10)


def temp2():
    print("temp2")


if __name__ == "__main__":
    # copyAndSave()
    # print('CPU core numbers:' + str(multiprocessing.cpu_count()))  # 查看当前机器CPU核心数量
    # print("Father process start!：%d" % os.getpid())
    #
    # if flag:
    #     print("It's real !")
    #     files = [r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\00_Cluster",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\01_GAC",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\02_VW",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\03_BJEV_N61",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\04_BJEV_N60_2",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\05_Xpeng",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\06_FAW_C105",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\07_Geely",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\08_report_summary",
    #              r"\\?\UNC\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\09_FAW_D357"]
    #     main(files)
    # else:
    #     print("It's test !")
    #     files = [r"C:\Users\YGP2SZH\Desktop\bosch\bosch-web",
    #              r"C:\Users\YGP2SZH\Desktop\download\myProject"]
    #     main(files)

    # # 每隔3秒钟运行foo，如果有参数，直接通过args= 或者kwargs=进行传参即可
    # schedule.every(3).seconds.do(foo)
    # # 每隔1秒钟运行foo
    # schedule.every().seconds.do(foo)
    # # 每隔1分钟运行foo
    # schedule.every().minutes.do(foo)
    # # 每隔一小时运行foo
    # schedule.every().hours.do(foo)
    # # 每隔一天运行foo
    # schedule.every().days.do(foo)
    # # 每隔一星期运行foo
    # schedule.every().weeks.do(foo)
    # # 每隔3到5秒钟运行foo
    # schedule.every(3).to(5).seconds.do(foo)
    # # 每隔3到5天运行foo
    # schedule.every(3).to(5).days.do(foo)
    #
    # # 每天在10:30的时候运行foo
    # schedule.every().days.at("10:30").do(foo)
    # # 每周一的时候运行foo
    # schedule.every().monday.do(foo)
    # # 每周日晚上11点的时候运行foo
    # schedule.every().sunday.at("23:00").do(foo)

    # 每天在10:30的时候运行foo
    schedule.every().days.at("07:00").do(foo)
    schedule.every().days.at("18:00").do(foo)
    schedule.every().days.at("19:00").do(copyAndSave)
    # schedule.every().week.sunday.at("18:00").do(copyAndSave)
    #schedule.every(3).seconds.do(temp)
    #schedule.every(1).seconds.do(temp2)
    while True:
        # 保持schedule一直运行，然后去查询上面的任务
        schedule.run_pending()

    # foo()
    # print(os.getcwd())
    # isilon()

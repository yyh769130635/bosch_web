# -*- coding: utf-8 -*-
# @Time : 7/15/2020 9:33 AM
# @Author : Peter yang

import os, time, sys, pprint
from os.path import join, getsize
import multiprocessing
import datetime
import sqlite3

# ------------Variables---------------#
extendMaxLengthSymbol = r'\\?\UNC'
flag = 0  # 1表示真实环境，0为test
# file_Format = ("avi", "zip", "mf4", "RIF", "htm")


file_Format = ('py', 'html', 'bat', 'css', 'ipynb')

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


def GetDirSize(dir):
    size = 0  # 文件总大小
    # top - - 是你所要遍历的目录的地址, 返回的是一个三元组(root, dirs, files)。
    # root所指的是当前正在遍历的这个文件夹的本身的地址
    # dirs是一个list ，内容是该文件夹中所有的目录的名字(不包括子目录)
    # files同样是list, 内容是该文件夹中所有的文件(不包括子目录)
    for root, dirs, files in os.walk(dir):
        # print(root, dirs, files)
        size += sum([getsize(join(root, name)) for name in files])
    return size


def getFileInfo(dir_data):
    '''
    :param dir_data: 调用ListDir函数是所需参数
    获取目录内的每个文件或目录的属性和大小并打印
    '''
    info = {}
    for root, obj in ListDir(dir_data):
        dir_obj = '%s/%s' % (root, obj)
        if os.path.isfile(dir_obj):  # 文件处理
            '''info为字典格式，方便返回调用，此脚本只是输出内容，不涉及返回调用'''
            info['TimeCreated'] = os.path.getctime(dir_obj)  # 获取创建时间
            info['TimeModified'] = os.path.getatime(dir_obj)  # 获取访问时间
            info['Size'] = os.path.getsize(dir_obj) / 1024 / 1024  # 获取文件大小，单位为M
            if info['Size'] >= 1024:  # 文件大小换算为G
                info['Size'] = info['Size'] / 1014
                print('%-5s\t%10.2fG\t%30s\t%30s\t%-20s' % (
                    'dir', info['Size'], time.ctime(info['TimeCreated']), time.ctime(info['TimeModified']), obj))
            elif info['Size'] < 1:  # 文件大小换算问K
                info['Size'] = info['Size'] * 1024
                print('%-5s\t%10.2fK\t%30s\t%30s\t%-20s' % (
                    'dir', info['Size'], time.ctime(info['TimeCreated']), time.ctime(info['TimeModified']), obj))
            else:
                print('%-5s\t%10.2fM\t%30s\t%30s\t%-20s' % (
                    'dir', info['Size'], time.ctime(info['TimeCreated']), time.ctime(info['TimeModified']), obj))

        else:  # 目录处理
            info['TimeCreated'] = os.path.getctime(dir_obj)
            info['TimeModified'] = os.path.getatime(dir_obj)
            info['Size'] = GetDirSize(dir_obj) / 1024 / 1024

            if info['Size'] >= 1024:
                info['Size'] = info['Size'] / 1014
                print('%-5s\t%10.2fG\t%30s\t%30s\t%-20s' % (
                    'file', info['Size'], time.ctime(info['TimeCreated']), time.ctime(info['TimeModified']), obj))
            elif info['Size'] < 1:
                info['Size'] = info['Size'] * 1024
                print('%-5s\t%10.2fK\t%30s\t%30s\t%-20s' % (
                    'file', info['Size'], time.ctime(info['TimeCreated']), time.ctime(info['TimeModified']), obj))
            else:
                print('%-5s\t%10.2fM\t%30s\t%30s\t%-20s' % (
                    'dir', info['Size'], time.ctime(info['TimeCreated']), time.ctime(info['TimeModified']), obj))


def scan_files(directory):
    start = time.time()
    # files_list = []
    # print("扫描{}文件的子进程ID号: {}".format(postfix, os.getpid()))  # os.getpid()进程ID
    cnt = [0, 0, 0, 0, 0]
    size = [0, 0, 0, 0, 0]
    others_size = 0
    others_cnt = 0
    fold_size = 0
    fold_cnt = 0
    global file_Format
    # top - - 是你所要遍历的目录的地址, 返回的是一个三元组(root, dirs, files)。
    # root所指的是当前正在遍历的这个文件夹的本身的地址
    # sub_dirs是一个list ，内容是该文件夹中所有的目录的名字(不包括子目录)
    # files同样是list, 内容是该文件夹中所有的文件(不包括子目录)
    # print(directory)
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
            # elif prefix:
            #     if special_file.startswith(prefix):
            #         files_list.append(os.path.join(root, special_file))
            # else:
            #     files_list.append(os.path.join(root, special_file))
    # print("后缀为 {} 格式的文件数量有 {} 个，大小为 {}KB".format(postfix, cnt, size // 1024))
    # for i in range(len(file_Format)):
    #     print("文件类型 {} 的数量有 {} 个，大小为 {}KB".format(file_Format[i],cnt[i], size[i] // 1024))

    result_name = directory.split("\\")[-1]
    end = time.time()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = (result_name, directory, fold_size, date, str((end - start) // 60), )

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

    # # 保存扫描整个folder的信息{path,文件夹大小（GB），扫描日期，扫描时长}
    # with open(r".\result\time_record.txt", "a+") as f2:
    #     # t = datetime.datetime.now().strftime('%F %T')
    #     t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # "%Y-%m-%d %H:%M:%S"
    #     f2.write(directory + ";" + str(fold_size) + ";" + t +
    #              ";" + str((end - start) // 60) + "\n")

    # print("folder: {} size: {}GB ,scan time:{} min".format(result_name, (fold_size // 1024 // 1024 // 1024),
    #                                                        (end - start) // 60))

    # 文件夹的具体信息{文件夹，文件格式，文件数量，文件大小（GB），扫描时间}
    # with open(r".\result\radar_05_details\{}.txt".format(result_name), 'a+') as f:
    #     for i in range(len(file_Format)):
    #         # t = datetime.datetime.now().strftime('%F %T')
    #         t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         f.write(directory + ";" + str(file_Format[i]) + ";" + str(cnt[i]) + ";" +
    #                 str(size[i]) + ";" + t + "\n")
    #     f.write(
    #         directory + ";others;" + str(others_cnt) + ";" + str(
    #             others_size) + ";" + t + "\n")


def scan_files_test(directory):
    start = time.time()
    cnt = [0, 0, 0, 0, 0]
    size = [0, 0, 0, 0, 0]
    others_size = 0
    others_cnt = 0
    fold_size = 0
    fold_cnt = 0
    global file_Format
    for root, sub_dirs, Files in os.walk(directory):
        for special_file in Files:
            temp = special_file.split('.')[-1]
            if temp in file_Format:
                index = file_Format.index(temp)
                cnt[index] += 1
                size[index] += getsize(os.path.join(root, special_file))
            else:
                others_cnt += 1
                others_size += getsize(os.path.join(root, special_file))
            fold_size += getsize(os.path.join(root, special_file))
            fold_cnt += 1
    result_name = directory.split("\\")[-1]

    # 保存扫描整个folder的信息{path,文件夹大小（GB），扫描日期，扫描时长}
    end = time.time()
    with open(r".\test_result\time_record.txt", "a+") as f2:
        # t = datetime.datetime.now().strftime('%F %T')
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # "%Y-%m-%d %H:%M:%S"
        f2.write(directory + ";" + str(fold_size) + ";" + t +
                 ";" + str((end - start) // 60) + "\n")

    print("folder: {} size: {}GB ,scan time:{} min".format(result_name, (fold_size // 1024 // 1024 // 1024),
                                                           (end - start) // 60))

    # 文件夹的具体信息{文件夹，文件格式，文件数量，文件大小（GB），扫描时间}
    with open(r".\test_result\radar_05_details\{}.txt".format(result_name), 'a+') as f:
        for i in range(len(file_Format)):
            # t = datetime.datetime.now().strftime('%F %T')
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(directory + ";" + str(file_Format[i]) + ";" + str(cnt[i]) + ";" +
                    str(size[i]) + ";" + t + "\n")
        f.write(
            directory + ";others;" + str(others_cnt) + ";" + str(
                others_size) + ";" + t + "\n")


def main(files):
    for path in files:
        p = multiprocessing.Process(target=scan_files, args=(path,))
        p.start()

    # 目前所有的运行的进程
    for p in multiprocessing.active_children():
        print('subProcess: ' + p.name + ' id: ' + str(p.pid))


def main_test(files):
    for path in files:
        p = multiprocessing.Process(target=scan_files_test, args=(path,))
        p.start()

    # 目前所有的运行的进程
    for p in multiprocessing.active_children():
        print('subProcess: ' + p.name + ' id: ' + str(p.pid))


if __name__ == "__main__":
    print('CPU core numbers:' + str(multiprocessing.cpu_count()))  # 查看当前机器CPU核心数量
    print("Father process start!：%d" % os.getpid())
    ##################
    # path = r"\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER\01_GAC"
    # dir = r"\abtvdfs2.de.bosch.com\ismdfs\loc\szh\AS\000000"
    # dir = extendMaxLengthSymbol + path
    # print(dir)
    # dir = r"C:\Users\YGP2SZH\Desktop\bosch\bosch-web"
    # scan_files(dir)
    ###############
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
        # print('All the tasks are finished !!')
    else:
        print("It's test !")
        files = [r"C:\Users\YGP2SZH\Desktop\bosch\bosch-web",
                 r"C:\Users\YGP2SZH\Desktop\download\myProject"]
        main_test(files)

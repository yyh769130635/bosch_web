# -*- coding: utf-8 -*-
# @Time : 7/28/2020 11:08 AM
# @Author : Peter yang

import os
import pprint
import shutil


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
        sourcePath = i[0]
        targetPath = r'.\\'
        fileName = "QuotaReport_" + i[1].split("_")[1] + ".txt"
        targetPath2 = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\static\\" + fileName
        targets.append([targetPath + fileName, i[2]])
        shutil.copy(sourcePath, targetPath + fileName)
        shutil.copy(sourcePath, targetPath2)
    print("copy successfully")

    # print(targetPaths)
    # 保存成特点格式的文件供读取
    for row in targets:
        file = r'.\\' + row[0].split("_")[1]
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


if __name__ == "__main__":
    copyAndSave()

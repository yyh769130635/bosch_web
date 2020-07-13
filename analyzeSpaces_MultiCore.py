import os, time, multiprocessing, datetime

# ------------Variables---------------#
g_PathsToScan = './networkPaths.txt'
g_ResultFileName = 'networkPaths_ScanResult.txt'
g_ResultPath = './result'

Radar_05_path = 'loc\\szh\\DA\\Radar\\05_Radar_ER'
extendMaxLengthSymbol = '\\\\?\\'  # ->\\?\


# ------------/Variables--------------#

def getdirsize(dir):  # 5
    size = 0
    for root, dirs, files in os.walk(dir):
        # print('Scanning {}'.format(root))
        for name in files:
            try:
                size += os.path.getsize(os.path.join(root, name))
            except:
                size += 0

    return size  # Int


def write(path, fileName):
    start = time.time()

    f = open(fileName, 'a')

    size = str(getdirsize(path))
    now_time = str(datetime.datetime.now().strftime('%F %T'))

    content = ';'.join([path,
                        size,
                        now_time, ])

    f.write(content + '\n')  # Write Into Result
    f.close()

    end = time.time()
    print('{} spend {} seconds'.format(path, round(end - start, 2)))  # Calculate time used


def bindPath(ResultPath, ResultFileName):
    global g_ResultFileName
    g_ResultFileName = os.path.join(ResultPath, ResultFileName)


def extract_05_Radar(path):
    result = []

    if Radar_05_path in path:
        subdirs = os.listdir(path)

        for subdir in subdirs:
            result.append(os.path.join(path, subdir))

    return result


# 创建result文件夹
def checkResultPath(ResultPath):
    if os.path.isdir(ResultPath):
        for i in os.listdir(ResultPath):
            os.remove(os.path.join(ResultPath, i))
    else:
        os.mkdir(ResultPath)


# 这个多进程跑的，输入所有要扫描的文件夹，输出到result文件夹中
def writeFile(path, ResultPath):  # 4
    # start = time.time()
    fileName = path.strip(extendMaxLengthSymbol).replace('\\', '-') + '.txt'
    if 'UNC' in fileName:
        fileName = fileName.lstrip('UNC-')

    fileName = os.path.join(ResultPath, fileName)
    # f = open(os.path.join(ResultPath,fileName),'a')

    tmp = extract_05_Radar(path)
    if tmp == []:
        path = [path]
    else:
        path = tmp

    for p in path:
        # f.write(p + ': ' + str(getdirsize(p))+' Byte' + '\n') #Write Into Result
        multiprocessing.Process(target=write, args=(p, fileName,)).start()
    # f.close()

    # end = time.time()
    # print('{} spend {} seconds'.format(fileName,round(end-start,2))) #Calculate time used


def formatPaths(paths, symbol):  # 3
    '''
    :param paths: list
    :param symbol: str
    :return: list
    '''
    for index in range(len(paths)):
        if symbol not in paths[index]:
            if ':' in paths[index]:
                paths[index] = symbol + paths[index].rstrip(
                    ' ')  # add '\\?\' infront of path to be able to read file inside toooooo looooong path folder

            else:
                paths[index] = symbol + 'UNC\\' + paths[index].lstrip('\\\\').rstrip(
                    ' ')  # add '\\?\UNC\' infront of path for SMB path

    return paths


def readFileInLines(path):  # 2
    '''
    :param path: str路径
    :return: list
    '''
    try:
        with open(path, mode='r') as f:
            tmp = f.read().split('\n')  # List
            # tmp = open(path).read().split('\n')  # List
            for i in tmp:
                if os.path.isdir(i):
                    pass
                else:
                    tmp.remove(i)
    except:
        pass
        # if ('\\\\abtvdfs2.de.bosch.com\\ismdfs\\' in i) or ('G:\\' in i):
        #     pass
        # else:
        #     tmp.remove(i)
    return tmp


# 主函数
def run(ResultPath, PathsToScan):  # 1
    paths = readFileInLines(PathsToScan)
    # extendMaxLengthSymbol = '\\\\?\\'  # ->\\?\
    # path为给定的每一个要扫描的文件夹
    import pprint
    pprint.pprint(paths)
    # '\\\\abtvdfs2.de.bosch.com\\ismdfs\\loc\\szh\\AS\\EXT'
    paths = formatPaths(paths, extendMaxLengthSymbol)  # 头部添加了？//UNV//
    pprint.pprint(paths)
    # '\\\\?\\UNC\\abtvdfs2.de.bosch.com\\ismdfs\\loc\\szh\\AS\\EXT'
    # paths = extract_05_Radar(paths)
    for path in paths:
        print('Scanning {}'.format(path))
        multiprocessing.Process(target=writeFile,
                                args=(path, ResultPath,)).start()  # MultiProcessing Scan for each Directory

    print('\n Result will be saved in {}\n'.format(os.path.join(os.getcwd(), ResultPath)))


if __name__ == "__main__":
    # -----Initialize-----#
    checkResultPath(g_ResultPath)
    # -----/Initialize----#
    # g_PathsToScan='./networkPaths.txt' 这个是给定的文件夹
    run(g_ResultPath, g_PathsToScan)

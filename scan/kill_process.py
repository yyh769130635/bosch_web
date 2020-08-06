# -*- coding: utf-8 -*-
# @Time : 8/6/2020 10:36 AM
# @Author : Peter yang

import os, time, sys, pprint
from os.path import join, getsize
import multiprocessing, signal, psutil
from multiprocessing import Process,Queue


def hello(i):
    while True:
        time.sleep(i * 2 + 2)
        # print("This is the child process {}".format(i))
        print("This is the child process: {} number: {}".format(os.getpid(), i + 1))


if __name__ == "__main__":

    print('CPU core numbers:' + str(multiprocessing.cpu_count()))  # 查看当前机器CPU核心数量
    print("Father process start! : %d" % os.getpid())

    # q = Queue()
    # q.put(1)
    # q.put(2)
    # q.put(3)
    # p = Process(target=, args=(q,))
    # p.daemon = True  # 加上这一行代码
    # p.start()

    for i in range(3):
        p = multiprocessing.Process(target=hello, args=(i,))
        # 设置子进程的daemon属性为True。这样，当在控制台上用ctrl - c，
        # 退发送SIGTERM杀掉父进程后，子进程也会跟着退出，不会成为孤儿进程。
        p.daemon = True
        p.start()

    # 目前所有的运行的进程
    for p in multiprocessing.active_children():
        print('subProcess: ' + p.name + ' id: ' + str(p.pid))

    cnt = 0
    while cnt < 2:
        time.sleep(10)
        cnt += 1
    print("Father process end! : %d" % os.getpid())
    # 获取所有在运行的进程
    # for proc in psutil.process_iter():
    #     print("pid-%d,name:%s" % (proc.pid, proc.name()))

# -*- coding: utf-8 -*-
# @Time : 8/9/2020 8:26 PM
# @Author : Peter yang

from django.http import HttpResponse
from django.shortcuts import render
import socket


def temp():
    # 创建实例
    client = socket.socket()

    # 访问服务器端的ip和端口
    ip_port = ("SGHZ001015127", 8888)

    # 连接主机
    client.connect(ip_port)
    # 接收主机初始化的消息
    data = client.recv(1024)
    print(data.decode())

    # 发送本机消息
    msg_input = "这是一条自动发送的消息"
    client.send(msg_input.encode())
    # 接收两条消息，第一天是自己发送服务器返回的，第二条是服务器发送的
    data = client.recv(1024)
    print((data.decode()))
    res = client.recv(1024)
    res = res.decode()
    # print(res)
    # 接收完停止发送
    client.send("exit".encode())
    # 定义一个循环，不断地发送消息
    # while True:
    #     # 接收主机信息
    #     data = client.recv(1024)
    #
    #     # 打印接收的数据
    #     print(data.decode())
    #
    #     # 输入发送的消息
    #     # msg_input = input("请输入要发送的消息：")
    #     msg_input = "这是一条自动发送的消息"
    #     # 发送消息
    #     client.send(msg_input.encode())
    #     # 退出循环
    #     if msg_input == "exit":
    #         break
    #     data = client.recv(1024)
    #     print((data.decode()))
    return res


# 表单
def search_form(request):
    return render(request, './ShowSpace/search_form.html')


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = '你搜索的内容为: ' + request.GET['q']
        #print("#"*10)
        res = temp()
        print(res)
        message = message+" "*10+"服务器返回的消息："+res
        message2 = message

    else:
        message = '你提交了空表单 sb'
    return HttpResponse(message)

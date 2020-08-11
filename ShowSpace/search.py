# -*- coding: utf-8 -*-
# @Time : 8/9/2020 8:26 PM
# @Author : Peter yang

from django.http import HttpResponse
from django.shortcuts import render


# 表单
def search_form(request):
    return render(request, './ShowSpace/search_form.html')


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)
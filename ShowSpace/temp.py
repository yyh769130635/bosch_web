# -*- coding: utf-8 -*-
# @Time : 7/23/2020 4:44 PM
# @Author : Peter yang
from django.shortcuts import render


def index(request):
    return render(request, "ShowSpace/temp.html")
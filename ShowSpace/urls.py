from django.urls import path
from django.conf.urls import url
from . import views
from . import views2

urlpatterns = [
    path('', views.main),
    url(r'^1/$', views2.main)
]
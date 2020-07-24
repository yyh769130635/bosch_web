from django.urls import path
from django.conf.urls import url
from . import views
from . import isilon2
from . import isilon1
from . import temp

urlpatterns = [
    path('', views.main),
    url(r'^2/$', isilon2.main),
    url(r"^1/$", isilon1.main),
    path('detail/<str:name>', isilon2.get_details),
    url(r"^3/$", temp.index),
]

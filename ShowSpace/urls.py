from django.urls import path
from django.conf.urls import url
from . import views
from . import radar05
from . import isilon1
from . import isilon2

urlpatterns = [
    path(r'Isilon_Usage_Condition/', views.main),
    url(r'^Radar05/$', radar05.main),
    url(r"^Isilon1/$", isilon1.main),
    url(r"^Isilon2/$", isilon2.main),
    path('Radar05/<str:name>', radar05.get_details),
]

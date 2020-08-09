from django.urls import path
from django.conf.urls import url
from . import views
from . import radar05
from . import isilon1
from . import isilon2
from . import search

urlpatterns = [
    path('', views.hello),
    path(r'Isilon_Usage_Condition/', views.main),
    url(r'^Radar05/$', radar05.main),
    url(r"^Isilon1/$", isilon1.main),
    url(r"^Isilon2/$", isilon2.main),
    path('Radar05/<str:name>', radar05.get_details),
    url(r'^search-form$', search.search_form),
    url(r'^search$', search.search),
    url(r'^details2$', radar05.get_details2),
    url(r'^details3$', radar05.get_details3),
]

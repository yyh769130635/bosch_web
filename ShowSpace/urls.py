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
    path('Radar05/', radar05.main),
    url(r"^Isilon1/$", isilon1.main),
    url(r"^Isilon2/$", isilon2.main),
    path('Radar05/<str:name>', radar05.get_details),
    path("test/", search.search_form),
    path("search", search.search),
    path('hello', radar05.get_method),
    path('hello2', radar05.post_method),

]

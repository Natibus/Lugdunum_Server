from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^photoList/([0-9]+)/$', views.photoList),
    url(r'^places/$', views.placeList)
]

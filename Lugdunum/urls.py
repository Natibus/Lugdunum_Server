from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^photoList/([0-9]+)/$', views.photoList),
    url(r'^voteUpload/([0-9]+)/$', views.voteUpload),
    url(r'^recentPhotoList/([0-9]+)/$', views.recentPhotoList),
    url(r'^photoUpload/$', views.photoUpload),
    url(r'^places/([0-9]+)/$', views.placeList),
    url(r'^places/$', views.placeList)
]

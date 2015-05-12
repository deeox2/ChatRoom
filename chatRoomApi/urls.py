from django.conf.urls import patterns, include, url
from chatRoomApi import views
 
urlpatterns = patterns('', 
    url(r'^$', views.index, name='home'),
    url(r'^api', views.chatApi, name='chatApi'),
    )

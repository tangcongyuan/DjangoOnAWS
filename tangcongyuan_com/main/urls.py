from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    #url(r'^more/$', views.more, name='more'),
    #url(r'^googlec41507c3bf67fa1c.html$', views.googleWebMaster, name='GWM'),
    #url(r'^BingSiteAuth.xml$', views.bingWebMaster, name='BWM'),
]
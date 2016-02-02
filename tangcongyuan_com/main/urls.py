from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^more$', views.more, name='more'),
    url(r'^contact_me$', views.contact_me, name='contact_me'),
    url(r'^googlec41507c3bf67fa1c.html$', views.google_web_master, name='GWM'),
    url(r'^BingSiteAuth.xml$', views.bing_web_master, name='BWM'),
]

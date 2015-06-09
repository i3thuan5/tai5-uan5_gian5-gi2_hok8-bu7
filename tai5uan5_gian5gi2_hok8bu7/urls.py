from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tai5uan5_gian5gi2_hok8bu7.views.home', name='home'),
    url(r'^', include('臺灣言語服務.網址')),

    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('臺灣言語服務.網址')),

    url(r'^admin/', include(admin.site.urls)),
]

from django.conf.urls import include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path(r'', include('臺灣言語服務.網址')),

    path(r'admin/', admin.site.urls),
]

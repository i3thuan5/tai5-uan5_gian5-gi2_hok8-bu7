# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from 臺灣言語服務.服務 import 服務


__服務 = 服務()
urlpatterns = patterns(
    '',
    url(r'^正規化翻譯$', __服務.正規化翻譯),
)

# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from 臺灣言語服務.服務 import 服務
from 臺灣言語服務.模型載入 import 全部翻譯母語模型
from 臺灣言語服務.模型載入 import 全部合成母語模型
_服務 = 服務(
    全部翻譯母語模型=全部翻譯母語模型,
    全部合成母語模型=全部合成母語模型,
)
urlpatterns = patterns(
    '',
    url(r'^正規化翻譯$', _服務.正規化翻譯),
    url(r'^語音合成$', _服務.語音合成),
)

# -*- coding: utf-8 -*-
from django.conf.urls import url
from 臺灣言語服務.HTS介面 import HTS介面
from 臺灣言語服務.Moses介面 import Moses介面

_Moses = Moses介面()
_HTS = HTS介面()

urlpatterns = [
    url(r'^正規化翻譯支援腔口$', _Moses.正規化翻譯支援腔口),
    url(r'^正規化翻譯$', _Moses.正規化翻譯),
    url(r'^標漢字音標$', _Moses.標漢字音標),
    url(r'^語音合成支援腔口$', _HTS.語音合成支援腔口),
    url(r'^語音合成$', _HTS.語音合成),
]

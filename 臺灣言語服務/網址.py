# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from 臺灣言語服務.HTS介面 import HTS介面
from 臺灣言語服務.Moses介面 import Moses介面
from 臺灣言語服務.Kaldi介面 import 看辨識結果
from 臺灣言語服務.Kaldi介面 import Kaldi辨識
from 臺灣言語服務.Kaldi介面 import 看對齊結果
from 臺灣言語服務.Kaldi介面 import Kaldi對齊
from 臺灣言語服務.文本介面 import 文本介面
from 臺灣言語服務.斷詞介面 import 斷詞介面

_Moses = Moses介面()
_HTS = HTS介面()

urlpatterns = [
    url(r'^羅馬字轉換$', 文本介面.羅馬字轉換),
    url(r'^漢字音標對齊$', 文本介面.漢字音標對齊),

    url(r'^標漢字音標$', _Moses.標漢字音標),
    url(r'^標漢羅$', 斷詞介面.標漢羅),

    url(r'^正規化翻譯支援腔口$', _Moses.正規化翻譯支援腔口),
    url(r'^正規化翻譯$', _Moses.正規化翻譯),

    url(r'^語音合成支援腔口$', _HTS.語音合成支援腔口),
    url(r'^語音合成$', _HTS.語音合成),
    url(r'^文本直接合成$', _HTS.文本直接合成),

    url(r'^辨識音檔$', Kaldi辨識),
    url(r'^辨識結果$', 看辨識結果),
    url(r'^對齊音檔$', Kaldi對齊),
    url(r'^對齊結果$', 看對齊結果),
    url(r'^資料庫影音檔案/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT, 'show_indexes': False
    }),
]

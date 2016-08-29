# -*- coding: utf-8 -*-
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 臺灣言語服務.語言判斷 import 語言判斷
from 臺灣言語工具.語音合成.閩南語變調 import 閩南語變調
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.音標系統.閩南語綜合標音 import 閩南語綜合標音
from 臺灣言語工具.音標系統.客話綜合標音 import 客話綜合標音


class 公家載入:

    @classmethod
    def _語言解析拼音(cls, 語言):
        if 語言判斷.是閩南語(語言):
            return 臺灣閩南語羅馬字拼音相容教會羅馬字音標
        return cls._語言拼音(語言)

    @classmethod
    def _語言拼音(cls, 語言):
        if 語言判斷.是閩南語(語言):
            return 臺灣閩南語羅馬字拼音
        if 語言判斷.是客話(語言):
            return 臺灣客家話拼音
        return 臺灣閩南語羅馬字拼音

    @classmethod
    def _語言變調(cls, 語言):
        if 語言判斷.是閩南語(語言):
            return 閩南語變調
        return None

    @classmethod
    def _語言字綜合標音(cls, 語言):
        if 語言判斷.是閩南語(語言):
            return 閩南語綜合標音
        if 語言判斷.是客話(語言):
            return 客話綜合標音
        return None

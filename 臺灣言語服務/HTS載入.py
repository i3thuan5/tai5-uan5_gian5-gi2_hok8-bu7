# -*- coding: utf-8 -*-
from os import listdir
from os.path import join


from 臺灣言語服務.資料模型路徑 import 合成模型資料夾
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 臺灣言語服務.語言判斷 import 語言判斷
from 臺灣言語工具.語音合成.HTS工具.HTS合成模型 import HTS合成模型
from 臺灣言語工具.語音合成.閩南語變調 import 閩南語變調
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.音標系統.閩南語綜合標音 import 閩南語綜合標音
from 臺灣言語工具.音標系統.客話綜合標音 import 客話綜合標音


class HTS載入:

    @classmethod
    def HTS模型(cls):
        合成母語模型 = {}
        for 母語腔口 in sorted(listdir(合成模型資料夾)):
            合成母語模型[母語腔口] = cls.HTS合成模型(合成模型資料夾, 母語腔口)
        return 合成母語模型

    @classmethod
    def HTS合成模型(cls, 合成模型資料夾, 母語腔口):
        母語合成模型 = join(合成模型資料夾, 母語腔口, 'Taiwanese.htsvoice')
        return {
            '模型': HTS合成模型(母語合成模型),
            '拼音': cls._語言拼音(母語腔口),
            '變調': cls._語言變調(母語腔口),
        }

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

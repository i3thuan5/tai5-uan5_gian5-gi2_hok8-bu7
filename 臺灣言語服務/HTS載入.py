# -*- coding: utf-8 -*-
from os import listdir
from os.path import join


from 臺灣言語服務.資料模型路徑 import 合成模型資料夾
from 臺灣言語工具.語音合成.HTS工具.HTS合成模型 import HTS合成模型
from 臺灣言語服務.公家載入 import 公家載入


class HTS載入(公家載入):

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

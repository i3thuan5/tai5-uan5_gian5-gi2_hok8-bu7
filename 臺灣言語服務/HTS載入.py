# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile


from 臺灣言語工具.語音合成.HTS工具.HTS合成模型 import HTS合成模型
from 臺灣言語服務.公家載入 import 公家載入
from 臺灣言語服務.資料模型路徑 import 合成模型路徑
from 臺灣言語服務.資料模型路徑 import 資料路徑


class HTS載入(公家載入):

    @classmethod
    def HTS模型(cls):
        合成母語模型 = {}
        for 母語腔口 in sorted(listdir(資料路徑)):
            if isfile(合成模型路徑(母語腔口)):
                合成母語模型[母語腔口] = cls.HTS合成模型(母語腔口)
        return 合成母語模型

    @classmethod
    def HTS合成模型(cls, 母語腔口):
        return {
            '模型': HTS合成模型(合成模型路徑(母語腔口)),
            '拼音': cls._語言拼音(母語腔口),
            '變調': cls._語言變調(母語腔口),
        }

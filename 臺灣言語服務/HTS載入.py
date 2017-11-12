# -*- coding: utf-8 -*-
from os.path import isfile


from django.conf import settings
from 臺灣言語工具.語音合成.HTS工具.HTS合成模型 import HTS合成模型
from 臺灣言語服務.資料模型路徑 import 合成模型路徑


class HTS載入:

    @classmethod
    def HTS模型(cls):
        合成母語模型 = {}
        for 母語腔口 in sorted(settings.HOK8_BU7_SIAT4_TING7.keys()):
            if isfile(合成模型路徑(母語腔口)):
                合成母語模型[母語腔口] = cls.HTS合成模型(母語腔口)
        return 合成母語模型

    @classmethod
    def HTS合成模型(cls, 母語腔口):
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[母語腔口]
        try:
            音韻規則 = 服務設定['音韻規則']
        except KeyError:
            音韻規則 = None
        return {
            '語族': 服務設定['語族'],
            '模型': HTS合成模型(合成模型路徑(母語腔口)),
            '拼音': 服務設定['音標系統'],
            '音韻': 音韻規則,
            '語音標仔轉換': 服務設定['語音標仔轉換'],
        }

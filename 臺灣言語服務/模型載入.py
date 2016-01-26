# -*- coding: utf-8 -*-
from os import listdir
from os.path import join

from django.apps import AppConfig


from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾
from 臺灣言語服務.資料模型路徑 import 合成模型資料夾
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 臺灣言語服務.語言判斷 import 語言判斷
from 臺灣言語工具.語音合成.HTS工具.HTS合成模型 import HTS合成模型
from 臺灣言語工具.語音合成.閩南語變調 import 閩南語變調
from 臺灣言語工具.綜合標音.閩南語字綜合標音 import 閩南語字綜合標音
from 臺灣言語工具.綜合標音.客話字綜合標音 import 客話字綜合標音
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標


全部翻譯母語模型 = {}
全部合成母語模型 = {}


class 模型載入(AppConfig):
    name = '臺灣言語服務'
    verbose_name = "臺灣言語服務模型載入"

    def ready(self):
        try:
            self.摩西模型()
        except FileNotFoundError:
            pass
        try:
            self.HTS模型()
        except FileNotFoundError:
            pass

    def 摩西模型(self):
        for 第幾个, 母語腔口 in enumerate(sorted(listdir(翻譯模型資料夾))):
            摩西埠 = 8500 + 第幾个
            try:
                全部翻譯母語模型[母語腔口] = self.摩西翻譯模型(翻譯模型資料夾, 母語腔口, 摩西埠)
            except OSError as 錯誤:
                print(錯誤)
                continue

    @classmethod
    def 摩西翻譯模型(cls, 翻譯模型資料夾, 母語腔口, 摩西埠):
        母語翻譯模型資料夾 = join(翻譯模型資料夾, 母語腔口)
        服務 = 摩西服務端(母語翻譯模型資料夾, 埠=摩西埠)
        服務.走()

        辭典檔案 = join(母語翻譯模型資料夾, '母語辭典.txt.gz')
        母語摩西用戶端 = 摩西用戶端(埠=摩西埠, 編碼器=語句編碼器())
        母語辭典 = 型音辭典(4)
        母語辭典.加檔案的詞(辭典檔案)

        語言模型檔案 = join(母語翻譯模型資料夾, '語言模型.lm')
        母語語言模型 = KenLM語言模型(語言模型檔案)

        母語模型 = {
            '摩西用戶端': 母語摩西用戶端,
            '辭典': 母語辭典,
            '語言模型': 母語語言模型,
            '拼音': cls._語言拼音(母語腔口),
            '字綜合標音': cls._語言字綜合標音(母語腔口),
            '摩西服務': 服務,
        }
        return 母語模型

    def HTS模型(self):
        for 母語腔口 in sorted(listdir(合成模型資料夾)):
            全部合成母語模型[母語腔口] = self.HTS合成模型(合成模型資料夾, 母語腔口)

    @classmethod
    def HTS合成模型(cls, 合成模型資料夾, 母語腔口):
        母語合成模型 = join(合成模型資料夾, 母語腔口, 'Taiwanese.htsvoice')
        return {
            '模型': HTS合成模型(母語合成模型),
            '拼音': cls._語言拼音(母語腔口),
            '變調': cls._語言變調(母語腔口),
        }

    @classmethod
    def _語言拼音(cls, 語言):
        if 語言判斷.是閩南語(語言):
            return 臺灣閩南語羅馬字拼音相容教會羅馬字音標
        if 語言判斷.是客話(語言):
            return 臺灣客家話拼音
        return 臺灣閩南語羅馬字拼音相容教會羅馬字音標

    @classmethod
    def _語言變調(cls, 語言):
        if 語言判斷.是閩南語(語言):
            return 閩南語變調
        return None

    @classmethod
    def _語言字綜合標音(cls, 語言):
        if 語言判斷.是閩南語(語言):
            return 閩南語字綜合標音
        if 語言判斷.是客話(語言):
            return 客話字綜合標音
        return None

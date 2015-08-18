# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.conf import settings
from os.path import join
from os import listdir


from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


全部翻譯母語模型 = {}
全部合成母語模型 = {}


class 模型載入(AppConfig):
    name = '臺灣言語服務'
    verbose_name = "臺灣言語服務模型載入"

    def ready(self):
        self.摩西模型()
        self.HTS模型()

    def 摩西模型(self):
        翻譯模型資料夾 = join(settings.BASE_DIR, '語料', '翻譯模型')
        for 第幾个, 母語腔口 in enumerate(listdir(翻譯模型資料夾)):
            母語翻譯模型資料夾 = join(翻譯模型資料夾, 母語腔口)
            摩西埠 = 8500 + 第幾个
            服務 = 摩西服務端(母語翻譯模型資料夾, 埠=摩西埠)

            辭典檔案 = join(settings.BASE_DIR, '語料', '翻譯模型', '閩南語', '母語辭典.txt.gz')
            語言模型檔案 = join(settings.BASE_DIR, '語料', '翻譯模型', '閩南語', '語言模型.lm')
            服務.走()

            母語摩西用戶端 = 摩西用戶端(埠=摩西埠, 編碼器=語句編碼器())
            母語辭典 = 型音辭典(4)
            母語辭典.加檔案的詞(辭典檔案)
            母語連詞 = KenLM語言模型(語言模型檔案)
            母語模型 = {
                '摩西用戶端': 母語摩西用戶端,
                '辭典': 母語辭典,
                '連詞': 母語連詞,
            }
            全部翻譯母語模型[母語腔口] = 母語模型

    def HTS模型(self):
        合成模型資料夾 = join(settings.BASE_DIR, '語料', '合成模型')
        for 母語腔口 in listdir(合成模型資料夾):
            母語合成模型 = join(合成模型資料夾, 母語腔口, 'Taiwanese.htsvoice')
            全部合成母語模型[母語腔口] = {
                '模型': 母語合成模型,
                '拼音': 臺灣閩南語羅馬字拼音,
            }

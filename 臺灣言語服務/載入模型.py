# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.conf import settings
from os.path import join
from os import listdir


from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.詞物件網仔 import 詞物件網仔
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器


def 辭典加檔案的詞(辭典, 檔名):
    腳本 = 程式腳本()
    分析器 = 拆文分析器()
    網仔 = 詞物件網仔()
    for 一逝 in 腳本._讀檔案(檔名):
        for 詞物件 in 網仔.網出詞物件(分析器.轉做句物件(一逝)):
            辭典.加詞(詞物件)

全部母語模型 = {}


class 載入模型(AppConfig):
    name = '臺灣言語服務'
    verbose_name = "臺灣言語服務載入模型"

    def ready(self):
        self.走摩西模型()

    def 走摩西模型(self):
        翻譯模型資料夾 = join(settings.BASE_DIR, '語料', '翻譯模型')
        for 母語腔口 in listdir(翻譯模型資料夾):
            母語翻譯模型資料夾=join(翻譯模型資料夾,母語腔口)
            服務 = 摩西服務端(母語翻譯模型資料夾, 埠=8500)
        
            辭典檔案 = join(settings.BASE_DIR, '語料', '翻譯模型', '閩南語', '母語辭典.txt.gz')
            語言模型檔案 = join(settings.BASE_DIR, '語料', '翻譯模型', '閩南語', '語言模型.lm')
            服務.走()
    
            母語摩西用戶端 = 摩西用戶端(埠=8500, 編碼器=語句編碼器())
            母語辭典 = 型音辭典(4)
            辭典加檔案的詞(母語辭典, 辭典檔案)
            母語連詞 = KenLM語言模型(語言模型檔案)
            母語模型 = {
                '摩西用戶端': 母語摩西用戶端,
                '辭典': 母語辭典,
                '連詞': 母語連詞,
            }
            全部母語模型[母語腔口]=母語模型

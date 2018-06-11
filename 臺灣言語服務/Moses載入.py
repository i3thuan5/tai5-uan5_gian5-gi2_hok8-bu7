# -*- coding: utf-8 -*-
from os.path import join

from django.conf import settings


from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語服務.資料模型路徑 import 翻譯正規化模型資料夾


class Moses載入:

    @classmethod
    def 摩西模型(cls):
        翻譯母語模型 = {}
        for 第幾个, 母語腔口 in enumerate(sorted(
            settings.HOK8_BU7_SIAT4_TING7.keys()
        )):
            摩西埠 = 8500 + 第幾个
            try:
                翻譯母語模型[母語腔口] = cls.摩西翻譯模型(母語腔口, 摩西埠)
            except OSError as 錯誤:
                print(錯誤)
                continue
        return 翻譯母語模型

    @classmethod
    def 摩西翻譯模型(cls, 母語腔口, 摩西埠):
        母語翻譯模型資料夾 = 翻譯正規化模型資料夾(母語腔口)
        服務 = 摩西服務端(母語翻譯模型資料夾, 埠=摩西埠)
        服務.走()

        母語摩西用戶端 = 摩西用戶端(埠=摩西埠, 編碼器=語句編碼器())

        辭典檔案 = join(母語翻譯模型資料夾, '母語辭典.txt.gz')
        母語辭典 = 型音辭典(4)
        母語辭典.加檔案的詞(辭典檔案)

        語言模型檔案 = join(母語翻譯模型資料夾, '語言模型資料夾', '語言模型.lm')
        母語語言模型 = KenLM語言模型(語言模型檔案)

        服務設定 = settings.HOK8_BU7_SIAT4_TING7[母語腔口]
        語族 = 服務設定['語族']

        母語模型 = {
            '語族': 語族,
            '摩西用戶端': 母語摩西用戶端,
            '辭典': 母語辭典,
            '語言模型': 母語語言模型,
            '摩西服務': 服務,
        }

        if 語族 == '漢語':
            try:
                解析拼音 = 服務設定['解析拼音']
            except KeyError:
                解析拼音 = 服務設定['音標系統']
            母語模型.update({
                '解析拼音': 解析拼音,
                '音標系統': 服務設定['音標系統'],
                '字綜合標音': 服務設定['字綜合標音'],
            })
        return 母語模型

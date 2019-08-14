# -*- coding: utf-8 -*-
from os.path import join

from Pyro4 import expose
from django.conf import settings


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語服務.文本介面 import 文本介面
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型


class 漢羅服務:

    def __init__(self):
        self.全部模型 = {}

        for 語言 in settings.HOK8_BU7_SIAT4_TING7.keys():
            try:
                辭典檔案 = join(self.資料所在(語言), '辭典.txt.gz')
                母語辭典 = 型音辭典(4)
                母語辭典.加檔案的詞(辭典檔案)

                語言模型檔案 = join(self.資料所在(語言), '語言模型.lm')
                母語語言模型 = KenLM語言模型(語言模型檔案)
                self.全部模型[語言] = {
                    '辭典': 母語辭典,
                    '語言模型': 母語語言模型,
                }
            except OSError as 錯誤:
                print(錯誤)
                continue

    @expose
    def 支援腔口(self):
        return sorted(self.全部模型.keys())

    @expose
    def 標漢羅實作(self, 查詢腔口, 查詢語句):
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[查詢腔口]
        母語模型 = self.全部模型[查詢腔口]
        try:
            解析拼音 = 服務設定['解析拼音']
        except KeyError:
            解析拼音 = 服務設定['音標系統']
        整理後語句 = 文章粗胚.數字英文中央全加分字符號(
            查詢語句
        )
        母語章物件 = (
            拆文分析器.建立章物件(整理後語句)
            .轉音(解析拼音)
            .揣詞(拄好長度辭典揣詞, 母語模型['辭典'])
            .揀(語言模型揀集內組, 母語模型['語言模型'])
        )
        return 文本介面.章物件轉回應結果(settings.HOK8_BU7_SIAT4_TING7[查詢腔口], 母語章物件)

    def 資料所在(self, 語言):
        return join(settings.BASE_DIR, '服務資料', 語言, '標漢羅')

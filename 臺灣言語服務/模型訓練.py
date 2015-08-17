# -*- coding: utf-8 -*-
from django.conf import settings
from os import listdir, makedirs
import os
from os.path import join
import re


from 臺灣言語資料庫.輸出 import 資料輸出工具
from 臺灣言語工具.翻譯.摩西工具.摩西翻譯模型訓練 import 摩西翻譯模型訓練
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.詞物件網仔 import 詞物件網仔
from 臺灣言語工具.基本元素.公用變數 import 標點符號
from 臺灣言語工具.基本元素.公用變數 import 無音
'''
from 臺灣言語服務.模型訓練 import 模型訓練
訓練=模型訓練()
訓練.走()
'''


class 模型訓練(程式腳本):
    漢語語言 = re.compile('(臺語|台語|閩南|客家|客語|華語)')

    def __init__(self, 資料夾=join(settings.BASE_DIR, '語料')):
        self.資料夾目錄 = 資料夾

    def 走(self):
        翻譯語料資料夾 = join(self.資料夾目錄, '翻譯語料')
#         self.輸出語料(翻譯語料資料夾)
        翻譯模型資料夾 = join(self.資料夾目錄, '翻譯模型')
        self.訓練摩西翻譯模型(翻譯語料資料夾, 翻譯模型資料夾)

    def 輸出語料(self, 語料資料夾):
        語料 = 資料輸出工具()
        語料.輸出翻譯語料(語料資料夾)

    def 訓練摩西翻譯模型(self, 語料資料夾, 模型資料夾):
        makedirs(模型資料夾, exist_ok=True)
        翻譯編碼器 = 語句編碼器()  # 若用著Unicdoe擴充就需要
        for 語言 in listdir(語料資料夾):
            語言資料夾 = join(語料資料夾, 語言)
            if self.漢語語言.search(語言):
                平行華語, 平行母語, 母語語料 = self._漢語語料訓練(語言資料夾)
            else:
                平行華語, 平行母語, 母語語料 = self._一般語料訓練(語言資料夾)
#                 平行華語, 平行母語, 母語語料 = self._一般語料訓練(語言,語言資料夾)
            moses模型資料夾路徑 = os.path.join(模型資料夾, 語言)

            模型訓練 = 摩西翻譯模型訓練()
            模型訓練.訓練(
                平行華語, 平行母語, 母語語料,
                moses模型資料夾路徑,
                連紲詞長度=2,
                編碼器=翻譯編碼器,
                刣掉暫存檔=True,
            )
    _分析器 = 拆文分析器()
    _譀鏡 = 物件譀鏡()
    _網仔 = 詞物件網仔()

    def _漢語語料訓練(self, 語言資料夾):
        平行華語, 平行母語, 母語語料 = self._原始語料(語言資料夾)
        全部詞 = set()
        for 檔名 in 母語語料:
            for 一逝 in self._讀檔案(檔名):
                for 詞物件 in self._網仔.網出詞物件(self._分析器.轉做句物件(一逝)):
                    字物件 = 詞物件.內底字[0]
                    if 字物件.音 != 無音 and 字物件.型 not in 標點符號:
                        全部詞.add(詞物件)
        加工語料 = join(語言資料夾, '加工語料')
        makedirs(加工語料, exist_ok=True)
        母語辭典檔名 = join(加工語料, '母語辭典.txt.gz')
        詞文本 = []
        for 詞物件 in 全部詞:
            詞文本.append(self._譀鏡.看分詞(詞物件))
        self._陣列寫入檔案(母語辭典檔名, 詞文本)
        return 平行華語, 平行母語, 母語語料

    def _原始語料(self, 語言資料夾):
        平行華語 = [
            os.path.join(語言資料夾, '對齊外語語句.txt.gz'),
            os.path.join(語言資料夾, '對齊外語字詞.txt.gz'),
        ]
        平行母語 = [
            os.path.join(語言資料夾, '對齊母語語句.txt.gz'),
            os.path.join(語言資料夾, '對齊母語字詞.txt.gz'),
        ]
        母語語料 = [
            os.path.join(語言資料夾, '語句文本.txt.gz'),
            os.path.join(語言資料夾, '字詞文本.txt.gz'),
        ]
        return 平行華語, 平行母語, 母語語料

    def _一般語料訓練(self, 語言資料夾):
        #         '華語斷詞'
        pass

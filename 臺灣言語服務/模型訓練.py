# -*- coding: utf-8 -*-
import os
from os.path import join
from os import listdir, makedirs


from 臺灣言語資料庫.輸出 import 資料輸出工具
from 臺灣言語工具.翻譯.摩西工具.摩西翻譯模型訓練 import 摩西翻譯模型訓練
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from django.conf import settings
'''
from 臺灣言語服務.模型訓練 import 模型訓練
訓練=模型訓練()
訓練.走()
'''


class 模型訓練():

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
            平行華語 = [
                os.path.join(語言資料夾, '對齊外語語句.txt.gz'),
                os.path.join(語言資料夾, '對齊外語字詞.txt.gz'),
            ]
            平行閩南語 = [
                os.path.join(語言資料夾, '對齊母語語句.txt.gz'),
                os.path.join(語言資料夾, '對齊母語字詞.txt.gz'),
            ]
            閩南語語料 = [
                os.path.join(語言資料夾, '語句文本.txt.gz'),
                os.path.join(語言資料夾, '字詞文本.txt.gz'),
            ]
            moses模型資料夾路徑 = os.path.join(模型資料夾, 語言)

            模型訓練 = 摩西翻譯模型訓練()
            模型訓練.訓練(
                平行華語, 平行閩南語, 閩南語語料,
                moses模型資料夾路徑,
                連紲詞長度=2,
                編碼器=翻譯編碼器,
                刣掉暫存檔=True,
            )

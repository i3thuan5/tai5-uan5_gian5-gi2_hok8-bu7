# -*- coding: utf-8 -*-
from os import listdir, makedirs
from os.path import join, basename
from sys import stderr
import traceback


from 臺灣言語服務.輸出 import 資料輸出工具
from 臺灣言語工具.翻譯.摩西工具.摩西翻譯模型訓練 import 摩西翻譯模型訓練
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.基本物件.公用變數 import 標點符號
from 臺灣言語工具.基本物件.公用變數 import 無音
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型
from 臺灣言語工具.語言模型.KenLM語言模型訓練 import KenLM語言模型訓練
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾
from 臺灣言語服務.語言判斷 import 語言判斷
from 臺灣言語工具.語言模型.實際語言模型 import 實際語言模型
from 臺灣言語工具.語音辨識.HTK工具.HTK辨識模型訓練 import HTK辨識模型訓練
from 臺灣言語工具.語音辨識.文本音值對照表.閩南語文本音值表 import 閩南語文本音值表
'''
python manage.py 訓練一个語言 閩南語
python manage.py 訓練全部語言
'''


class HTK模型訓練(程式腳本):

    @classmethod
    def 走(cls):
        cls.輸出全部語料(翻譯語料資料夾)
        cls.訓練全部摩西翻譯模型(翻譯語料資料夾, 翻譯模型資料夾)

    @classmethod
    def 輸出全部語料(cls, 語料資料夾):
        語料 = 資料輸出工具()
        語料.輸出翻譯語料(語料資料夾)

    @classmethod
    def 訓練全部摩西翻譯模型(cls, 語料資料夾, 模型資料夾):
        makedirs(模型資料夾, exist_ok=True)
        for 語言 in listdir(語料資料夾):
            try:
                cls.訓練一个摩西翻譯模型(語料資料夾, 模型資料夾, 語言)
            except:
                print('{}的摩西模型訓練失敗！！'.format(語言), file=stderr)
                traceback.print_exc()
                print(file=stderr)

    @classmethod
    def 訓練一个摩西翻譯模型(cls, 語料資料夾, 模型資料夾, 語言):
        辨識語料資料夾 = join(語料資料夾, 語言)
        辨識模型資料夾路徑 = join(模型資料夾, 語言)
        makedirs(辨識模型資料夾路徑, exist_ok=True)
        音節聲韻對照檔 = join(辨識模型資料夾路徑, '聲韻對照.dict')
        with open(音節聲韻對照檔, 'w') as 檔案:
            print('\n'.join(閩南語文本音值表().音節佮聲韻對照()), file=檔案)

        原本標音辨識模型 = HTK辨識模型訓練.訓練原本標音辨識模型(
            join(辨識語料資料夾, '音檔'),
            join(辨識語料資料夾, '標仔'),
            音節聲韻對照檔,
            辨識模型資料夾路徑
        )
        原本標音辨識模型.存資料佇(辨識模型資料夾路徑)

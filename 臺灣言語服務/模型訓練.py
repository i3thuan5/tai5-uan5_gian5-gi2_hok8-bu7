# -*- coding: utf-8 -*-
from os import listdir, makedirs
from os.path import join, basename, isdir
from sys import stderr
import traceback


from 臺灣言語服務.輸出 import 資料輸出工具
from 臺灣言語工具.翻譯.摩西工具.摩西翻譯模型訓練 import 摩西翻譯模型訓練
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.基本物件.公用變數 import 標點符號
from 臺灣言語工具.基本物件.公用變數 import 無音
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型
from 臺灣言語工具.語言模型.KenLM語言模型訓練 import KenLM語言模型訓練
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語服務.語言判斷 import 語言判斷
from 臺灣言語工具.語言模型.實際語言模型 import 實際語言模型
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾
from 臺灣言語服務.資料模型路徑 import 資料路徑
'''
python manage.py 訓練一个語言 閩南語
python manage.py 訓練全部語言
'''


class 模型訓練(程式腳本):

    @classmethod
    def 走(cls):
        cls.輸出全部語料()
        cls.訓練全部摩西翻譯模型()

    @classmethod
    def 輸出全部語料(cls):
        語料 = 資料輸出工具()
        語料.輸出翻譯語料()

    @classmethod
    def 訓練全部摩西翻譯模型(cls):
        for 語言 in listdir(資料路徑):
            if isdir(翻譯語料資料夾(語言)):
                try:
                    cls.訓練一个摩西翻譯模型(語言)
                except:
                    print('{}的摩西模型訓練失敗！！'.format(語言), file=stderr)
                    traceback.print_exc()
                    print(file=stderr)

    @classmethod
    def 訓練一个摩西翻譯模型(cls, 語言):
        語料資料夾 = 翻譯語料資料夾(語言)
        模型資料夾 = 翻譯模型資料夾(語言)
        makedirs(模型資料夾, exist_ok=True)
        if 語言判斷().是漢語(語言):
            平行華語, 平行母語, 母語文本 = cls._漢語語料訓練(語料資料夾, 模型資料夾)
        else:
            平行華語, 平行母語, 母語文本 = cls._南島語語料訓練(語料資料夾, 模型資料夾)

        模型訓練 = 摩西翻譯模型訓練()
        模型訓練.訓練(
            平行華語, 平行母語, 母語文本,
            模型資料夾,
            連紲詞長度=2,
            編碼器=語句編碼器(),  # 若用著Unicdoe擴充就需要,
            刣掉暫存檔=True,
        )

    @classmethod
    def _漢語語料訓練(cls, 語言資料夾, 翻譯模型資料夾):
        平行華語, 平行母語, 母語文本 = cls._原始語料(語言資料夾)
        全部詞 = set()
        for 檔名 in 母語文本:
            for 一逝 in cls._讀檔案(檔名):
                for 詞物件 in 拆文分析器.分詞句物件(一逝).網出詞物件():
                    字物件 = 詞物件.內底字[0]
                    if 字物件.音 != 無音 and 字物件.型 not in 標點符號:
                        全部詞.add(詞物件)

        母語辭典檔名 = join(翻譯模型資料夾, '母語辭典.txt.gz')
        詞文本 = []
        母語辭典 = 型音辭典(4)
        for 詞物件 in 全部詞:
            詞文本.append(詞物件.看分詞())
            母語辭典.加詞(詞物件)
        cls._陣列寫入檔案(母語辭典檔名, 詞文本)

        加工資料夾 = join(翻譯模型資料夾, '加工語料')
        makedirs(加工資料夾, exist_ok=True)
        try:
            原始母語語言模型 = cls._文本檔轉模型物件(加工資料夾, 母語文本)
        except RuntimeError:
            原始母語語言模型 = 實際語言模型(1)
            for 檔名 in 母語文本:
                for 一逝 in cls._讀檔案(檔名):
                    原始母語語言模型.看(拆文分析器.分詞句物件(一逝))
        補漢字音標的母語文本 = cls._檔案陣列正規化(母語辭典, 原始母語語言模型, 加工資料夾, 母語文本)
        母語語言模型 = cls._文本檔轉模型物件(翻譯模型資料夾, 補漢字音標的母語文本)
        return (
            cls._檔案陣列正規化(母語辭典, 母語語言模型, 加工資料夾, 平行華語),
            cls._檔案陣列正規化(母語辭典, 母語語言模型, 加工資料夾, 平行母語),
            補漢字音標的母語文本
        )

    @classmethod
    def _檔案陣列正規化(cls, 母語辭典, 母語語言模型, 加工資料夾, 檔名陣列):
        加工了檔名陣列 = []
        for 檔名 in 檔名陣列:
            新檔名 = join(加工資料夾, basename(檔名))
            cls._陣列寫入檔案(新檔名, cls._檔案正規化(母語辭典, 母語語言模型, 檔名))
            加工了檔名陣列.append(新檔名)
        return 加工了檔名陣列

    @classmethod
    def _檔案正規化(cls, 母語辭典, 母語語言模型, 檔名):
        for 一逝 in cls._讀檔案(檔名):
            yield (
                拆文分析器.分詞句物件(一逝)
                .揣詞(拄好長度辭典揣詞, 母語辭典)
                .揀(語言模型揀集內組, 母語語言模型)
                .看分詞()
            )

    @classmethod
    def _文本檔轉模型物件(cls, 語言資料夾, 母語辭典檔名):
        模型訓練 = KenLM語言模型訓練()
        模型檔 = 模型訓練.訓練(
            母語辭典檔名,
            join(語言資料夾, '語言模型資料夾'),
            連紲詞長度=2,
            使用記憶體量='20%',
        )

        return KenLM語言模型(模型檔)

    @classmethod
    def _原始語料(cls, 語言資料夾):
        平行華語 = [
            join(語言資料夾, '對齊外語語句.txt.gz'),
            join(語言資料夾, '對齊外語字詞.txt.gz'),
        ]
        平行母語 = [
            join(語言資料夾, '對齊母語語句.txt.gz'),
            join(語言資料夾, '對齊母語字詞.txt.gz'),
        ]
        母語文本 = [
            join(語言資料夾, '語句文本.txt.gz'),
            join(語言資料夾, '字詞文本.txt.gz'),
        ]
        return 平行華語, 平行母語, 母語文本

    @classmethod
    def _南島語語料訓練(cls, 語言資料夾, 翻譯模型資料夾路徑):
        return cls._漢語語料訓練(語言資料夾, 翻譯模型資料夾)

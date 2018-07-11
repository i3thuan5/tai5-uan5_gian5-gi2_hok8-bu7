# -*- coding: utf-8 -*-
import gzip
from os import makedirs
from os.path import join, basename


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
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語服務.models import 訓練過渡格式


class Moses模型訓練(程式腳本):

    @classmethod
    def 輸出全部語料(cls, 資料夾):
        makedirs(資料夾, exist_ok=True)

        對齊語句數量 = 0
        with cls._照資料夾開壓縮檔(資料夾, '對齊母語語句.txt.gz') as 對齊母語語句:
            with cls._照資料夾開壓縮檔(資料夾, '對齊外語語句.txt.gz') as 對齊外語語句:
                for 一筆 in 訓練過渡格式.objects.filter(
                    文本__isnull=False, 外文__isnull=False,
                    種類='語句'
                ):
                    print(一筆.文本, file=對齊母語語句)
                    print(一筆.外文, file=對齊外語語句)
                    對齊語句數量 += 1

        對齊字詞數量 = 0
        with cls._照資料夾開壓縮檔(資料夾, '對齊母語字詞.txt.gz') as 對齊母語字詞:
            with cls._照資料夾開壓縮檔(資料夾, '對齊外語字詞.txt.gz') as 對齊外語字詞:
                for 一筆 in 訓練過渡格式.objects.filter(
                    文本__isnull=False, 外文__isnull=False,
                    種類='字詞'
                ):
                    print(一筆.文本, file=對齊母語字詞)
                    print(一筆.外文, file=對齊外語字詞)
                    對齊字詞數量 += 1

        語句數 = 0
        with cls._照資料夾開壓縮檔(資料夾, '語句文本.txt.gz') as 語句文本:
            for 一筆 in 訓練過渡格式.objects.filter(文本__isnull=False, 種類='語句'):
                print(一筆.文本, file=語句文本)
                語句數 += 1
        字詞數 = 0
        with cls._照資料夾開壓縮檔(資料夾, '字詞文本.txt.gz') as 字詞文本:
            for 一筆 in 訓練過渡格式.objects.filter(文本__isnull=False, 種類='字詞'):
                print(一筆.文本, file=字詞文本)
                字詞數 += 1
        return 對齊語句數量, 對齊字詞數量, 語句數, 字詞數

    @classmethod
    def _照資料夾開壓縮檔(cls, 資料夾, 檔名):
        return gzip.open(join(資料夾, 檔名), 'wt')

    @classmethod
    def 訓練翻譯做母語模型(cls, 語料資料夾, 模型資料夾):
        平行華語, 平行母語, 母語文本 = cls._原始語料(語料資料夾)
        模型訓練 = 摩西翻譯模型訓練()
        模型訓練.訓練(
            平行華語, 平行母語, 母語文本,
            模型資料夾,
            連紲詞長度=3,
            編碼器=語句編碼器(),  # 若用著Unicdoe擴充就需要,
            使用記憶體量='80%',
            愛直接顯示輸出=True,
            刣掉暫存檔=False,
        )

    @classmethod
    def 訓練翻譯做外文模型(cls, 語料資料夾, 模型資料夾):
        平行華語, 平行母語, _母語文本 = cls._原始語料(語料資料夾)
        模型訓練 = 摩西翻譯模型訓練()
        模型訓練.訓練(
            平行母語, 平行華語, 平行華語,
            模型資料夾,
            連紲詞長度=3,
            編碼器=語句編碼器(),  # 若用著Unicdoe擴充就需要,
            使用記憶體量='80%',
            愛直接顯示輸出=True,
            刣掉暫存檔=False,
        )

    @classmethod
    def 訓練正規化模型(cls, 語料資料夾, 模型資料夾):
        makedirs(模型資料夾, exist_ok=True)
        平行華語, 平行母語, 母語文本 = cls._漢語語料訓練(語料資料夾, 模型資料夾)

        模型訓練 = 摩西翻譯模型訓練()
        模型訓練.訓練(
            平行華語, 平行母語, 母語文本,
            模型資料夾,
            連紲詞長度=3,
            編碼器=語句編碼器(),  # 若用著Unicdoe擴充就需要,
            使用記憶體量='80%',
            愛直接顯示輸出=True,
            刣掉暫存檔=False,
        )

    @classmethod
    def _漢語語料訓練(cls, 語言資料夾, 翻譯模型資料夾):
        平行華語, 平行母語, 母語文本 = cls._原始語料(語言資料夾)
        全部詞 = set()
        for 檔名 in 母語文本:
            for 一逝 in cls._讀檔案(檔名):
                try:
                    句物件 = 拆文分析器.分詞句物件(一逝)
                except 解析錯誤:  # 舊的資料無一定是分詞，換做過渡就會當提掉這矣
                    try:
                        句物件 = 拆文分析器.建立句物件(一逝)
                    except 解析錯誤:
                        continue
                for 詞物件 in 句物件.網出詞物件():
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
        原始母語語言模型 = cls._文本檔轉模型物件(加工資料夾, 母語文本)
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
            try:
                句物件 = 拆文分析器.分詞句物件(一逝)
            except 解析錯誤:  # 舊的資料無一定是分詞，換做過渡就會當提掉這矣
                try:
                    句物件 = 拆文分析器.建立句物件(一逝)
                except 解析錯誤:
                    continue
            yield (
                句物件
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
            連紲詞長度=3,
            使用記憶體量='80%',
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

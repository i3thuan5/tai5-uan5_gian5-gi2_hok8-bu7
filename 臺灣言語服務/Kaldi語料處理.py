# -*- coding: utf-8 -*-
from django.db.models.query_utils import Q


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


class Kaldi語料處理():

    @classmethod
    def 揣出漢語音節種類(cls, 語句陣列):
        音 = set()
        for 逝 in 語句陣列:
            for 字物件 in 拆文分析器.分詞句物件(逝.strip()).篩出字物件():
                音.add(字物件.看音())
        return 音

    @classmethod
    def 轉fst格式(cls, 音):
        資料 = []
        for 音節 in sorted(音):
            資料.append('0\t0\t{0}｜{0}\t0'.format(音節))
        資料.append('0\t1')
        return 資料

    @classmethod
    def 匯出一種語言語料2(cls, 語言, 音標系統, 語料資料夾, 資料夾名, 辭典資料, 匯出條件=Q()):
        pass

    @classmethod
    def 匯出一種語言3語料(cls, 語言, 音標系統, 語料資料夾, 資料夾名, 辭典資料, 匯出條件=Q()):
        pass

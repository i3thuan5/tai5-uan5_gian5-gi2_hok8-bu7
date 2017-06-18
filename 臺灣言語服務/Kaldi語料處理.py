# -*- coding: utf-8 -*-

from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.基本物件.公用變數 import 分型音符號
import re


class Kaldi語料處理():

    @classmethod
    def 揣出漢語音節種類(cls, 音標系統, 語句陣列):
        音 = set()
        for 逝 in 語句陣列:
            for 字物件 in 拆文分析器.分詞句物件(逝.strip()).篩出字物件():
                if 音標系統(字物件.看音()).音標:
                    音.add(字物件.看音())
        return 音

    @classmethod
    def 轉fst格式(cls, 音陣列):
        資料 = []
        for 音節 in sorted(音陣列):
            資料.append('0\t0\t{0}{1}{0}\t{0}{1}{0}'.format(音節, 分型音符號))
        資料.append('0\t1')
        return 資料

    @classmethod
    def 轉辭典檔(cls, 音標系統, 音陣列):
        資料 = []
        for 音節 in sorted(音陣列):
            資料.append(Kaldi語料匯出.音節轉辭典格式(
                set(), {}, {},
                拆文分析器.對齊字物件(音節, 音節), 音標系統, True
            ))
        return 資料

    @classmethod
    def 轉音節text格式(cls, 音標系統, 語句陣列):
        切text = re.compile(r'([^ ]*)(.*)\Z')
        結果 = []
        for 逝 in 語句陣列:
            if 逝.strip():
                切開結果 = 切text.match(逝)
                音節逝 = [切開結果.group(1)]
                for 字物件 in 拆文分析器.分詞句物件(切開結果.group(2).strip()).篩出字物件():
                    if 音標系統(字物件.看音()).音標:
                        音節逝.append('{0}{1}{0}'.format(字物件.看音(), 分型音符號))
                結果.append(' '.join(音節逝))
        return 結果

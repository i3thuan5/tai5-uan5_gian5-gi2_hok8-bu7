# -*- coding: utf-8 -*-

from 臺灣言語工具.基本物件.公用變數 import 無音
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語服務.models import 訓練過渡格式
import re
from 臺灣言語工具.基本物件.公用變數 import 標點符號


class Kaldi語料處理():

    @classmethod
    def 揣出漢語音節種類(cls, 辭典輸出物件, 語句陣列):
        音 = set()
        for 逝 in 語句陣列:
            for 分詞 in 逝.split():
                try:
                    for 字物件 in 拆文分析器.分詞詞物件(分詞).篩出字物件():
                        if 字物件.音 != 無音:
                            if 辭典輸出物件.羅馬字系統(字物件.看音()).音標:
                                音.add(字物件.看音())
                        else:
                            if 辭典輸出物件.羅馬字系統(字物件.看型()).音標:
                                音.add(字物件.看型())
                except 解析錯誤:  # 語句名「tong0000000-0000000無註明-ku0000000」超過一e5詞
                    pass
        return 音

    @classmethod
    def 轉fst格式(cls, 辭典輸出物件, 音陣列):
        路 = set()
        for 音節 in 音陣列:
            路.add(
                '0\t0\t{1}\t{1}'.format(
                    音節, 辭典輸出物件.漢字聲韻(音節)
                )
            )
        資料 = sorted(路)
        資料.append('0\t1')
        return 資料

    @classmethod
    def 轉辭典檔(cls, 辭典輸出物件, 音陣列):
        資料 = set()
        for 音節 in sorted(音陣列):
            辭典格式, *_新聲學類 = Kaldi語料匯出.音節轉辭典格式(
                拆文分析器.對齊字物件(音節, 音節), 辭典輸出物件,
                辭典輸出物件.漢字聲韻(音節)
            )
            資料.add(辭典格式)
        return sorted(資料)

    @classmethod
    def 轉音節text格式(cls, 音標系統, 語句陣列):
        切text = re.compile(r'([^ ]*)(.*)\Z')
        結果 = []
        for 逝 in 語句陣列:
            if 逝.strip():
                切開結果 = 切text.match(逝)
                音節逝 = [切開結果.group(1)]
                for 字物件 in 拆文分析器.分詞句物件(切開結果.group(2).strip()).篩出字物件():
                    if 字物件.音 != 無音:
                        音 = 字物件.音
                    else:
                        音 = 字物件.型
                    音標物件 = 音標系統(音)
                    if 音標物件.音標:
                        音節逝.append(音標物件.聲 + 音標物件.韻)
                    elif 音 not in 標點符號:
                        音節逝.append(音)
                結果.append(' '.join(音節逝))
        return 結果

    @classmethod
    def 資料庫匯出外語辭典檔(cls, 辭典輸出物件, 輸出):
        # 匯出華字台音的lexicon
        # 母親    ʔ- a1 b- o2
        for 一筆 in 訓練過渡格式.objects.filter(外文__isnull=False, 文本__isnull=False):
            try:
                辭典格式, *_新聲學類 = Kaldi語料匯出.音節轉辭典格式(
                    拆文分析器.分詞句物件(一筆.文本),
                    辭典輸出物件, 一筆.外文
                )
                輸出.add(辭典格式)
            except ValueError:
                pass
        return sorted(輸出)

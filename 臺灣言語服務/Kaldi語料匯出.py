# -*- coding: utf-8 -*-
import json
from os import makedirs
from os.path import join


from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class Kaldi語料匯出(程式腳本):

    @classmethod
    def 匯出一種語言語料(cls, 語言, 語料資料夾):
        訓練語料資料夾 = join(語料資料夾, 'data', 'train')
        makedirs(訓練語料資料夾, exist_ok=True)
        with cls._寫檔(訓練語料資料夾, 'text') as 聽拍內容:
            with cls._寫檔(訓練語料資料夾, 'wav.scp') as 音檔目錄:
                with cls._寫檔(訓練語料資料夾, 'segments') as 語句目錄:
                    with cls._寫檔(訓練語料資料夾, 'reco2file_and_channel') as 音檔對應頻道:
                        with cls._寫檔(訓練語料資料夾, 'utt2spk') as 語句對應語者:
                            cls._揣影音輸出(語言, 聽拍內容, 音檔目錄, 語句目錄, 音檔對應頻道, 語句對應語者)

    @classmethod
    def 做音韻資料(cls, 語言文本, 語料資料夾):
        全部詞 = {'SIL\tSIL'}
        全部句 = []
        聲類 = set()
        韻類 = {}
        with open(語言文本, 'r') as 檔案:
            for 一逝 in 檔案:
                句物件 = 拆文分析器.分詞句物件(一逝.strip())
                一句 = []
                for 詞物件 in 句物件.網出詞物件():
                    try:
                        聲韻陣列 = []
                        for 字物件 in 詞物件.轉音(臺灣閩南語羅馬字拼音, '音值').篩出字物件():
                            聲, 韻, 調 = 字物件.音
                            聲韻陣列.append(聲)
                            聲韻陣列.append(韻 + 調)
                            聲類.add(聲)
                            try:
                                韻類[韻].add(韻 + 調)
                            except:
                                韻類[韻] = {韻 + 調}
                        分詞 = 詞物件.看分詞()
                        一項 = '{}\t{}'.format(分詞, ' '.join(聲韻陣列))
                        if 'iauh' in 分詞 or 'er' in 分詞 or 'ir' in 分詞:
                            continue
                        全部詞.add(一項)
                        一句.append(分詞)
    #                     print(一項)
                    except:
                        pass
                全部句.append(' '.join(一句))
        return 全部詞, 全部句

    @classmethod
    def _揣影音輸出(cls, 語言, 聽拍內容, 音檔目錄, 語句目錄, 音檔對應頻道, 語句對應語者):
        第幾个 = 0
        for 第幾个, 影音 in enumerate(
            影音表.objects
            .distinct()
            .filter(影音聽拍__isnull=False)
            .filter(語言腔口__語言腔口=語言)
        ):
            音檔名 = 'tong{0:07}'.format(第幾个)
            print(
                音檔名,
                'sox {} -b 16 -c 1 -r 16k -t wav - | '.format(影音.影音所在()),
                file=音檔目錄
            )
#             sw02001-A sw02001 A
            print(音檔名, 音檔名, 'A', file=音檔對應頻道)
            聽拍 = cls._揣上尾的聽拍(影音.影音聽拍.first().聽拍)
            for 第幾句, 一句聽拍 in enumerate(json.loads(聽拍.聽拍資料)):
                if float(一句聽拍['開始時間']) < float(一句聽拍['結束時間']):
                    if 一句聽拍['語者'] == '無註明':
                        語者 = '{0}-無註明{1:07}'.format(音檔名, 第幾句)
                    else:
                        語者 = '{}-{}'.format(音檔名, ''.join(一句聽拍['語者'].split()))
                    語句名 = '{0}-ku{1:07}'.format(音檔名, 第幾句)
                    語者 = 語句名
                    print(語句名, 一句聽拍['內容'], file=聽拍內容)
    #                 sw02001-A_000098-001156 sw02001-A 0.98 11.56
                    print(語句名, 音檔名, 一句聽拍['開始時間'], 一句聽拍['結束時間'], file=語句目錄)
                    if 一句聽拍['語者'] == '無註明':
                        print(語句名, 語句名, file=語句對應語者)
                    else:
                        print(語句名, 語者, file=語句對應語者)
        for 第幾个, 影音 in enumerate(
            影音表.objects
            .distinct()
            .filter(影音聽拍__isnull=True)
            .filter(影音文本__isnull=False)
            .filter(語言腔口__語言腔口=語言),
            start=第幾个
        ):
            cls._揣上尾的文本(影音.影音文本.first().文本)

    @classmethod
    def _揣上尾的聽拍(cls, 聽拍):
        try:
            while True:
                聽拍 = 聽拍.聽拍校對.first().新聽拍
        except:
            return 聽拍

    @classmethod
    def _揣上尾的文本(cls, 文本):
        try:
            while True:
                文本 = 文本.文本校對.first().新文本
        except:
            return 文本

    @classmethod
    def _寫檔(cls, 資料夾, 檔名):
        return open(join(資料夾, 檔名), 'w')

# -*- coding: utf-8 -*-
from itertools import chain
from os import makedirs
from os.path import join, isdir
from shutil import rmtree

from django.db.models.query_utils import Q


from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.語言模型.KenLM語言模型訓練 import KenLM語言模型訓練
from 臺灣言語工具.基本物件.公用變數 import 標點符號
from 臺灣言語工具.基本物件.公用變數 import 無音
from 臺灣言語工具.基本物件.公用變數 import 分詞符號
from 臺灣言語服務.models import 訓練過渡格式


class Kaldi語料匯出(程式腳本):
    環境噪音 = 'NSN\tNSN'

    @classmethod
    def 初使化辭典資料(cls):
        return {
            '全部詞': {'SIL\tSIL', '<UNK>\tSPN', 'SPN\tSPN'},
            '全部句': [],
            '聲類': set(),
            '韻類': {},
            '調類': {},
        }

    @classmethod
    def 匯出一種語言語料(cls, 語言, 辭典輸出物件, 語料資料夾, 資料夾名, 辭典資料, 匯出條件=Q()):
        訓練語料資料夾 = join(語料資料夾, 資料夾名, 'train')
        if isdir(訓練語料資料夾):
            rmtree(訓練語料資料夾)
        makedirs(訓練語料資料夾, exist_ok=True)
        with cls._寫檔(訓練語料資料夾, 'text') as 聽拍內容:
            with cls._寫檔(訓練語料資料夾, 'wav.scp') as 音檔目錄:
                with cls._寫檔(訓練語料資料夾, 'segments') as 語句目錄:
                    with cls._寫檔(訓練語料資料夾, 'reco2file_and_channel') as 音檔對應頻道:
                        with cls._寫檔(訓練語料資料夾, 'utt2spk') as 語句對應語者:
                            return cls._揣影音輸出(
                                辭典輸出物件,
                                聽拍內容, 音檔目錄, 語句目錄, 音檔對應頻道, 語句對應語者, 辭典資料,
                                匯出條件,
                            )

    @classmethod
    def 辭典資料載入語句文本(cls, 語言文本, 辭典輸出物件, 辭典資料, 加語料=False):
        for 一逝 in cls._讀檔案(語言文本):
            這擺參數 = {'辭典輸出物件': 辭典輸出物件, '一逝': 一逝, '加語料': 加語料}
            這擺參數.update(辭典資料)
            cls._資料加到辭典(**這擺參數)

    @classmethod
    def 匯出辭典資料(cls, 辭典資料, 語料資料夾, 資料夾名):
        訓練語料資料夾 = join(語料資料夾, 資料夾名, 'local', 'dict')
        if isdir(訓練語料資料夾):
            rmtree(訓練語料資料夾)
        makedirs(訓練語料資料夾, exist_ok=True)
        cls._陣列寫入檔案(join(訓練語料資料夾, 'optional_silence.txt'), ["SIL"])
        cls._陣列寫入檔案(join(訓練語料資料夾, 'lexicon.txt'), sorted(辭典資料['全部詞']))

        安靜噪音集 = ["SIL", "SPN"]
        if cls.環境噪音 in 辭典資料['全部詞']:
            安靜噪音集.append("NSN")
        cls._陣列寫入檔案(join(訓練語料資料夾, 'silence_phones.txt'), 安靜噪音集)

        聲韻類 = 辭典資料['聲類'].copy()
        for 仝韻 in 辭典資料['韻類'].values():
            聲韻類.add(' '.join(sorted(仝韻)))
        cls._陣列寫入檔案(join(訓練語料資料夾, 'nonsilence_phones.txt'), sorted(聲韻類))

        調問題 = {' '.join(安靜噪音集)}
        for 仝調 in 辭典資料['調類'].values():
            調問題.add(' '.join(sorted(仝調)))
        cls._陣列寫入檔案(join(訓練語料資料夾, 'extra_questions.txt'), sorted(調問題))
        return 訓練語料資料夾

    @classmethod
    def 匯出語言模型(cls, 語言文本, 連紲詞長度, 語料資料夾, 資料夾名):
        訓練語料資料夾 = join(語料資料夾, 資料夾名, 'local', 'lm')
        if isdir(訓練語料資料夾):
            rmtree(訓練語料資料夾)
        makedirs(訓練語料資料夾, exist_ok=True)
        KenLM語言模型訓練().訓練([語言文本], 訓練語料資料夾, 連紲詞長度=連紲詞長度)

    @classmethod
    def _資料加到辭典(cls, 聲類, 韻類, 調類, 全部詞, 全部句, 一逝, 辭典輸出物件, 加語料):
        章物件 = 拆文分析器.分詞章物件(一逝)
        一句 = []
        SIL數量 = 0
        NSN數量 = 0
        外來語數量 = 0
        for 詞物件 in 章物件.網出詞物件():
            分詞 = 詞物件.看分詞()
            # 換逝符號
            if len(分詞.strip()) == 0:
                continue
            try:
                辭典格式, 新聲類, 新韻類, 新調類 = cls.音節轉辭典格式(詞物件, 辭典輸出物件)
                if 加語料:
                    cls._加新聲學單位(聲類, 韻類, 調類, 新聲類, 新韻類, 新調類)
                else:
                    cls._檢查有新聲學單位無(聲類, 韻類, 調類, 新聲類, 新韻類, 新調類)
                全部詞.add(辭典格式)
            except (ValueError, RuntimeError):
                字物件陣列 = 詞物件.篩出字物件()
                if (
                    len(字物件陣列) == 1 and
                    字物件陣列[0].型 == "NSN" and
                    字物件陣列[0].音 == 無音
                ):
                    全部詞.add(cls.環境噪音)
                    NSN數量 += 1
                elif (
                    len(字物件陣列) == 1 and
                    (字物件陣列[0].型 in 標點符號 or 字物件陣列[0].型 == "'") and
                    (字物件陣列[0].音 in 標點符號 or 字物件陣列[0].音 in {無音, "'"})
                ):
                    一項 = '{}\tSIL'.format(分詞)
                    全部詞.add(一項)
                    SIL數量 += 1
                else:
                    一項 = '{}\tSPN'.format(分詞)
                    外來語數量 += 1
#                     全部詞.add(一項)
            一句.append(分詞)
        全部句.append(' '.join(一句))
        return len(一句), SIL數量, NSN數量, 外來語數量

    @classmethod
    def 音節轉辭典格式(cls, 物件, 辭典輸出物件, 詞條=None):
        新聲類 = set()
        新韻類 = set()
        新調類 = set()
        聲韻陣列 = []
        for 字物件 in 物件.篩出字物件():
            聲類, 韻類, 調類 = 辭典輸出物件.輸出函式(字物件)
            for 聲 in 聲類:
                聲韻陣列.append(聲)
                新聲類.add(聲)
            for 韻 in 韻類:
                聲韻陣列.append(韻[1])
                新韻類.add(韻)
            新調類 |= 調類
        if 詞條:
            分詞 = ''.join(詞條.split())
        else:
            分詞 = 物件.看分詞()
        辭典格式 = '{}\t{}'.format(分詞, ' '.join(聲韻陣列))
        return 辭典格式, 新聲類, 新韻類, 新調類

    @classmethod
    def _揣影音輸出(cls, 辭典輸出物件,
               聽拍內容, 音檔目錄, 語句目錄, 音檔對應頻道, 語句對應語者, 辭典資料,
               匯出條件):
        第幾个人 = 0
        語者名對應輸出名 = {}
        第幾个 = 0
        影音對應聽拍 = {}
        for 一筆 in (
            訓練過渡格式.objects
            .distinct()
            .filter(影音所在__isnull=False)
            .filter(聽拍__isnull=False)
            .filter(匯出條件)
            .order_by('pk')
        ):
            try:
                影音對應聽拍[一筆.影音所在]['聽拍'].append(一筆.聽拍)
            except KeyError:
                影音對應聽拍[一筆.影音所在] = {
                    'pk': 一筆.pk,
                    '音檔長度': 一筆.聲音檔().時間長度(),
                    '聽拍': [一筆.聽拍],
                }
        for 影音所在, 狀況, in sorted(
            影音對應聽拍.items(), key=lambda tong: tong[1]['pk']
        ):
            音檔名 = 'tong{0:07}'.format(第幾个)
            cls._音檔資訊(影音所在, 音檔名, 音檔目錄, 音檔對應頻道)
            for 第幾句, 一句聽拍 in enumerate(chain.from_iterable(狀況['聽拍'])):
                第幾个人 = cls._語句資訊(
                    辭典資料, 辭典輸出物件, 語者名對應輸出名,
                    音檔名, 狀況['音檔長度'], 第幾句, 第幾个人,
                    一句聽拍['開始時間'], 一句聽拍['結束時間'], 一句聽拍['語者'], 一句聽拍['內容'],
                    聽拍內容, 語句目錄, 語句對應語者
                )
            第幾个 += 1

        for 一筆 in (
            訓練過渡格式.objects
            .distinct()
            .filter(影音所在__isnull=False)
            .filter(文本__isnull=False)
            .filter(匯出條件)
            .order_by('pk')
        ):
            音檔名 = 'tong{0:07}'.format(第幾个)
            cls._音檔資訊(一筆.影音所在, 音檔名, 音檔目錄, 音檔對應頻道)
            音檔長度 = 一筆.聲音檔().時間長度()
            第幾个人 = cls._語句資訊(
                辭典資料, 辭典輸出物件, 語者名對應輸出名,
                音檔名, 音檔長度, 0, 第幾个人,
                0, 音檔長度, 一筆.影音語者, 一筆.文本,
                聽拍內容, 語句目錄, 語句對應語者
            )
            第幾个 += 1
        return 第幾个

    @classmethod
    def _音檔資訊(cls, 影音所在, 音檔名, 音檔目錄, 音檔對應頻道):
        print(
            音檔名,
            "sox -G '{}' -b 16 -c 1 -r 16k -t wav - | ".format(影音所在),
            file=音檔目錄
        )
#             sw02001-A sw02001 A
        print(音檔名, 音檔名, 'A', file=音檔對應頻道)

    @classmethod
    def _語句資訊(cls, 辭典資料, 辭典輸出物件, 語者名對應輸出名,
              音檔名, 音檔長度, 第幾句, 第幾个人,
              開始時間, 結束時間, 原本語者, 內容,
              聽拍內容, 語句目錄, 語句對應語者):
        開始 = float(開始時間)
        結束 = float(結束時間)
        if 0.0 <= 開始 and 開始 + 0.1 < 結束 and 結束 <= 音檔長度:
            if 原本語者 in ['', '無註明']:
                語者 = '{0:07}無註明'.format(第幾个人)
                第幾个人 += 1
            else:
                語者名 = ''.join(原本語者.split())
                try:
                    語者 = 語者名對應輸出名[語者名]
                except KeyError:
                    語者 = '{0:07}{1}'.format(第幾个人, 語者名)
                    語者名對應輸出名[語者名] = 語者
                    第幾个人 += 1
            語句名 = '{0}-{1}-ku{2:07}'.format(語者, 音檔名, 第幾句)
            這擺參數 = {'辭典輸出物件': 辭典輸出物件, '一逝': 內容, '加語料': True}
            這擺參數.update(辭典資料)
            _詞數量, _SIL數量, _NSN數量, _外來語數量 = cls._資料加到辭典(**這擺參數)
            print(語句名, 內容.replace('\n', 分詞符號).strip(), file=聽拍內容)
    #                 sw02001-A_000098-001156 sw02001-A 0.98 11.56
            print(語句名, 音檔名, 開始時間, 結束時間, file=語句目錄)
            print(語句名, 語者, file=語句對應語者)
        return 第幾个人

    @classmethod
    def _加新聲學單位(cls, 聲類, 韻類, 調類, 新聲類, 新韻類, 新調類):
        for 新聲 in 新聲類:
            聲類.add(新聲)
        for 一个音素, 一个音素調 in 新韻類:
            try:
                韻類[一个音素].add(一个音素調)
            except KeyError:
                韻類[一个音素] = {一个音素調}
        for 調, 一个音素調 in 新調類:
            try:
                調類[調].add(一个音素調)
            except KeyError:
                調類[調] = {一个音素調}

    @classmethod
    def _檢查有新聲學單位無(cls, 聲類, 韻類, 調類, 新聲類, 新韻類, 新調類):
        '調免檢查，因為韻就會檢查掉矣'
        for 新聲 in 新聲類:
            if 新聲 not in 聲類:
                raise RuntimeError('語料無這个音')
        for 一个音素, 一个音素調 in 新韻類:
            try:
                if 一个音素調 not in 韻類[一个音素]:
                    raise RuntimeError('語料無這个韻抑是調')
            except KeyError:
                raise RuntimeError('語料無這个韻抑是調')

    @classmethod
    def _寫檔(cls, 資料夾, 檔名):
        return open(join(資料夾, 檔名), 'w')

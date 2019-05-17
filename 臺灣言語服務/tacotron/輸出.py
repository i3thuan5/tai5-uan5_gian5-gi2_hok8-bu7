# -*- coding: utf-8 -*-
from os import makedirs
from os.path import join,  isdir
from shutil import rmtree
from subprocess import run, PIPE


from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.基本物件.公用變數 import 無音
from 臺灣言語工具.基本物件.公用變數 import 標點符號
from 臺灣言語服務.models import 訓練過渡格式


class Tacotron模型訓練(程式腳本):

    @classmethod
    def 輸出LJ格式(cls, 合成語料資料夾,  語者, 頻率, 音標系統):
        音檔資料夾 = join(合成語料資料夾, 'taioanoe', 'wavs')
        for 資料夾 in [音檔資料夾]:
            if isdir(資料夾):
                rmtree(資料夾)
            makedirs(資料夾)
        LJ資料 = []
        for 第幾个, 資料 in enumerate(
            訓練過渡格式.objects
            .filter(影音所在__isnull=False, 影音語者=語者, 文本__isnull=False)
        ):
            文本句物件 = 拆文分析器.分詞句物件(資料.文本).轉音(音標系統)
            for 字物件 in 文本句物件.篩出字物件():
                if 字物件.音 == 無音 and 字物件.型 not in 標點符號:
                    字物件.音 = 字物件.型
            LJ資料.append('{}|{}|{}'.format(
                'im{:07}'.format(第幾个),
                文本句物件.看型().replace('\n', ' '),
                文本句物件.看音().replace('\n', ' '),
            ))
            run([
                'ffmpeg', '-i', 資料.影音所在,
                '-acodec', 'pcm_s16le',
                '-ar', '{}'.format(頻率),
                '-ac', '1',
                '-y', join(音檔資料夾, 'im{:07}.wav'.format(第幾个)),
            ], stdout=PIPE, stderr=PIPE, check=True)

        with open(join(合成語料資料夾, 'taioanoe', 'metadata.csv'), 'wt') as tong:
            print('\n'.join(LJ資料), file=tong)

        return len(LJ資料)

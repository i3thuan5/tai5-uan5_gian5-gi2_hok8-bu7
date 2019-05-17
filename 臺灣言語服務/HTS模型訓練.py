# -*- coding: utf-8 -*-
from os import makedirs
from os.path import join, exists, isdir
from posix import listdir
from shutil import rmtree
import shutil
from subprocess import run, PIPE


from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.語音辨識.HTK工具.HTK辨識模型訓練 import HTK辨識模型訓練
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語工具.語音合成.HTS工具.訓練HTSengine模型 import 訓練HTSEngine模型
from 臺灣言語工具.基本物件.公用變數 import 無音
from 臺灣言語工具.基本物件.公用變數 import 標點符號
from 臺灣言語服務.models import 訓練過渡格式


class HTS模型訓練(程式腳本):

    @classmethod
    def 輸出語料(cls, 合成語料資料夾,  語者, 頻率, 音標系統, 音韻規則, 語音標仔轉換):
        音檔資料夾 = join(合成語料資料夾, '音檔')
        孤音標仔資料夾 = join(合成語料資料夾, '孤音標仔')
        相依標仔資料夾 = join(合成語料資料夾, '相依標仔')
        for 資料夾 in [音檔資料夾, 孤音標仔資料夾, 相依標仔資料夾]:
            if isdir(資料夾):
                rmtree(資料夾)
            makedirs(資料夾)
        全部音值 = set()
        for 第幾个, 資料 in enumerate(
            訓練過渡格式.objects
            .filter(影音所在__isnull=False, 影音語者=語者, 文本__isnull=False)
        ):
            文本句物件 = 拆文分析器.分詞句物件(資料.文本).轉音(音標系統)
            for 字物件 in 文本句物件.篩出字物件():
                if 字物件.音 == 無音 and 字物件.型 not in 標點符號:
                    字物件.音 = 字物件.型
            音值句物件 = 文本句物件.轉音(音標系統, '音值')
            if 音韻規則 is not None:
                實際音句物件 = 音值句物件.做(音韻規則, '套用')
            else:
                實際音句物件 = 音值句物件
            相依標仔陣列 = 語音標仔轉換.物件轉完整合成標仔(實際音句物件)
            孤音標仔陣列 = 語音標仔轉換.提出標仔陣列主要音值(相依標仔陣列)
            全部音值 |= set(孤音標仔陣列)

            cls._陣列寫入檔案(join(孤音標仔資料夾, 'im{:07}.lab'.format(第幾个)), 孤音標仔陣列)
            cls._陣列寫入檔案(join(相依標仔資料夾, 'im{:07}.lab'.format(第幾个)), 相依標仔陣列)
            run([
                'ffmpeg', '-i', 資料.影音所在,
                '-acodec', 'pcm_s16le',
                '-ar', '{}'.format(頻率),
                '-ac', '1',
                '-y', join(音檔資料夾, 'im{:07}.wav'.format(第幾个)),
            ], stdout=PIPE, stderr=PIPE, check=True)
        音節聲韻對照檔 = join(合成語料資料夾, '聲韻對照.dict')
        聲韻對照 = ['{0}\t{0}'.format(音值) for 音值 in sorted(全部音值)]
        cls._陣列寫入檔案(音節聲韻對照檔, 聲韻對照)

    @classmethod
    def 對齊聲韻(cls, 合成語料資料夾, 辨識模型資料夾路徑):
        makedirs(辨識模型資料夾路徑, exist_ok=True)
        聲韻對照檔 = join(合成語料資料夾, '聲韻對照.dict')

        對齊聲韻 = HTK辨識模型訓練.快速對齊聲韻(
            join(合成語料資料夾, '音檔'),
            join(合成語料資料夾, '孤音標仔'),
            聲韻對照檔,
            join(辨識模型資料夾路徑, 'HTK對齊標仔過程'),
        )
        return 對齊聲韻

    @classmethod
    def 輸出HTS標仔問題音檔而且訓練(cls, 合成語料資料夾, 對齊聲韻結果資料夾, 合成模型資料夾路徑, 決策樹仔):
        HTS訓練過程目錄 = cls._細項目錄(合成模型資料夾路徑, 'HTS訓練過程')
        HTS資料目錄 = cls._細項目錄(HTS訓練過程目錄, 'data')
        HTS標仔目錄 = cls._細項目錄(HTS資料目錄, 'labels')
        HTS孤音標仔目錄 = join(HTS標仔目錄, 'mono')
        HTS相依標仔目錄 = join(HTS標仔目錄, 'full')
        for 來源, 目標 in [
            (對齊聲韻結果資料夾, HTS孤音標仔目錄),
            (join(合成語料資料夾, '相依標仔'), HTS相依標仔目錄),
        ]:
            if exists(目標):
                shutil.rmtree(目標)
            shutil.copytree(來源, 目標)

        HTS試驗標仔目錄 = cls._細項目錄(HTS標仔目錄, 'gen')
        for 檔名 in listdir(HTS相依標仔目錄)[:10]:
            來源完整標仔 = join(HTS相依標仔目錄, 檔名)
            目標完整標仔 = join(HTS試驗標仔目錄, 檔名)
            shutil.copy(來源完整標仔, 目標完整標仔)

        print('    2.HTS愛分類標仔，所以愛決策樹仔的問題')
        問題 = 決策樹仔.生()
        HTS問題目錄 = cls._細項目錄(HTS資料目錄, 'questions')
        HTS問題檔案 = join(HTS問題目錄, 'questions_qst001.hed')
        cls._陣列寫入檔案(HTS問題檔案, 問題)

        print('    3.HTS愛無檔頭的音標，所以愛提掉檔頭')
        HTS原始檔目錄 = join(HTS資料目錄, 'raw')
        if exists(HTS原始檔目錄):
            shutil.rmtree(HTS原始檔目錄)
        makedirs(HTS原始檔目錄, exist_ok=True)
        全部頻率 = set()
        音檔目錄 = join(合成語料資料夾, '音檔')
        for 檔名 in listdir(音檔目錄):
            if 檔名.endswith('wav'):
                音檔檔名 = join(音檔目錄, 檔名)
                音檔 = 聲音檔.對檔案讀(音檔檔名)
                with open(join(HTS原始檔目錄, 檔名[:-4] + '.raw'), 'wb') as 原始檔:
                    原始檔.write(音檔.wav音值資料())

                if 音檔.幾个聲道 != 1 or 音檔.一點幾位元組 != 2:
                    raise RuntimeError('音標愛單聲道，逐的點愛兩位元組的整數')
                全部頻率.add(音檔.一秒幾點)
        if len(全部頻率) > 1:
            raise RuntimeError('音檔的取樣頻率愛仝款！！有{0}Hz'.format(
                '、'.join([str(頻率) for 頻率 in sorted(全部頻率)])
            ))
        頻率 = 全部頻率.pop()
        return 訓練HTSEngine模型.訓練(HTS訓練過程目錄, 頻率)

    @classmethod
    def _揣上尾的文本(cls, 文本):
        try:
            while True:
                文本 = 文本.文本校對.first().新文本
        except AttributeError:
            return 文本

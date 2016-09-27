# -*- coding: utf-8 -*-
from os import makedirs
from os.path import join, exists, basename
from posix import listdir
import shutil


from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.語音辨識.HTK工具.HTK辨識模型訓練 import HTK辨識模型訓練
from 臺灣言語工具.語音辨識.文本音值對照表.閩南語文本音值表 import 閩南語文本音值表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語工具.語音辨識.漢語轉辨識標仔 import 漢語轉辨識標仔
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語資料庫.資料模型 import 資料屬性表
from 臺灣言語工具.語音合成.決策樹仔問題.閩南語決策樹仔 import 閩南語決策樹仔
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 臺灣言語工具.語音辨識.文本音值對照表.客家話文本音值表 import 客家話文本音值表
from 臺灣言語工具.語音合成.決策樹仔問題.客家話決策樹仔 import 客家話決策樹仔
from 臺灣言語工具.音標系統.官話.官話注音符號 import 官話注音符號
from 臺灣言語工具.語音辨識.文本音值對照表.官話文本音值表 import 官話文本音值表
from 臺灣言語工具.語音合成.決策樹仔問題.官話決策樹仔 import 官話決策樹仔
from 臺灣言語工具.語音合成.語音標仔轉換 import 語音標仔轉換
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔


class HTS模型訓練(程式腳本):

    @classmethod
    def 輸出一種語言語料(cls, 合成語料資料夾, 語言, 語者):
        音標系統 = 臺灣閩南語羅馬字拼音
        音檔 = join(合成語料資料夾, '音檔')
        標仔 = join(合成語料資料夾, '音值標仔')
        合成標仔 = join(合成語料資料夾, '相依標仔')
        makedirs(音檔, exist_ok=True)
        makedirs(標仔, exist_ok=True)
        makedirs(合成標仔, exist_ok=True)
        for 第幾个, 影音 in enumerate(
            影音表.objects
            .distinct()
            .filter(影音文本__isnull=False)
            .filter(語言腔口__語言腔口=語言)
            .filter(屬性=資料屬性表.揣屬性('語者', 語者))
        ):
            文本 = cls._揣上尾的文本(影音.影音文本.first().文本)
            句物件 = 拆文分析器.分詞句物件(文本.文本佮音標格式化資料()).轉音(音標系統)
            標 = '\n'.join(
                漢語轉辨識標仔
                .物件轉音節標仔(
                    句物件,
                    音標系統
                )
            )
            合成標 = '\n'.join(
                語音標仔轉換.物件轉完整合成標仔(
                    句物件.轉音(音標系統, '音值')
                )
            )
            with open(join(標仔, 'im{:07}.lab'.format(第幾个)), 'w') as 目標txt檔案:
                print(標, file=目標txt檔案)
            with open(join(合成標仔, 'im{:07}.lab'.format(第幾个)), 'w') as 目標txt檔案:
                print(合成標, file=目標txt檔案)
            with open(join(音檔, 'im{:07}.wav'.format(第幾个)), 'wb') as 目標wav檔案:
                影音資料 = 影音.影音資料
                影音資料.open()
                目標wav檔案.write(影音資料.read())
                影音資料.close()

    @classmethod
    def 對齊聲韻(cls, 合成語料資料夾, 辨識模型資料夾路徑):
        makedirs(辨識模型資料夾路徑, exist_ok=True)
        音節聲韻對照檔 = join(辨識模型資料夾路徑, '聲韻對照.dict')
        with open(音節聲韻對照檔, 'w') as 檔案:
            print('\n'.join(閩南語文本音值表().音節佮聲韻對照()), file=檔案)

        對齊聲韻 = HTK辨識模型訓練.快速對齊聲韻(
            join(合成語料資料夾, '音檔'),
            join(合成語料資料夾, '音值標仔'),
            音節聲韻對照檔,
            join(辨識模型資料夾路徑, 'HTK對齊標仔過程'),
        )
        return 對齊聲韻

    @classmethod
    def 輸出HTS標仔(cls, 合成語料資料夾, 對齊聲韻結果資料夾, 合成模型資料夾路徑):
        if True:
            語言拼音 = 臺灣閩南語羅馬字拼音
            文本音值表 = 閩南語文本音值表
            決策樹仔 = 閩南語決策樹仔
        elif True:
            語言拼音 = 臺灣客家話拼音
            文本音值表 = 客家話文本音值表
            決策樹仔 = 客家話決策樹仔
        elif True:
            語言拼音 = 官話注音符號
            文本音值表 = 官話文本音值表
            決策樹仔 = 官話決策樹仔
        HTS資料目錄 = cls._細項目錄(合成模型資料夾路徑, 'HTS訓練過程')
        HTS標仔目錄 = cls._細項目錄(HTS資料目錄, 'labels')
        HTS音值標仔目錄 = join(HTS標仔目錄, 'mono')
        HTS完整標仔目錄 = join(HTS標仔目錄, 'full')
        for 來源, 目標 in [
            (對齊聲韻結果資料夾, HTS音值標仔目錄),
            (join(合成語料資料夾, '相依標仔'), HTS完整標仔目錄),
        ]:
            if exists(目標):
                shutil.rmtree(目標)
            shutil.copytree(來源, 目標)

        HTS試驗標仔目錄 = cls._細項目錄(HTS標仔目錄, 'gen')
        for 檔名 in listdir(HTS完整標仔目錄)[:10]:
            來源完整標仔 = join(HTS完整標仔目錄, 檔名)
            目標完整標仔 = join(HTS試驗標仔目錄, 檔名)
            shutil.copy(來源完整標仔, 目標完整標仔)

        print('    2.HTS愛分類標仔，所以愛決策樹仔的問題')
        問題 = 決策樹仔.生()
        HTS問題目錄 = cls._細項目錄(HTS資料目錄, 'questions')
        HTS問題檔案 = join(HTS問題目錄, 'questions_qst001.hed')
        cls._陣列寫入檔案(HTS問題檔案, 問題)

        print('    3.HTS愛無檔頭的音標，所以愛提掉檔頭')
        HTS原始檔目錄 = cls._細項目錄(HTS資料目錄, 'raw')
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
            raise('音檔的取樣頻率愛仝款！！有{0}Hz'.format('、'.join(sorted(全部頻率))))
        頻率 = 全部頻率.pop()

        '走HTS'
        音框長度 = 頻率 // 40
        音框移動 = 音框長度 // 5
        if 頻率 < 20000:
            參數量 = 24
        else:
            參數量 = 40
        HTS設定指令 = (
            '''LANG=C ./configure --with-sptk-search-path={0} \
--with-hts-search-path={1} \
--with-hts-engine-search-path={2} \
LOWERF0=60 UPPERF0=500 SAMPFREQ={3} FRAMELEN={4} FRAMESHIFT={5} \
USEGV=0\
GAMMA=3 LNGAIN=1 MGCORDER={6} 
'''
        ).format(
            SPTK執行檔路徑, HTS執行檔路徑, HTS_ENGINE執行檔路徑,
            頻率, 音框長度, 音框移動, 參數量
        )
        cls._走指令(HTS設定指令)
        HTS走指令 = 'LANG=C make all'
        cls._走指令(HTS走指令)

    @classmethod
    def _揣上尾的文本(cls, 文本):
        try:
            while True:
                文本 = 文本.文本校對.first().新文本
        except:
            return 文本

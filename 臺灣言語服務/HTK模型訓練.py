# -*- coding: utf-8 -*-
from os import listdir, makedirs
from os.path import join
from sys import stderr
import traceback


from 臺灣言語服務.輸出 import 資料輸出工具
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾
from 臺灣言語工具.語音辨識.HTK工具.HTK辨識模型訓練 import HTK辨識模型訓練
from 臺灣言語工具.語音辨識.文本音值對照表.閩南語文本音值表 import 閩南語文本音值表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語工具.語音辨識.漢語轉辨識標仔 import 漢語轉辨識標仔
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class HTK模型訓練(程式腳本):

    @classmethod
    def 走全部(cls):
        cls.輸出全部語料(翻譯語料資料夾)
        cls.訓練全部辨識模型(翻譯語料資料夾, 翻譯模型資料夾)

    @classmethod
    def 輸出全部語料(cls, 語料資料夾):
        語料 = 資料輸出工具()
        語料.輸出翻譯語料(語料資料夾)

    @classmethod
    def 訓練全部辨識模型(cls, 語料資料夾, 模型資料夾):
        makedirs(模型資料夾, exist_ok=True)
        for 語言 in listdir(語料資料夾):
            try:
                cls.訓練一个辨識模型(語料資料夾, 模型資料夾, 語言)
            except:
                print('{}的HTK辨識模型訓練失敗！！'.format(語言), file=stderr)
                traceback.print_exc()
                print(file=stderr)

    @classmethod
    def 輸出一種語言語料(cls, 語料資料夾, 語言):
        辨識語料資料夾 = join(語料資料夾, 語言)
        音檔 = join(辨識語料資料夾, '音檔')
        標仔 = join(辨識語料資料夾, '標仔')
        makedirs(音檔, exist_ok=True)
        makedirs(標仔, exist_ok=True)
        for 第幾个, 影音 in enumerate(
            影音表.objects
            .distinct()
            .filter(影音文本__isnull=False)
            .filter(語言腔口__語言腔口=語言)
        ):
            文本 = cls._揣上尾的文本(影音.影音文本.first().文本)
            標 = '\n'.join(
                漢語轉辨識標仔
                .物件轉音節標仔(
                    拆文分析器.分詞句物件(文本.文本佮音標格式化資料()),
                    臺灣閩南語羅馬字拼音
                )
            )
            with open(join(標仔, 'im{:07}.lab'.format(第幾个)), 'w') as 目標txt檔案:
                print(標, file=目標txt檔案)
            with open(join(音檔, 'im{:07}.wav'.format(第幾个)), 'wb') as 目標wav檔案:
                影音資料 = 影音.原始影音資料
                影音資料.open()
                目標wav檔案.write(影音資料.read())
                影音資料.close()

    @classmethod
    def 訓練一个辨識模型(cls, 語料資料夾, 模型資料夾, 語言):
        辨識語料資料夾 = join(語料資料夾, 語言)
        辨識模型資料夾路徑 = join(模型資料夾, 語言)
        makedirs(辨識模型資料夾路徑, exist_ok=True)
        音節聲韻對照檔 = join(辨識模型資料夾路徑, '聲韻對照.dict')
        with open(音節聲韻對照檔, 'w') as 檔案:
            print('\n'.join(閩南語文本音值表().音節佮聲韻對照()), file=檔案)

        原本標音辨識模型 = HTK辨識模型訓練.訓練原本標音辨識模型(
            join(辨識語料資料夾, '音檔'),
            join(辨識語料資料夾, '標仔'),
            音節聲韻對照檔,
            辨識模型資料夾路徑
        )
        原本標音辨識模型.存資料佇(辨識模型資料夾路徑)

    @classmethod
    def _揣上尾的文本(cls, 文本):
        try:
            while True:
                文本 = 文本.文本校對.first().新文本
        except:
            return 文本

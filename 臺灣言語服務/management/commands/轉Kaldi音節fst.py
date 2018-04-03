from os import makedirs
from os.path import join

from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class Command(BaseCommand, 程式腳本):
    help = '照kaldi格式匯出語料'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='選擇語料的語言'
        )
        parser.add_argument(
            '辭典輸出函式',
            type=str,
            help='選擇lexicon佮聲學單位格式'
        )
        parser.add_argument(
            '語言文本',
            type=str,
            help='選擇語料的語言文本'
        )
        parser.add_argument(
            '匯出路徑',
            type=str,
            help='kaldi的egs內底的s5資料夾'
        )
        parser.add_argument(
            '--資料夾',
            type=str,
            dest='資料夾名',
            default='data',
            help='s5底下的資料夾名',
        )

    def handle(self, *args, **參數):
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[參數['語言']]
        辭典輸出物件 = 辭典輸出(服務設定['音標系統'], 參數['辭典輸出函式'])
        漢語音節 = Kaldi語料處理.揣出漢語音節種類(
            辭典輸出物件,
            self._讀檔案(參數['語言文本'])
        )
        資料夾 = join(參數['匯出路徑'], 參數['資料夾名'], 'local', 'free-syllable')
        makedirs(資料夾, exist_ok=True)
        self._陣列寫入檔案(
            join(資料夾, 'uniform.fst'),
            Kaldi語料處理.轉fst格式(辭典輸出物件, 漢語音節)
        )
        self._陣列寫入檔案(
            join(資料夾, 'lexicon.txt'),
            Kaldi語料處理.轉辭典檔(辭典輸出物件, 漢語音節)
        )

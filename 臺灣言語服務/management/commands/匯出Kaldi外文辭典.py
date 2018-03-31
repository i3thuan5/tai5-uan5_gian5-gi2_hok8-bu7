from os import makedirs
from os.path import join

from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class Command(BaseCommand, 程式腳本):
    help = '從資料庫匯出kaldi格式的外文辭典'

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
            '匯出路徑',
            type=str,
            help='kaldi的egs內底的s5資料夾'
        )

    def handle(self, *args, **參數):
        資料夾 = 參數['匯出路徑']
        makedirs(資料夾, exist_ok=True)
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[參數['語言']]
        辭典輸出物件 = 辭典輸出(服務設定['音標系統'], 參數['辭典輸出函式'])

        self._陣列寫入檔案(
            join(資料夾, 'lexicon.txt'),
            Kaldi語料處理.資料庫匯出外語辭典檔(
                辭典輸出物件,
                Kaldi語料匯出.初使化辭典資料()['全部詞']
            )
        )

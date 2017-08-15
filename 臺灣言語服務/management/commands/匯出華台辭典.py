from os import makedirs
from os.path import join

from django.core.management.base import BaseCommand
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出


class Command(BaseCommand, 程式腳本):
    help = '從資料庫匯出kaldi格式的華台辭典'

    def add_arguments(self, parser):
        parser.add_argument(
            '匯出路徑',
            type=str,
            help='kaldi的egs內底的s5資料夾'
        )

    def handle(self, *args, **參數):
        資料夾 = 參數['匯出路徑']
        makedirs(資料夾, exist_ok=True)
        self._陣列寫入檔案(
            join(資料夾, 'lexicon.txt'),
            Kaldi語料處理.資料庫匯出外語辭典檔(
                Kaldi語料匯出.初使化辭典資料()['全部詞']
            )
        )

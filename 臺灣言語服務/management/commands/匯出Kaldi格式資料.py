from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class Command(BaseCommand):
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
            choices=[
                mia
                for mia in dir(辭典輸出)
                if (
                    callable(getattr(辭典輸出, mia)) and
                    not mia.startswith("_") and
                    mia != '漢字聲韻'
                )
            ],
            help='選擇lexicon佮聲學單位格式'
        )
        parser.add_argument(
            '--語言文本',
            type=str,
            help='選擇語料的語言文本，產生lexicon辭典'
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
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        語言 = 參數['語言']
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]
        辭典輸出物件 = 辭典輸出(服務設定['音標系統'], 參數['辭典輸出函式'])
        幾段音檔 = Kaldi語料匯出.匯出一種語言語料(
            語言, 辭典輸出物件,
            參數['匯出路徑'], 參數['資料夾名'], 辭典資料
        )
        if 參數['語言文本'] is not None:
            Kaldi語料匯出.辭典資料載入語句文本(參數['語言文本'], 辭典輸出物件, 辭典資料)
        Kaldi語料匯出.匯出辭典資料(辭典資料, 參數['匯出路徑'], 參數['資料夾名'])
        self.stdout.write('輸出 {} 段音檔'.format(幾段音檔))

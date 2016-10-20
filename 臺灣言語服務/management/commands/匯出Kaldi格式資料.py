from sys import stderr

from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出


class Command(BaseCommand):
    help = '照kaldi格式匯出語料'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            nargs='+',
            help='選擇語料的語言'
        )
        parser.add_argument(
            '--語言文本',
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
        parser.add_argument(
            '--輸出試驗音檔',
            dest='輸出試驗音檔',
            default=False,
            action='store_const',
            const=True,
        )

    def handle(self, *args, **參數):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        for 語言 in 參數['語言']:
            try:
                服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]
                Kaldi語料匯出.匯出一種語言語料(
                    語言, 服務設定['音標系統'], 參數['輸出試驗音檔'],
                    參數['匯出路徑'], 參數['資料夾名'], 辭典資料
                )
            except FileNotFoundError:
                print('資料庫無「{}」的語料！！'.format(語言), file=stderr)
        if not 參數['輸出試驗音檔']:
            if 參數['語言文本'] is not None:
                服務設定 = settings.HOK8_BU7_SIAT4_TING7[參數['語言'][0]]
                Kaldi語料匯出.辭典資料載入語句文本(參數['語言文本'], 服務設定['音標系統'], 辭典資料)
                Kaldi語料匯出.匯出語言模型(參數['語言文本'], 參數['匯出路徑'], 參數['資料夾名'])
            Kaldi語料匯出.匯出辭典資料(辭典資料, 參數['匯出路徑'], 參數['資料夾名'])

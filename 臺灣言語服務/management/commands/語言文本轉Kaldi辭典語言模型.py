from sys import stderr

from django.core.management.base import BaseCommand
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出


class Command(BaseCommand):
    help = '照kaldi格式匯出語料'

    def add_arguments(self, parser):
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
        try:
            Kaldi語料匯出.做語言模型(參數['語言文本'], 參數['匯出路徑'], 參數['資料夾名'])
            Kaldi語料匯出.做辭典資料(參數['語言文本'], 參數['匯出路徑'], 參數['資料夾名'])
        except FileNotFoundError:
            print('揣無「{}」的語料！！'.format(參數['語言文本']), file=stderr)

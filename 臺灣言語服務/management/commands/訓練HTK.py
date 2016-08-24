from os.path import join
from sys import stderr

from django.core.management.base import BaseCommand
from 臺灣言語服務.HTK模型訓練 import HTK模型訓練
from 臺灣言語服務.資料模型路徑 import 資料模型路徑


class Command(BaseCommand):
    help = '訓練一个語言的HTK模型'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='愛訓練的語言'
        )

    def handle(self, *args, **參數):
        try:
            語言 = 參數['語言']
            語料資料夾 = join(資料模型路徑, 語言, 'HTK語料')
            模型資料夾 = join(資料模型路徑, 語言, 'HTK模型')
            HTK模型訓練.輸出一種語言語料(語料資料夾, 語言)
            HTK模型訓練.訓練一个辨識模型(語料資料夾, 模型資料夾, 語言)
        except FileNotFoundError:
            print('資料庫無「{}」的語料！！'.format(參數['語言']), file=stderr)

from django.core.management.base import BaseCommand
from 臺灣言語工具.翻譯.摩西工具.安裝摩西翻譯佮相關程式 import 安裝摩西翻譯佮相關程式
from 臺灣言語服務.模型訓練 import 模型訓練
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾
from sys import stderr


class Command(BaseCommand):
    help = '訓練一个語言的模型'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='愛訓練的語言'
        )

    def handle(self, *args, **參數):
        安裝摩西翻譯佮相關程式.安裝gizapp()
        安裝摩西翻譯佮相關程式.安裝moses(編譯CPU數=4)
        模型訓練.輸出全部語料(翻譯語料資料夾)
        try:
            模型訓練.訓練一个摩西翻譯模型(翻譯語料資料夾, 翻譯模型資料夾, 參數['語言'])
        except FileNotFoundError:
            print('資料庫無「{}」的語料！！'.format(參數['語言']), file=stderr)

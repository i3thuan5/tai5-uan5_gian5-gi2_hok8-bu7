from sys import stderr
import traceback

from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語工具.翻譯.摩西工具.安裝摩西翻譯佮相關程式 import 安裝摩西翻譯佮相關程式
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾


class Command(BaseCommand):
    help = (
        '訓練Moses模型，會當選愛訓練啥物語言抑是全部語言的。\n'
        '裝Moses程式，掠而且編譯，可能愛半點鐘以上'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='輸出的語言資料夾名'
        )
        parser.add_argument(
            '--編譯核心數',
            dest='核心數',
            default=4,
            type=int,
        )

    def handle(self, *args, **參數):
        安裝摩西翻譯佮相關程式.安裝gizapp()
        安裝摩西翻譯佮相關程式.安裝moses(編譯CPU數=參數['核心數'])
        語言 = 參數['語言']
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]
        Moses模型訓練.輸出全部語料(翻譯語料資料夾(語言))
        try:
            Moses模型訓練.訓練翻譯做母語模型(語言, 服務設定['語族'])
        except FileNotFoundError:
            print('訓練時發生問題！！', file=stderr)
            traceback.print_exc()
            print(file=stderr)

from sys import stderr
import traceback

from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語工具.翻譯.摩西工具.安裝摩西翻譯佮相關程式 import 安裝摩西翻譯佮相關程式


class Command(BaseCommand):
    help = (
        '訓練Moses模型，會當選愛訓練啥物語言抑是全部語言的。\n'
        '裝Moses程式，掠而且編譯，可能愛半點鐘以上'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            nargs='*',
            help='愛訓練的語言'
        )
        parser.add_argument(
            '--全部語言攏訓練',
            dest='全部語言',
            default=False,
            action='store_const',
            const=True,
        )
        parser.add_argument(
            '--編譯核心數',
            dest='核心數',
            default=4,
            type=int,
        )

    def handle(self, *args, **參數):
        if not 參數['全部語言'] and len(參數['語言']) == 0:
            self.stdout.write('請指明愛訓練啥物語言的Moses模型！！')
            return
        if 參數['全部語言'] and len(參數['語言']) > 0:
            self.stdout.write('愛訓練全部語言的Moses模型無？！')
            return
        if 參數['全部語言']:
            語言陣列 = sorted(settings.HOK8_BU7_SIAT4_TING7.keys())
        else:
            語言陣列 = 參數['語言']
        安裝摩西翻譯佮相關程式.安裝gizapp()
        安裝摩西翻譯佮相關程式.安裝moses(編譯CPU數=參數['核心數'])
        Moses模型訓練.輸出全部語料()
        for 一个語言 in 語言陣列:
            try:
                服務設定 = settings.HOK8_BU7_SIAT4_TING7[一个語言]
                Moses模型訓練.訓練一个摩西翻譯模型(一个語言, 服務設定['語族'])
            except FileNotFoundError:
                print('訓練「{}」時發生問題！！'.format(一个語言), file=stderr)
                traceback.print_exc()
                print(file=stderr)

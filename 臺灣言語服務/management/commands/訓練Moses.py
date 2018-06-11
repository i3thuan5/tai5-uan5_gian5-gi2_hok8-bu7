from django.core.management.base import BaseCommand


from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯做母語模型資料夾
from 臺灣言語工具.翻譯.摩西工具.安裝摩西翻譯佮相關程式 import 安裝摩西翻譯佮相關程式


class Command(BaseCommand):
    help = (
        '訓練Moses模型，會用資料庫全部ê語料來訓練。\n'
        '裝Moses程式，掠而且編譯，可能愛半點鐘以上'
    )

    def 翻譯做資料夾(self):
        return 翻譯做母語模型資料夾

    def 訓練做(self):
        return Moses模型訓練.訓練翻譯做母語模型

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
        語料資料夾 = 翻譯語料資料夾(語言)
        模型資料夾 = self.翻譯做資料夾()(語言)
        Moses模型訓練.輸出全部語料(語料資料夾)
        self.訓練做()(語料資料夾, 模型資料夾)
